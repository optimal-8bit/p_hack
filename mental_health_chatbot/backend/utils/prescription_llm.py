"""
LLM-based prescription text analysis
Uses Phi-3 Mini for structured medicine extraction
"""

import json
import logging
import asyncio
import time
from typing import List, Dict, Optional
import config

logger = logging.getLogger(__name__)

# Import LLM components
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers not available. Install with: pip install transformers torch")

# Global model cache
_model = None
_tokenizer = None
_model_loaded = False


async def extract_medicines_with_llm(prescription_text: str) -> Optional[List[Dict]]:
    """
    Extract medicines from prescription text using LLM
    
    Returns:
        List of medicine dictionaries or None if extraction fails
    """
    if not config.LLM_ENABLED:
        logger.info("LLM disabled in config")
        return None
    
    if not TRANSFORMERS_AVAILABLE:
        logger.warning("Transformers not available")
        return None
    
    try:
        # Ensure model is loaded
        if not await _ensure_model_loaded():
            return None
        
        # Generate extraction with timeout
        result = await asyncio.wait_for(
            _run_extraction(prescription_text),
            timeout=config.LLM_TIMEOUT
        )
        
        return result
        
    except asyncio.TimeoutError:
        logger.warning(f"LLM extraction timeout ({config.LLM_TIMEOUT}s)")
        return None
    except Exception as e:
        logger.error(f"LLM extraction error: {e}", exc_info=True)
        return None


async def _ensure_model_loaded() -> bool:
    """Ensure model is loaded (lazy loading)"""
    global _model, _tokenizer, _model_loaded
    
    if _model_loaded:
        return _model is not None
    
    try:
        logger.info("Loading Phi-3 Mini for prescription analysis...")
        
        model, tokenizer = await asyncio.get_event_loop().run_in_executor(
            None, _load_model
        )
        
        _model = model
        _tokenizer = tokenizer
        _model_loaded = True
        
        if model is not None:
            logger.info("✅ Phi-3 Mini loaded successfully for prescription analysis")
            return True
        else:
            logger.warning("⚠️ Failed to load Phi-3 Mini")
            return False
            
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        _model_loaded = True
        return False


def _load_model():
    """Load Phi-3 Mini model"""
    try:
        model_name = config.LLM_MODEL_NAME
        
        # Detect device
        if torch.cuda.is_available():
            device = "cuda"
            device_map = "auto"
            torch_dtype = torch.float16
            logger.info("🚀 Using GPU for prescription analysis")
        else:
            device = "cpu"
            device_map = "cpu"
            torch_dtype = "auto"
            logger.info("⚠️ Using CPU for prescription analysis (will take 20-30 seconds)")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            torch_dtype=torch_dtype,
            trust_remote_code=True
        )
        
        logger.info(f"Model loaded on: {device.upper()}")
        return model, tokenizer
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None, None


async def _run_extraction(prescription_text: str) -> Optional[List[Dict]]:
    """Run medicine extraction"""
    global _model, _tokenizer
    
    if _model is None or _tokenizer is None:
        return None
    
    # Create extraction prompt
    system_prompt = """You are a medical prescription analyzer. Extract medicine information from prescription text.

For each medicine, extract:
- medicine_name: The name of the medicine
- dosage: The strength (e.g., "100mg", "500mg")
- frequency: How often (e.g., "twice daily", "once daily")
- instructions: Special instructions (e.g., "after meals", "before bed")

Return ONLY a valid JSON array. Example:
[
  {
    "medicine_name": "Aspirin",
    "dosage": "100mg",
    "frequency": "twice daily",
    "instructions": "take after meals"
  }
]

If no medicines found, return: []"""

    user_prompt = f"""Extract medicines from this prescription:

{prescription_text}

Return JSON array only:"""

    # Format messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        # Apply chat template
        prompt = _tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    except:
        # Fallback
        prompt = f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
    
    logger.info("Starting LLM generation for prescription analysis...")
    start_time = time.time()
    
    # Run generation in executor
    response = await asyncio.get_event_loop().run_in_executor(
        None, _generate, prompt
    )
    
    elapsed = time.time() - start_time
    logger.info(f"LLM generation completed in {elapsed:.1f}s")
    
    if not response:
        return None
    
    # Parse JSON response
    try:
        # Clean response
        cleaned = response.strip()
        
        # Remove markdown code blocks if present
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        
        # Find JSON array
        start_idx = cleaned.find('[')
        end_idx = cleaned.rfind(']')
        
        if start_idx == -1 or end_idx == -1:
            logger.warning("No JSON array found in response")
            return None
        
        json_str = cleaned[start_idx:end_idx+1]
        medicines = json.loads(json_str)
        
        if not isinstance(medicines, list):
            logger.warning("Response is not a list")
            return None
        
        logger.info(f"Successfully extracted {len(medicines)} medicines")
        return medicines
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        logger.debug(f"Response was: {response[:200]}")
        return None
    except Exception as e:
        logger.error(f"Error parsing response: {e}")
        return None


def _generate(prompt: str) -> Optional[str]:
    """Generate response with model"""
    global _model, _tokenizer
    
    try:
        # Tokenize
        inputs = _tokenizer(prompt, return_tensors="pt")
        input_length = inputs.input_ids.shape[1]
        
        # Move to device
        if hasattr(_model, 'device'):
            inputs = {k: v.to(_model.device) for k, v in inputs.items()}
        
        # Generate
        logger.info("Generating with model...")
        outputs = _model.generate(
            **inputs,
            max_new_tokens=config.LLM_MAX_TOKENS,
            temperature=config.LLM_TEMPERATURE,
            top_p=0.9,
            do_sample=True,
            pad_token_id=_tokenizer.eos_token_id
        )
        
        # Decode
        response = _tokenizer.decode(
            outputs[0][input_length:],
            skip_special_tokens=True
        )
        
        logger.info(f"Generated {len(response)} characters")
        return response
        
    except Exception as e:
        logger.error(f"Generation error: {e}", exc_info=True)
        return None
