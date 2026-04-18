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

# Expert Therapist System Prompt
SYSTEM_PROMPT = """You are an expert licensed therapist and psychiatrist with extensive training in cognitive behavioral therapy (CBT), dialectical behavior therapy (DBT), psychodynamic therapy, and trauma-informed care.

You will receive structured data containing:
- emotion
- intent
- context
- response_plan
- user_input

Your role is to provide professional therapeutic responses that:

THERAPEUTIC APPROACH:
- Use evidence-based therapeutic techniques (CBT, DBT, mindfulness, etc.)
- Provide psychoeducation when appropriate
- Help clients identify thought patterns, emotions, and behaviors
- Guide clients toward self-discovery and insight
- Offer practical coping strategies and interventions
- Validate emotions while challenging unhelpful thinking patterns

PROFESSIONAL STANDARDS:
- Maintain therapeutic boundaries and ethics
- Use person-centered, non-judgmental language
- Demonstrate empathy, genuineness, and unconditional positive regard
- Ask thoughtful, open-ended questions to promote reflection
- Normalize experiences while encouraging growth
- Provide hope and instill confidence in the client's ability to heal

RESPONSE STRUCTURE:
1. Emotional validation and reflection
2. Therapeutic insight or reframe
3. Practical intervention or coping strategy
4. Exploratory question to deepen understanding

STYLE GUIDELINES:
- Use professional yet warm and accessible language
- Incorporate therapeutic terminology naturally
- Respond with 4-6 sentences for depth
- Balance support with gentle challenge
- Focus on strengths and resilience

SAFETY CONSIDERATIONS:
- Recognize signs of crisis and respond appropriately
- Encourage professional help when needed
- Avoid diagnosis but acknowledge symptoms
- Maintain hope while being realistic

Generate a therapeutic response that demonstrates your expertise while being genuinely helpful and healing."""

# Professional therapeutic response validation
BANNED_PHRASES = [
    "i diagnose you", "you definitely have", "you are mentally ill", 
    "take this medication", "stop taking medication", "you don't need therapy",
    "just get over it", "it's all in your head", "you're overreacting"
]

