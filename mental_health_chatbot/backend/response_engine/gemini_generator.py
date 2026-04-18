"""
Gemini API-based LLM Surface Generator
CRITICAL: This is ONLY for language formatting, NOT reasoning or decision making
"""

import os
import logging
import asyncio
import time
from typing import Dict, Optional
import json

logger = logging.getLogger(__name__)

# Global model instance (singleton pattern)
_model = None
_model_loaded = False
_load_error = None

# Strict system prompt - NO reasoning allowed
SYSTEM_PROMPT = """You are a mental health support assistant language formatter.

You are NOT allowed to think, reason, analyze, or generate new ideas.

You will receive structured data containing:
- emotion
- intent
- context
- response_plan

Your ONLY job is to convert the response_plan into a natural, human-like message.

CRITICAL RULES:
- You MUST use ONLY the text provided inside response_plan
- You MUST NOT add any new advice, suggestions, or concepts
- You MUST NOT introduce new sentences beyond response_plan content
- You MUST NOT change the meaning of any field
- You MUST NOT hallucinate context or emotions

STRUCTURE RULES:
- Combine the fields in this order:
  1. validation
  2. reflection
  3. coping (if exists)
  4. question

STYLE RULES:
- Keep response between 3–4 sentences
- Use a warm, empathetic tone
- Use soft language (e.g., "it feels like", "it sounds like")
- Keep it natural and conversational

If response_plan is incomplete:
- gracefully connect available parts
- do NOT invent missing parts

Output ONLY the final message text."""

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


