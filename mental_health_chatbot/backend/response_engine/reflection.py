"""
Advanced Reflection Module - Generates meaningful reflections (NOT copying text)
Transforms user statements into empathetic reflections
"""

import re
from typing import Optional


class ReflectionGenerator:
    """Generates natural, meaningful reflections from user input"""
    
    # Pattern-based transformation rules
    TRANSFORMATION_RULES = [
        # Failure/inadequacy patterns
        (r"(?:i feel like |i'm |i am )?(?:i'm )?failing (?:at )?everything", 
         "it feels like things aren't going the way you hoped"),
        (r"(?:i feel like |i'm |i am )?(?:a )?failure", 
         "it feels like you're being really hard on yourself"),
        (r"(?:i )?can't do anything right", 
         "it feels like nothing is working out"),
        
        # Loneliness/isolation patterns
        (r"(?:i feel |i'm feeling )?(?:so )?alone", 
         "it feels like you're disconnected from others"),
        (r"(?:i feel like )?(?:no one|nobody) (?:cares|understands)", 
         "it feels like you're not being seen or heard"),
        (r"(?:i have )?no (?:one|friends)", 
         "it feels like you're lacking connection"),
        
        # Hopelessness patterns
        (r"(?:there's )?no point (?:in|to) (?:anything|this)", 
         "it feels like things have lost their meaning"),
        (r"nothing matters", 
         "it feels like you're struggling to find purpose"),
        (r"(?:i )?can't go on", 
         "it feels like you're at a breaking point"),
        
        # Anxiety/worry patterns
        (r"(?:i'm |i am )?(?:so )?(?:anxious|worried) about (.+)", 
         "it sounds like {1} is weighing heavily on you"),
        (r"(?:i )?can't stop (?:worrying|thinking) about (.+)", 
         "it seems like {1} is consuming your thoughts"),
        (r"(?:i'm |i am )?(?:so )?stressed (?:about )?(.+)", 
         "it sounds like {1} is creating a lot of pressure"),
        
        # Overwhelm patterns
        (r"(?:i'm |i am )?overwhelmed", 
         "it feels like everything is too much right now"),
        (r"(?:i )?can't (?:handle|take) (?:this|it) anymore", 
         "it feels like you've reached your limit"),
        (r"everything is too much", 
         "it sounds like you're carrying a heavy load"),
        
        # Exhaustion patterns
        (r"(?:i'm |i am )?(?:so )?tired (?:of )?(.+)", 
         "it sounds like {1} has been draining"),
        (r"(?:i'm |i am )?exhausted", 
         "it feels like you're running on empty"),
        
        # Anger/frustration patterns
        (r"(?:i'm |i am )?(?:so )?(?:angry|frustrated) (?:with|about) (.+)", 
         "it sounds like {1} is really getting to you"),
        (r"(?:i )?hate (.+)", 
         "it seems like {1} is causing a lot of pain"),
        
        # Self-worth patterns
        (r"(?:i'm |i am )?(?:not )?good enough", 
         "it feels like you're doubting your worth"),
        (r"(?:i'm |i am )?worthless", 
         "it sounds like you're in a lot of pain about yourself"),
        (r"(?:i )?don't matter", 
         "it feels like you're questioning your value"),
    ]
    
    # Fallback reflection starters for when no pattern matches
    GENERIC_REFLECTIONS = [
        "it sounds like you're going through something difficult",
        "it seems like you're dealing with a lot right now",
        "it feels like this is really affecting you",
        "it sounds like you're carrying something heavy",
    ]
    
    def generate(self, text: str, emotion: str = None) -> Optional[str]:
        """
        Generate meaningful reflection from user text
        
        Args:
            text: User input text
            emotion: Detected emotion (optional, for context)
        
        Returns:
            Reflection string or None if unable to generate
        """
        text_lower = text.lower().strip()
        
        # Try pattern-based transformations
        for pattern, reflection_template in self.TRANSFORMATION_RULES:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                # If template has placeholders, fill them
                if '{1}' in reflection_template and len(match.groups()) > 0:
                    captured = match.group(1).strip()
                    # Clean up captured text
                    captured = self._clean_captured_text(captured)
                    reflection = reflection_template.replace('{1}', captured)
                else:
                    reflection = reflection_template
                
                return reflection
        
        # Try emotion-based generic reflection
        if emotion and emotion in ["sadness", "fear", "anger"]:
            return self._get_emotion_based_reflection(text_lower, emotion)
        
        # Fallback: extract key phrase and reflect
        key_phrase = self._extract_key_phrase(text_lower)
        if key_phrase:
            return f"it sounds like {key_phrase} is really affecting you"
        
        return None
    
    def _clean_captured_text(self, text: str) -> str:
        """Clean captured text from regex groups"""
        # Remove trailing punctuation
        text = re.sub(r'[.!?,;]+$', '', text)
        # Remove leading articles
        text = re.sub(r'^(the|a|an)\s+', '', text)
        # Limit length
        if len(text) > 40:
            text = text[:40].rsplit(' ', 1)[0] + "..."
        return text.strip()
    
    def _extract_key_phrase(self, text: str) -> Optional[str]:
        """Extract key phrase from text for reflection"""
        # Look for "about X" patterns
        about_match = re.search(r'about\s+(.{5,30}?)(?:[.!?,]|$)', text)
        if about_match:
            return self._clean_captured_text(about_match.group(1))
        
        # Look for "with X" patterns
        with_match = re.search(r'with\s+(.{5,30}?)(?:[.!?,]|$)', text)
        if with_match:
            return self._clean_captured_text(with_match.group(1))
        
        return None
    
    def _get_emotion_based_reflection(self, text: str, emotion: str) -> str:
        """Generate emotion-appropriate generic reflection"""
        emotion_reflections = {
            "sadness": "it sounds like you're in a lot of pain right now",
            "fear": "it seems like you're feeling really scared or anxious",
            "anger": "it sounds like something is really frustrating you",
        }
        return emotion_reflections.get(emotion, self.GENERIC_REFLECTIONS[0])


# Singleton instance
_reflection_generator: Optional[ReflectionGenerator] = None


def get_reflection_generator() -> ReflectionGenerator:
    """Get singleton reflection generator"""
    global _reflection_generator
    if _reflection_generator is None:
        _reflection_generator = ReflectionGenerator()
    return _reflection_generator


def generate_reflection(text: str, emotion: str = None) -> Optional[str]:
    """
    Convenience function to generate reflection
    
    Args:
        text: User input text
        emotion: Detected emotion (optional)
    
    Returns:
        Reflection string or None
    """
    generator = get_reflection_generator()
    return generator.generate(text, emotion)