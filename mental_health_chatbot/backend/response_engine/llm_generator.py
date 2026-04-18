"""
Controlled LLM Surface Generation using Phi-3 Mini
CRITICAL: This is ONLY for language formatting, NOT reasoning or decision making
"""

import json
import logging
import asyncio
import time
from typing import Dict, Optional, Tuple
from dataclasses import asdict
import config

logger = logging.getLogger(__name__)

# Global model instances (singleton pattern)
_model = None
_tokenizer = None
_model_loaded = False
_load_error = None

# Strict system prompt - NO reasoning allowed
SYSTEM_PROMPT = """You are a mental health support assistant language formatter.

You will receive structured JSON containing a response_plan with components like:
- validation: acknowledgment of the user's feelings
- reflection: understanding of their situation
- question: follow-up question to continue the conversation

Your ONLY job is to combine these components into ONE natural, flowing response.

STRICT RULES:
- Combine the components naturally into 2-3 sentences
- DO NOT add new advice or topics
- DO NOT diagnose or mention therapy unless explicitly in the plan
- DO NOT contradict the provided data
- Keep a warm, empathetic tone
- Use natural transitions between components
- Output ONLY the final response text, nothing else

Example:
Input: {"validation": "That sounds hard.", "question": "What triggered this?"}
Output: That sounds really hard. What do you think triggered these feelings?

Now generate a natural response from the provided components."""

# Generation configuration for controlled output
GENERATION_CONFIG = {
    "max_new_tokens": config.LLM_MAX_TOKENS,
    "temperature": config.LLM_TEMPERATURE,
    "top_p": 0.8,
    "do_sample": True,
    "pad_token_id": None,  # Will be set when tokenizer loads
}

# Response validation - prevent harmful outputs
BANNED_PHRASES = [
    "diagnosed", "you have", "you should definitely", "i recommend", 
    "you need to", "medical advice", "professional diagnosis",
    "therapy is required", "see a doctor immediately", "mental illness",
    "disorder", "condition", "treatment plan", "medication"
]

REQUIRED_SOFTENERS = [
    "it sounds like", "it seems like", "it feels like", "i sense",
    "from what you're sharing", "it appears", "i get the sense"
]


