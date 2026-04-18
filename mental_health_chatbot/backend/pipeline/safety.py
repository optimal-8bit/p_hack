import re
import logging
from dataclasses import dataclass
from typing import Optional
import config

logger = logging.getLogger(__name__)

# Distress patterns (not crisis, but elevated concern)
DISTRESS_PATTERNS = [
    r"\b(can't take it anymore|can't handle this)\b",
    r"\b(nobody cares|no one cares about me)\b",
    r"\b(what's the point|nothing matters)\b",
]

CRISIS_RESPONSE = """I'm really concerned about what you've shared. Please know that you are not alone, and help is available right now.

🆘 iCall India: 9152987821 (Mon–Sat, 8am–10pm)
🆘 Vandrevala Foundation: 1860-2662-345 (24/7)
🆘 iCall Chat: icallhelpline.org

If you are in immediate danger, please call 112 (Emergency) right now.

I'm here with you. Would you like to talk about what's happening?"""


@dataclass
class SafetyResult:
    is_crisis: bool
    crisis_type: Optional[str]  # "suicide", "self_harm", "general_distress"
    matched_pattern: Optional[str]
    response: Optional[str]  # pre-written response to return immediately if crisis


class SafetyChecker:
    def __init__(self):
        # Compile crisis patterns
        self.crisis_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in config.CRISIS_PATTERNS
        ]
        
        # Compile distress patterns
        self.distress_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in DISTRESS_PATTERNS
        ]
        
        logger.info("Safety checker initialized with crisis and distress patterns")
    
    def check(self, text: str) -> SafetyResult:
        """Check text for crisis indicators"""
        # Check crisis patterns first
        for pattern in self.crisis_patterns:
            match = pattern.search(text)
            if match:
                crisis_type = self._determine_crisis_type(match.group(0))
                logger.warning(f"CRISIS DETECTED: type={crisis_type}, pattern={match.group(0)}")
                
                return SafetyResult(
                    is_crisis=True,
                    crisis_type=crisis_type,
                    matched_pattern=match.group(0),
                    response=CRISIS_RESPONSE
                )
        
        # Check distress patterns (not crisis, but log for monitoring)
        for pattern in self.distress_patterns:
            match = pattern.search(text)
            if match:
                logger.info(f"Distress signal detected: {match.group(0)}")
                # Not a crisis, continue normal processing
                break
        
        # No crisis detected
        return SafetyResult(
            is_crisis=False,
            crisis_type=None,
            matched_pattern=None,
            response=None
        )
    
    def _determine_crisis_type(self, matched_text: str) -> str:
        """Determine specific crisis type from matched text"""
        matched_lower = matched_text.lower()
        
        if any(word in matched_lower for word in ["suicid", "kill myself", "end my life", "want to die", "wish i was dead"]):
            return "suicide"
        elif any(word in matched_lower for word in ["self harm", "self-harm", "cut myself", "hurt myself"]):
            return "self_harm"
        else:
            return "general_distress"


# Singleton instance
_safety_checker: Optional[SafetyChecker] = None


def get_safety_checker() -> SafetyChecker:
    """Get singleton safety checker instance"""
    global _safety_checker
    if _safety_checker is None:
        _safety_checker = SafetyChecker()
    return _safety_checker