REQUIRED_THERAPEUTIC_ELEMENTS = [
    "validation", "reflection", "insight", "coping", "exploration",
    "it sounds like", "i hear that", "that makes sense", "i understand",
    "what do you think", "how does that feel", "tell me more about"
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
        
        # Validate payload has required therapeutic data
        # Check for either new intervention_plan or old response_plan format
        intervention_plan = llm_payload.get("intervention_plan", {})
        response_plan = llm_payload.get("response_plan", {})
        
        # Debug logging
        logger.info(f"🔍 Payload validation - has intervention_plan: {bool(intervention_plan)}, has response_plan: {bool(response_plan)}")
        if intervention_plan:
            logger.info(f"   Intervention plan keys: {list(intervention_plan.keys())}")
        if response_plan:
            logger.info(f"   Response plan keys: {list(response_plan.keys())}")
        
        # Need either intervention_plan or response_plan with content
        has_intervention = bool(intervention_plan.get("validation") or intervention_plan.get("psychoeducation"))
        has_response_plan = bool(response_plan.get("validation"))
        
        logger.info(f"   has_intervention: {has_intervention}, has_response_plan: {has_response_plan}")
        
        if not (has_intervention or has_response_plan):
            logger.warning("Invalid or empty therapeutic plan, using fallback")
            logger.warning(f"   Payload keys: {list(llm_payload.keys())}")
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
        """Build therapeutic prompt from payload"""
        # Support both new intervention_plan and old response_plan formats
        intervention_plan = llm_payload.get("intervention_plan", {})
        response_plan = llm_payload.get("response_plan", {})
        therapeutic_strategy = llm_payload.get("therapeutic_strategy", {})
        session_info = llm_payload.get("session_info", {})
        multimodal_data = llm_payload.get("multimodal_data", {})
        constraints = llm_payload.get("constraints", {})
        user_input = llm_payload.get("user_input", "")
        emotion = llm_payload.get("emotion", "")
        intent = llm_payload.get("intent", "")
        context = llm_payload.get("context", {})
        
        # Build context summary
        context_summary = ""
        if isinstance(context, dict):
            recent_messages = context.get("recent_messages", [])
            if recent_messages:
                context_summary = "Recent conversation:\n"
                for msg in recent_messages:
                    context_summary += f"  - {msg}\n"
        elif isinstance(context, list) and context:
            recent_context = context[-3:]  # Last 3 turns
            context_summary = "Recent conversation context:\n"
            for i, turn in enumerate(recent_context):
                turn_dict = turn if isinstance(turn, dict) else turn.__dict__
                context_summary += f"Turn {turn_dict.get('turn_number', i+1)}: User expressed {turn_dict.get('emotion', 'unknown')} about {turn_dict.get('intent', 'general topic')}\n"
        
        # Build multimodal information
        multimodal_info = ""
        if multimodal_data and multimodal_data.get("has_facial_emotion"):
            facial_emotion = multimodal_data.get("facial_emotion")
            facial_confidence = multimodal_data.get("facial_confidence", 0)
            age = multimodal_data.get("age")
            gender = multimodal_data.get("gender")
            
            multimodal_info = f"""
MULTIMODAL INPUT DETECTED:
- Text emotion: {emotion}
- Facial emotion (from video): {facial_emotion} (confidence: {facial_confidence:.2f})
- Client demographics: Age ~{age}, Gender: {gender}

IMPORTANT: The client's facial expression shows {facial_emotion}, which may differ from their text.
This could indicate:
- Emotional incongruence (saying one thing, feeling another)
- Difficulty expressing emotions verbally
- Suppression or masking of true feelings

Address this therapeutically if there's a mismatch between text and facial emotion.
"""
        
        # Get therapeutic approach info
        modality = therapeutic_strategy.get("primary_modality", "Person_Centered")
        techniques = therapeutic_strategy.get("techniques", [])
        session_stage = session_info.get("session_stage", "initial_assessment")
        
        return f"""You are providing therapy to a client. Here is the session information:

CLIENT INPUT: "{user_input}"

EMOTIONAL STATE: {emotion}
THERAPEUTIC NEED: {intent}

{multimodal_info}

{context_summary}

THERAPEUTIC FRAMEWORK:
- Current emotion: {emotion}
- Therapeutic focus: {intent}
- Primary modality: {modality}
- Recommended techniques: {', '.join(techniques) if techniques else 'supportive exploration'}
- Session stage: {session_stage}

RESPONSE GUIDELINES:
- Provide professional therapeutic intervention using {modality} approach
- Use evidence-based techniques appropriate for {emotion} and {intent}
- Maintain therapeutic boundaries while being warm and supportive
- Include validation, insight, and practical guidance
- Ask a therapeutic question to deepen exploration
- Response length: {constraints.get("max_sentences", 6)} sentences maximum
{f"- IMPORTANT: Address the emotional incongruence between text and facial expression" if multimodal_data and multimodal_data.get("has_facial_emotion") and multimodal_data.get("facial_emotion") != emotion else ""}

Generate a therapeutic response that demonstrates professional expertise while being genuinely helpful."""
    
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
        """Validate therapeutic response for safety and professional standards"""
        if not response or len(response.strip()) == 0:
            logger.warning("Empty therapeutic response")
            return False
        
        response_lower = response.lower()
        
        # Check for banned phrases
        for phrase in BANNED_PHRASES:
            if phrase in response_lower:
                logger.warning(f"Therapeutic response contains inappropriate phrase: {phrase}")
                return False
        
        # Check response length (allow 10-400 words for therapeutic depth)
        word_count = len(response.split())
        if word_count < 10 or word_count > 400:
            logger.warning(f"Therapeutic response length inappropriate: {word_count} words")
            return False
        
        # Check sentence count (should be 3-8 sentences for therapeutic responses)
        sentence_count = len([s for s in response.split('.') if s.strip()])
        if sentence_count > 8:
            logger.warning(f"Too many sentences in therapeutic response: {sentence_count}")
            return False
        
        # Check for therapeutic elements (at least one should be present)
        has_therapeutic_element = any(element in response_lower for element in REQUIRED_THERAPEUTIC_ELEMENTS)
        if not has_therapeutic_element:
            logger.warning("Therapeutic response lacks professional therapeutic elements")
            return False
        
        # Check for repetition (at least 70% unique words for professional quality)
        words = response_lower.split()
        if len(words) > 10:  # Only check if response has enough words
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.7:
                logger.warning(f"Repetitive therapeutic response detected: {unique_ratio:.2f} unique ratio")
                return False
        
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