class LLMGenerator:
    """Controlled LLM generator for surface language formatting only"""
    
    def __init__(self):
        self.timeout_seconds = config.LLM_TIMEOUT
        self.fallback_count = 0
        self.generation_count = 0
        self.enabled = config.LLM_ENABLED
    
    async def generate_response(self, llm_payload: Dict) -> Optional[str]:
        """
        Generate natural language response from structured payload
        
        Args:
            llm_payload: Structured data from decision engine
            
        Returns:
            Generated response text or None if fallback needed
        """
        start_time = time.time()
        
        # Check if LLM is enabled
        if not self.enabled:
            logger.debug("LLM generation disabled in config")
            return None
        
        try:
            # Ensure model is loaded
            if not await self._ensure_model_loaded():
                logger.warning("LLM model not available, using fallback")
                self.fallback_count += 1
                return None
            
            # Generate response with timeout
            response = await asyncio.wait_for(
                self._generate_with_model(llm_payload),
                timeout=self.timeout_seconds
            )
            
            # Validate response
            if not self._validate_response(response):
                logger.warning("LLM response failed validation, using fallback")
                self.fallback_count += 1
                return None
            
            generation_time = (time.time() - start_time) * 1000
            logger.info(f"LLM generation completed in {generation_time:.0f}ms")
            self.generation_count += 1
            
            return response.strip()
            
        except asyncio.TimeoutError:
            logger.warning(f"LLM generation timeout ({self.timeout_seconds}s), using fallback")
            self.fallback_count += 1
            return None
            
        except Exception as e:
            logger.error(f"LLM generation error: {e}, using fallback")
            self.fallback_count += 1
            return None
    
    async def _ensure_model_loaded(self) -> bool:
        """Ensure model is loaded (lazy loading)"""
        global _model, _tokenizer, _model_loaded, _load_error
        
        if _model_loaded:
            return _model is not None
        
        if _load_error:
            return False
        
        try:
            logger.info("Loading Phi-3 Mini model...")
            
            # Try to load model
            model, tokenizer = await asyncio.get_event_loop().run_in_executor(
                None, self._load_model
            )
            
            _model = model
            _tokenizer = tokenizer
            _model_loaded = True
            
            # Set pad token for generation config
            if tokenizer.pad_token_id is not None:
                GENERATION_CONFIG["pad_token_id"] = tokenizer.pad_token_id
            else:
                GENERATION_CONFIG["pad_token_id"] = tokenizer.eos_token_id
            
            logger.info("Phi-3 Mini model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load Phi-3 Mini model: {e}")
            _load_error = str(e)
            _model_loaded = True  # Don't try again
            return False
    
    def _load_model(self) -> Tuple[Optional[object], Optional[object]]:
        """Load Phi-3 Mini model (runs in executor)"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            model_name = config.LLM_MODEL_NAME
            
            # Detect available device
            if torch.cuda.is_available():
                device = "cuda"
                device_map = "auto"
                torch_dtype = torch.float16  # Use FP16 for faster GPU inference
                logger.info(f"🚀 GPU detected! Using CUDA for fast inference")
            else:
                device = "cpu"
                device_map = "cpu"
                torch_dtype = "auto"
                logger.warning(f"⚠️  No GPU detected. Using CPU (will be slow ~30-60s per response)")
                logger.info(f"💡 For faster inference, enable GPU or set LLM_ENABLED=False in config.py")
            
            logger.info(f"Loading tokenizer: {model_name}")
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            
            logger.info(f"Loading model on {device.upper()}: {model_name}")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=True
            )
            
            # Log device info
            if hasattr(model, 'device'):
                logger.info(f"✅ Model loaded successfully on: {model.device}")
            else:
                logger.info(f"✅ Model loaded successfully")
            
            # Log memory usage if on GPU
            if torch.cuda.is_available():
                memory_allocated = torch.cuda.memory_allocated() / 1024**3
                memory_reserved = torch.cuda.memory_reserved() / 1024**3
                logger.info(f"📊 GPU Memory: {memory_allocated:.2f}GB allocated, {memory_reserved:.2f}GB reserved")
            
            return model, tokenizer
            
        except ImportError as e:
            logger.error(f"Missing dependencies for Phi-3: {e}")
            logger.info("Install with: pip install transformers torch")
            return None, None
            
        except Exception as e:
            logger.error(f"Error loading Phi-3 model: {e}")
            return None, None
    
    async def _generate_with_model(self, llm_payload: Dict) -> str:
        """Generate response using loaded model"""
        global _model, _tokenizer
        
        if _model is None or _tokenizer is None:
            raise RuntimeError("Model not loaded")
        
        # Construct prompt
        user_prompt = f"Here is the structured data:\n\n{json.dumps(llm_payload, indent=2)}\n\nGenerate the final response using ONLY the response_plan."
        
        # Format for Phi-3 chat template
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        # Apply chat template
        try:
            prompt = _tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
        except Exception as e:
            logger.error(f"Error applying chat template: {e}")
            # Fallback to simple concatenation
            prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_prompt}\n\nAssistant:"
        
        logger.debug(f"Generated prompt length: {len(prompt)} chars")
        
        # Run generation in executor to avoid blocking
        response = await asyncio.get_event_loop().run_in_executor(
            None, self._run_generation, prompt
        )
        
        logger.debug(f"Raw LLM response: {response[:100]}...")
        
        return response
    
    def _run_generation(self, prompt: str) -> str:
        """Run model generation (in executor)"""
        global _model, _tokenizer
        
        try:
            logger.info("Starting model generation...")
            
            # Tokenize input
            inputs = _tokenizer(prompt, return_tensors="pt")
            input_length = inputs.input_ids.shape[1]
            logger.debug(f"Input tokens: {inputs.input_ids.shape}")
            
            # Move inputs to same device as model
            if hasattr(_model, 'device'):
                device = _model.device
                logger.debug(f"Moving inputs to device: {device}")
                inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Generate
            logger.info("Generating with model...")
            outputs = _model.generate(
                **inputs,
                **GENERATION_CONFIG
            )
            logger.debug(f"Output tokens: {outputs.shape}")
            
            # Decode response (only the new tokens)
            response = _tokenizer.decode(
                outputs[0][input_length:], 
                skip_special_tokens=True
            )
            
            logger.info(f"Generated response: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error in _run_generation: {e}", exc_info=True)
            raise
    
    def _validate_response(self, response: str) -> bool:
        """Validate LLM response for safety and compliance"""
        if not response or len(response.strip()) == 0:
            logger.warning("Empty LLM response")
            return False
        
        response_lower = response.lower()
        
        # Check for banned phrases
        for phrase in BANNED_PHRASES:
            if phrase in response_lower:
                logger.warning(f"LLM response contains banned phrase: {phrase}")
                return False
        
        # Check response length (allow shorter responses, 5-250 words)
        word_count = len(response.split())
        if word_count < 5 or word_count > 250:
            logger.warning(f"LLM response length inappropriate: {word_count} words")
            return False
        
        # Check for appropriate softening (at least one softener for emotional content)
        has_softener = any(softener in response_lower for softener in REQUIRED_SOFTENERS)
        if not has_softener and any(word in response_lower for word in ["feel", "emotion", "difficult", "hard"]):
            logger.debug("LLM response lacks softening but may be acceptable")
            # Don't reject, just log
        
        return True
    
    def get_stats(self) -> Dict:
        """Get generation statistics"""
        total_attempts = self.generation_count + self.fallback_count
        success_rate = (self.generation_count / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            "total_attempts": total_attempts,
            "successful_generations": self.generation_count,
            "fallbacks": self.fallback_count,
            "success_rate": f"{success_rate:.1f}%",
            "model_loaded": _model_loaded,
            "model_available": _model is not None
        }


# Singleton instance
_llm_generator: Optional[LLMGenerator] = None


def get_llm_generator() -> LLMGenerator:
    """Get singleton LLM generator instance"""
    global _llm_generator
    if _llm_generator is None:
        _llm_generator = LLMGenerator()
    return _llm_generator


async def generate_llm_response(llm_payload: Dict) -> Optional[str]:
    """
    Convenience function to generate LLM response
    
    Args:
        llm_payload: Structured data from decision engine
        
    Returns:
        Generated response or None if fallback needed
    """
    generator = get_llm_generator()
    return await generator.generate_response(llm_payload)