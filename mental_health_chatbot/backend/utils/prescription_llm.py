"""
Gemini Vision API for prescription image analysis
Direct image-to-LLM using langchain_google_genai (matches Con_Code implementation)
"""

import json
import logging
import base64
from typing import List, Dict, Optional
import os

logger = logging.getLogger(__name__)

# Import LangChain Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.error("LangChain Gemini not available. Install: pip install langchain-google-genai")

# Global Gemini model
_vision_llm = None
_gemini_configured = False


async def extract_medicines_from_image(image_bytes: bytes) -> Optional[List[Dict]]:
    """
    Send prescription image directly to Gemini Vision API using LangChain
    
    Args:
        image_bytes: Raw image bytes from upload
        
    Returns:
        List of medicine dicts or None if fails
    """
    if not GEMINI_AVAILABLE:
        logger.error("❌ LangChain Gemini SDK not installed")
        logger.error("Install: pip install langchain-google-genai")
        return None
    
    try:
        if not _ensure_gemini_configured():
            return None
        
        return await _analyze_image(image_bytes)
        
    except Exception as e:
        logger.error(f"❌ Gemini image analysis failed: {e}", exc_info=True)
        return None


def _ensure_gemini_configured() -> bool:
    """Configure Gemini API (synchronous)"""
    global _vision_llm, _gemini_configured
    
    if _gemini_configured:
        return _vision_llm is not None
    
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logger.error("❌ GEMINI_API_KEY not found in environment!")
            logger.error("❌ Make sure .env file exists with GEMINI_API_KEY")
            _gemini_configured = True
            return False
        
        # Get model name from environment or use default
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        
        logger.info(f"✅ Found GEMINI_API_KEY: {api_key[:10]}...")
        logger.info(f"✅ Using model: {model_name}")
        
        # Create LangChain Gemini Vision model (matches Con_Code implementation)
        _vision_llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.1,
            google_api_key=api_key,
        )
        
        _gemini_configured = True
        logger.info("✅ Gemini Vision API configured successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Gemini config failed: {e}", exc_info=True)
        _gemini_configured = True
        return False


async def _analyze_image(image_bytes: bytes) -> Optional[List[Dict]]:
    """Send image to Gemini and get medicines (matches Con_Code implementation)"""
    global _vision_llm
    
    if _vision_llm is None:
        logger.error("❌ Vision LLM not configured")
        return None
    
    system_prompt = """You are a clinical pharmacist AI. Extract prescription data from images accurately.
Convert medical abbreviations (BD = twice daily, TDS = thrice daily, QID = four times daily).
Be thorough and extract ALL visible medicines."""

    user_prompt = """Analyze this prescription image and extract ALL medicines.

For EACH medicine, extract:
- medicine_name: exact medicine name
- dosage: strength (e.g., "100mg", "500mg", "1 tablet")
- frequency: how often (e.g., "once daily", "twice daily", "BD", "TDS")
- instructions: special instructions (e.g., "after meals", "before bed")

**IMPORTANT: Carefully read the prescription image and extract all visible medicine details.**

Return ONLY valid JSON array:
[
  {
    "medicine_name": "Medicine Name",
    "dosage": "100mg",
    "frequency": "twice daily",
    "instructions": "take after meals"
  }
]

If no medicines visible, return: []
JSON ONLY, no markdown, no other text!"""

    try:
        logger.info("📸 Sending image to Gemini Vision API via LangChain...")
        
        # Convert image to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        logger.info(f"📄 Image size: {len(image_bytes)} bytes, base64: {len(image_base64)} chars")
        
        # Create multimodal message (matches Con_Code implementation)
        message = HumanMessage(
            content=[
                {"type": "text", "text": f"{system_prompt}\n\n{user_prompt}"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                },
            ]
        )
        
        # Call Gemini Vision API
        logger.info("🚀 Invoking Gemini Vision model...")
        response = await _vision_llm.ainvoke([message])
        
        if not response or not response.content:
            logger.error("❌ Gemini returned empty response")
            return None
        
        response_text = response.content if isinstance(response.content, str) else str(response.content)
        logger.info(f"✅ Gemini response received: {len(response_text)} chars")
        logger.info(f"📝 Raw response: {response_text[:300]}...")
        
        # Parse JSON
        cleaned = response_text.strip()
        
        # Remove markdown code blocks
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        
        # Extract JSON array
        start = cleaned.find('[')
        end = cleaned.rfind(']')
        
        if start == -1 or end == -1:
            logger.error(f"❌ No JSON array in response: {response_text[:200]}")
            return None
        
        json_str = cleaned[start:end+1]
        medicines = json.loads(json_str)
        
        if not isinstance(medicines, list):
            logger.error("❌ Response is not a list")
            return None
        
        logger.info(f"✅ Successfully extracted {len(medicines)} medicines:")
        for med in medicines:
            logger.info(f"  • {med.get('medicine_name')} - {med.get('dosage')} - {med.get('frequency')}")
        
        return medicines
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parse error: {e}")
        logger.error(f"Response was: {response_text[:500]}")
        return None
    except Exception as e:
        logger.error(f"❌ Image analysis error: {e}", exc_info=True)
        return None