class GeminiGenerator:
    """Gemini API-based generator for surface language formatting only"""
    
    def __init__(self):
        # Get timeout from environment or use default
        timeout_str = os.getenv("GEMINI_TIMEOUT", "3.0")
        try:
            self.timeout_seconds = float(timeout_str)
        except ValueError:
            logger.warning(f"Invalid GEMINI_TIMEOUT value: {timeout_str}, using default 3.0s")
            self.timeout_seconds = 3.0
        
        self.fallback_count = 0
        self.generation_count = 0
        self.enabled = os.getenv("GEMINI_API_KEY") is not None
        self.total_latency = 0.0
    
    async def generate_response(self, llm_payload: Dict) -> Optional[str]:
        """
        Generate natural language response from structured payload
        
        Args:
            llm_payload: Structured data from decision engine
            
        Returns:
            Generated response text or None if fallback needed
        """
        start_time = time.time()
        
        # Check if Gemini is enabled
        if not self.enabled:
            logger.debug("Gemini API key not set, using fallback")
            return None
        
        # Validate response_plan exists and has content
        response_plan = llm_payload.get("response_plan", {})
        if not response_plan.get("validation"):
            logger.warning("Invalid or empty response_plan, using fallback")
            return None
        
        try:
            # Ensure model is loaded
            if not await self._ensure_model_loaded():
                logger.warning("Gemini model not available, using fallback")
                self.fallback_count += 1
                return None
            
            # Generate response with timeout
            response = await asyncio.wait_for(
                self._generate_with_model(llm_payload),
                timeout=self.timeout_seconds
            )
            
            # Clean up response
            response = self._cleanup_response(response)
            
            # Validate response
            if not self._validate_response(response):
                logger.warning("Gemini response failed validation, using fallback")
                self.fallback_count += 1
                return None
            
            generation_time = (time.time() - start_time) * 1000
            self.total_latency += generation_time
            logger.info(f"Gemini generation completed in {generation_time:.0f}ms")
            self.generation_count += 1
            
            return response.strip()
            
        except asyncio.TimeoutError:
            logger.warning(f"Gemini generation timeout ({self.timeout_seconds}s), using fallback")
            self.fallback_count += 1
            return None
            
        except Exception as e:
            logger.error(f"Gemini generation error: {e}, using fallback")
            self.fallback_count += 1
            return None
    
    async def _ensure_model_loaded(self) -> bool:
        """Ensure Gemini model is loaded (lazy loading)"""
        global _model, _model_loaded, _load_error
        
        if _model_loaded:
            return _model is not None
        
        if _load_error:
            return False
        
        try:
            logger.info("Loading Gemini model...")
            
            # Try to load model
            model = await asyncio.get_event_loop().run_in_executor(
                None, self._load_model
            )
            
            _model = model
            _model_loaded = True
            
            logger.info("Gemini model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load Gemini model: {e}")
            _load_error = str(e)
            _model_loaded = True  # Don't try again
            return False
    
    def _load_model(self) -> Optional[object]:
        """Load Gemini model (runs in executor)"""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.error("GEMINI_API_KEY environment variable not set")
                return None
            
            # Get model name from environment or use default
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Create model instance
            model = genai.GenerativeModel(model_name)
            
            logger.info(f"✅ Gemini API configured successfully (model: {model_name})")
            return model
            
        except ImportError as e:
            logger.error(f"Missing google-generativeai package: {e}")
            logger.info("Install with: pip install google-generativeai")
            return None
            
        except Exception as e:
            logger.error(f"Error loading Gemini model: {e}")
            return None
    
    async def _generate_with_model(self, llm_payload: Dict) -> str:
        """Generate response using Gemini API"""
        global _model
        
        if _model is None:
            raise RuntimeError("Model not loaded")
        
        # Build prompt
        user_prompt = self._build_prompt(llm_payload)
        
        # Combine system and user prompts
        full_prompt = f"{SYSTEM_PROMPT}\n\n{user_prompt}"
        
        logger.debug(f"Generated prompt length: {len(full_prompt)} chars")
        
        # Run generation in executor to avoid blocking
        response = await asyncio.get_event_loop().run_in_executor(
            None, self._run_generation, full_prompt
        )
        
        logger.debug(f"Raw Gemini response: {response[:100]}...")
        
        return response
    
    def _build_prompt(self, llm_payload: Dict) -> str:
        """Build user prompt from payload"""
        response_plan = llm_payload.get("response_plan", {})
        decision = llm_payload.get("decision_engine", {})
        constraints = llm_payload.get("constraints", {})
        
        return f"""You are given structured data.

IMPORTANT:
- Only use response_plan fields to generate the response.
- Do NOT use other fields to invent new content.

RESPONSE PLAN:
validation: {response_plan.get("validation", "")}
reflection: {response_plan.get("reflection", "")}
coping: {response_plan.get("coping", "")}
question: {response_plan.get("question", "")}

CONSTRAINTS:
- max_sentences: {constraints.get("max_sentences", 4)}
- tone: {decision.get("tone", "warm and empathetic")}

Generate the final response strictly following the rules."""
    
    def _run_generation(self, prompt: str) -> str:
        """Run model generation (in executor)"""
        global _model
        
        try:
            logger.info("Starting Gemini generation...")
            
            # Generate with Gemini
            response = _model.generate_content(prompt)
            
            # Extract text
            if hasattr(response, 'text'):
                text = response.text
            elif hasattr(response, 'parts'):
                text = ''.join(part.text for part in response.parts)
            else:
                raise ValueError("Unexpected response format from Gemini")
            
            logger.info(f"Generated response: {text[:100]}...")
            return text
            
        except Exception as e:
            # Enhanced error logging with specific error types
            error_msg = str(e).lower()
            
            if "429" in str(e) or "quota" in error_msg or "rate limit" in error_msg:
                logger.error("🚫 RATE LIMIT EXCEEDED")
                logger.error("   Free tier: 15 requests/minute")
                logger.error("   Wait 1 minute or upgrade to paid tier")
                logger.error("   System will use template fallback")
            elif "404" in str(e) or "not found" in error_msg:
                logger.error(f"🚫 MODEL NOT FOUND: {os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')}")
                logger.error("   Available models: gemini-pro, gemini-2.0-flash-exp")
                logger.error("   Update GEMINI_MODEL in .env file")
            elif "403" in str(e) or "permission" in error_msg or "api key" in error_msg:
                logger.error("🚫 API KEY INVALID OR EXPIRED")
                logger.error("   Check your GEMINI_API_KEY in .env file")
                logger.error("   Get new key: https://makersuite.google.com/app/apikey")
            elif "timeout" in error_msg or "deadline" in error_msg:
                logger.error("🚫 REQUEST TIMEOUT")
                logger.error("   Gemini API took too long to respond")
                logger.error("   Check your internet connection")
            else:
                logger.error(f"🚫 GEMINI ERROR: {e}")
            
            logger.info("✅ Using template fallback (system continues working)")
            raise
    
    def _cleanup_response(self, response: str) -> str:
        """Clean up and format the response"""
        if not response:
            return response
        
        # Strip whitespace
        response = response.strip()
        
        # Capitalize first letter if needed
        if response and not response[0].isupper():
            response = response[0].upper() + response[1:]
        
        # Ensure proper ending punctuation
        if response and response[-1] not in '.!?':
            response += '.'
        
        return response
    
    def _validate_response(self, response: str) -> bool:
        """Validate Gemini response for safety and compliance"""
        if not response or len(response.strip()) == 0:
            logger.warning("Empty Gemini response")
            return False
        
        response_lower = response.lower()
        
        # Check for banned phrases
        for phrase in BANNED_PHRASES:
            if phrase in response_lower:
                logger.warning(f"Gemini response contains banned phrase: {phrase}")
                return False
        
        # Check response length (allow 5-250 words)
        word_count = len(response.split())
        if word_count < 5 or word_count > 250:
            logger.warning(f"Gemini response length inappropriate: {word_count} words")
            return False
        
        # Check sentence count (should be 3-5 sentences max)
        sentence_count = len([s for s in response.split('.') if s.strip()])
        if sentence_count > 5:
            logger.warning(f"Too many sentences from Gemini: {sentence_count}")
            return False
        
        # Check for repetition (at least 60% unique words)
        words = response_lower.split()
        if len(words) > 5:  # Only check if response has enough words
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.6:
                logger.warning(f"Repetitive response detected: {unique_ratio:.2f} unique ratio")
                return False
        
        # Check for appropriate softening (at least one softener for emotional content)
        has_softener = any(softener in response_lower for softener in REQUIRED_SOFTENERS)
        if not has_softener and any(word in response_lower for word in ["feel", "emotion", "difficult", "hard"]):
            logger.debug("Gemini response lacks softening but may be acceptable")
            # Don't reject, just log
        
        return True
    
    def get_stats(self) -> Dict:
        """Get generation statistics"""
        total_attempts = self.generation_count + self.fallback_count
        success_rate = (self.generation_count / total_attempts * 100) if total_attempts > 0 else 0
        avg_latency = (self.total_latency / self.generation_count) if self.generation_count > 0 else 0
        
        return {
            "total_attempts": total_attempts,
            "successful_generations": self.generation_count,
            "fallbacks": self.fallback_count,
            "success_rate": f"{success_rate:.1f}%",
            "avg_latency_ms": f"{avg_latency:.0f}",
            "model_loaded": _model_loaded,
            "model_available": _model is not None,
            "api_key_set": self.enabled
        }


# Singleton instance
_gemini_generator: Optional[GeminiGenerator] = None


def get_gemini_generator() -> GeminiGenerator:
    """Get singleton Gemini generator instance"""
    global _gemini_generator
    if _gemini_generator is None:
        _gemini_generator = GeminiGenerator()
    return _gemini_generator


async def generate_gemini_response(llm_payload: Dict) -> Optional[str]:
    """
    Convenience function to generate Gemini response
    
    Args:
        llm_payload: Structured data from decision engine
        
    Returns:
        Generated response or None if fallback needed
    """
    generator = get_gemini_generator()
    return await generator.generate_response(llm_payload)
