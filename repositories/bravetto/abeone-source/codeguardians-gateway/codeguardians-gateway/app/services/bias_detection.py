"""
Bias Detection Service for CodeGuardians Gateway

Integrated bias detection functionality that eliminates the need for
a separate BiasGuard service with authentication issues.
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class BiasDetectionResult:
    """Result of bias detection analysis"""
    bias_detected: bool
    bias_score: float
    bias_types: List[str]
    bias_details: Dict[str, float]
    mitigation_suggestions: List[str]
    fairness_score: float
    confidence: float
    processing_time: float

class BiasDetectionService:
    """
    Integrated bias detection service for the CodeGuardians Gateway.
    
    Provides comprehensive bias detection without external dependencies
    or authentication requirements.
    """
    
    def __init__(self):
        """Initialize the bias detection service."""
        self.bias_patterns = self._load_bias_patterns()
        self.demographic_terms = self._load_demographic_terms()
        self.fairness_rules = self._load_fairness_rules()
        
    def _load_bias_patterns(self) -> Dict[str, List[str]]:
        """Load bias detection patterns."""
        return {
            "gender_bias": [
                r"\b(he|him|his)\b.*\b(she|her|hers)\b",
                r"\b(man|men)\b.*\b(woman|women)\b",
                r"\b(boys|girls)\b",
                r"\b(gentlemen|lady|ladies)\b",
                r"\b(men|women)\s+(are|is)\s+(better|worse|more|less)",
                r"\b(he|she)\s+(should|must)\s+(be|become)",
                r"\b(gender|sex)\s+(matters?|is\s+important)",
                r"\b(masculine|feminine)\s+(traits?|qualities?)"
            ],
            "racial_bias": [
                r"\b(white|black|brown|yellow|red)\s+(people|person|man|woman)\b",
                r"\b(african|asian|european|american)\s+(only|exclusively)\b",
                r"\b(ethnicity|race)\s+(matters|important)\b"
            ],
            "age_bias": [
                r"\b(young|old|elderly|senior|junior)\s+(people|person|man|woman)\b",
                r"\b(millennial|boomer|gen[xyz])\b",
                r"\b(too old|too young)\b"
            ],
            "socioeconomic_bias": [
                r"\b(rich|poor|wealthy|poverty)\s+(people|person|man|woman)\b",
                r"\b(upper|lower|middle)\s+class\b",
                r"\b(privileged|underprivileged)\b"
            ],
            "ability_bias": [
                r"\b(disabled|handicapped|retarded|crazy|insane)\b",
                r"\b(normal|abnormal)\s+(people|person|man|woman)\b",
                r"\b(mental|physical)\s+(illness|disability)\b"
            ]
        }
    
    def _load_demographic_terms(self) -> Dict[str, List[str]]:
        """Load demographic terms for analysis."""
        return {
            "gender": ["male", "female", "man", "woman", "boy", "girl", "masculine", "feminine"],
            "race": ["white", "black", "asian", "hispanic", "latino", "native", "indigenous"],
            "age": ["young", "old", "elderly", "senior", "junior", "adult", "child", "teenager"],
            "religion": ["christian", "muslim", "jewish", "hindu", "buddhist", "atheist", "agnostic"],
            "ability": ["disabled", "handicapped", "able-bodied", "neurotypical", "neurodivergent"]
        }
    
    def _load_fairness_rules(self) -> List[Dict[str, Any]]:
        """Load fairness assessment rules."""
        return [
            {
                "rule_id": "FAIRNESS_001",
                "name": "Equal Representation",
                "description": "Ensures equal representation across demographic groups",
                "weight": 0.3
            },
            {
                "rule_id": "FAIRNESS_002", 
                "name": "Inclusive Language",
                "description": "Promotes inclusive and neutral language",
                "weight": 0.25
            },
            {
                "rule_id": "FAIRNESS_003",
                "name": "Stereotype Avoidance",
                "description": "Avoids harmful stereotypes and generalizations",
                "weight": 0.25
            },
            {
                "rule_id": "FAIRNESS_004",
                "name": "Accessibility",
                "description": "Ensures content is accessible to all abilities",
                "weight": 0.2
            }
        ]
    
    async def detect_bias(
        self,
        text: str,
        bias_types: Optional[List[str]] = None,
        mitigation_level: str = "moderate",
        target_audience: str = "general"
    ) -> BiasDetectionResult:
        """
        Detect bias in the given text.
        
        Args:
            text: Text to analyze for bias
            bias_types: Specific types of bias to detect
            mitigation_level: Level of mitigation suggestions (low/moderate/aggressive)
            target_audience: Target audience for analysis
            
        Returns:
            BiasDetectionResult with detection results
        """
        start_time = datetime.now()
        
        try:
            # Analyze text for bias
            bias_analysis = self._analyze_text_bias(text, bias_types)
            
            # Calculate fairness score
            fairness_score = self._calculate_fairness_score(text, bias_analysis)
            
            # Generate mitigation suggestions
            suggestions = self._generate_mitigation_suggestions(
                bias_analysis, mitigation_level, target_audience
            )
            
            # Calculate overall bias score
            bias_score = self._calculate_bias_score(bias_analysis)
            
            # Determine if bias was detected
            bias_detected = bias_score > 0.05  # Even lower threshold for age bias sensitivity
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return BiasDetectionResult(
                bias_detected=bias_detected,
                bias_score=bias_score,
                bias_types=bias_analysis.get("detected_types", []),
                bias_details=bias_analysis.get("bias_details", {}),
                mitigation_suggestions=suggestions,
                fairness_score=fairness_score,
                confidence=min(0.95, bias_score + 0.1),  # Confidence based on bias score
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Bias detection error: {e}")
            return BiasDetectionResult(
                bias_detected=False,
                bias_score=0.0,
                bias_types=[],
                bias_details={},
                mitigation_suggestions=["Error in bias detection"],
                fairness_score=0.5,
                confidence=0.0,
                processing_time=(datetime.now() - start_time).total_seconds()
            )
    
    def _analyze_text_bias(self, text: str, bias_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analyze text for various types of bias."""
        text_lower = text.lower()
        detected_types = []
        bias_details = {}
        
        # Check each bias type
        for bias_category, patterns in self.bias_patterns.items():
            if bias_types and bias_category not in bias_types:
                continue
                
            category_score = 0.0
            matches = []
            
            for pattern in patterns:
                try:
                    if re.search(pattern, text_lower, re.IGNORECASE):
                        matches.append(pattern)
                        category_score += 0.3  # Increased scoring for better detection
                except re.error:
                    continue
            
            if category_score > 0:
                detected_types.append(bias_category)
                bias_details[bias_category] = min(1.0, category_score)
        
        return {
            "detected_types": detected_types,
            "bias_details": bias_details,
            "total_matches": sum(1 for score in bias_details.values() if score > 0)
        }
    
    def _calculate_fairness_score(self, text: str, bias_analysis: Dict[str, Any]) -> float:
        """Calculate overall fairness score."""
        base_score = 1.0
        
        # Reduce score based on detected bias
        for category, score in bias_analysis.get("bias_details", {}).items():
            base_score -= score * 0.3
        
        # Check for inclusive language
        inclusive_terms = ["inclusive", "diverse", "equitable", "accessible", "welcoming"]
        inclusive_count = sum(1 for term in inclusive_terms if term in text.lower())
        base_score += min(0.2, inclusive_count * 0.05)
        
        return max(0.0, min(1.0, base_score))
    
    def _generate_mitigation_suggestions(
        self,
        bias_analysis: Dict[str, Any],
        mitigation_level: str,
        target_audience: str
    ) -> List[str]:
        """Generate mitigation suggestions based on detected bias."""
        suggestions = []
        
        detected_types = bias_analysis.get("detected_types", [])
        
        if "gender_bias" in detected_types:
            suggestions.append("Use gender-neutral language (they/them instead of he/she)")
            suggestions.append("Include diverse gender examples")
        
        if "racial_bias" in detected_types:
            suggestions.append("Avoid racial generalizations and stereotypes")
            suggestions.append("Use inclusive, culturally sensitive language")
        
        if "age_bias" in detected_types:
            suggestions.append("Avoid age-based assumptions and stereotypes")
            suggestions.append("Use age-inclusive language")
        
        if "socioeconomic_bias" in detected_types:
            suggestions.append("Avoid assumptions about economic status")
            suggestions.append("Use inclusive language that doesn't assume privilege")
        
        if "ability_bias" in detected_types:
            suggestions.append("Use person-first language (person with disability)")
            suggestions.append("Avoid ableist language and assumptions")
        
        # Add general suggestions
        if not suggestions:
            suggestions.append("Review content for inclusive language")
            suggestions.append("Consider diverse perspectives and examples")
        
        # Adjust based on mitigation level
        if mitigation_level == "aggressive":
            suggestions.append("Conduct comprehensive bias review")
            suggestions.append("Get feedback from diverse stakeholders")
        elif mitigation_level == "moderate":
            suggestions.append("Review and revise problematic sections")
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _calculate_bias_score(self, bias_analysis: Dict[str, Any]) -> float:
        """Calculate overall bias score."""
        bias_details = bias_analysis.get("bias_details", {})
        
        if not bias_details:
            return 0.0
        
        # Weight different types of bias
        weights = {
            "gender_bias": 0.25,
            "racial_bias": 0.3,
            "age_bias": 0.2,
            "socioeconomic_bias": 0.15,
            "ability_bias": 0.1
        }
        
        weighted_score = sum(
            score * weights.get(category, 0.1)
            for category, score in bias_details.items()
        )
        
        return min(1.0, weighted_score)

# Global instance
bias_detection_service = BiasDetectionService()
