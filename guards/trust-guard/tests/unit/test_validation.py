"""
Unit tests for Trust Guard validation engine
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from trustguard.validation import ValidationEngine


class TestValidationEngine:
    """Test the validation engine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = ValidationEngine()
    
    def test_initialization(self):
        """Test validator initializes correctly."""
        assert self.validator is not None
        assert hasattr(self.validator, 'kl_divergence_threshold')
        assert hasattr(self.validator, 'uncertainty_threshold')
        assert hasattr(self.validator, 'evidence_weights')
    
    def test_health_check(self):
        """Test validator health check."""
        assert self.validator.is_healthy() is True
    
    def test_mathematical_validation(self):
        """Test mathematical validation functionality."""
        input_text = "What is the capital of France?"
        output_text = "The capital of France is Paris."
        
        result = self.validator.perform_mathematical_validation(input_text, output_text)
        
        assert isinstance(result, dict)
        assert "kl_divergence" in result
        assert "uncertainty_score" in result
        assert "consistency_score" in result
        assert "statistical_metrics" in result
        assert "confidence_intervals" in result
        
        # Validate score ranges
        assert 0 <= result["kl_divergence"] <= 10.0
        assert 0 <= result["uncertainty_score"] <= 1.0
        assert 0 <= result["consistency_score"] <= 1.0
    
    def test_risk_assessment_calculation(self):
        """Test risk assessment calculation."""
        pattern_detections = {
            "hallucination": {"score": 0.8, "confidence": 0.9, "risk_level": "high"},
            "bias": {"score": 0.3, "confidence": 0.7, "risk_level": "medium"},
            "deception": {"score": 0.1, "confidence": 0.6, "risk_level": "low"}
        }
        
        result = self.validator.calculate_risk_assessment(pattern_detections)
        
        assert isinstance(result, dict)
        assert "score" in result
        assert "level" in result
        assert "description" in result
        assert "components" in result
        
        assert result["score"] > 0
        assert result["level"] in ["low", "medium", "high"]
        assert len(result["components"]) == 3
    
    def test_risk_assessment_empty_input(self):
        """Test risk assessment with empty input."""
        result = self.validator.calculate_risk_assessment({})
        
        assert result["score"] == 0.0
        assert result["level"] == "low"
        assert result["description"] == "No patterns detected"
    
    def test_evidence_generation(self):
        """Test evidence generation."""
        pattern_detections = {
            "hallucination": {"score": 0.7, "confidence": 0.8, "risk_level": "high", "evidence": ["test"]}
        }
        mathematical_scores = {
            "kl_divergence": 0.3,
            "uncertainty_score": 0.4,
            "consistency_score": 0.8
        }
        request = {"input_text": "test", "output_text": "test"}
        
        result = self.validator.generate_evidence(pattern_detections, mathematical_scores, request)
        
        assert isinstance(result, dict)
        assert "pattern_evidence" in result
        assert "mathematical_evidence" in result
        assert "confidence_factors" in result
        assert "risk_factors" in result
        assert "overall_confidence" in result
    
    def test_kl_divergence_calculation(self):
        """Test KL divergence calculation."""
        input_text = "What is the capital of France?"
        output_text = "Paris is the capital of France."
        
        result = self.validator._calculate_kl_divergence(input_text, output_text)
        
        assert isinstance(result, float)
        assert 0 <= result <= 10.0
    
    def test_uncertainty_quantification(self):
        """Test uncertainty quantification."""
        text = "Maybe this could possibly be the right answer, I think."
        result = self.validator._quantify_uncertainty(text)
        
        assert isinstance(result, float)
        assert 0 <= result <= 1.0
        assert result > 0.1  # Should detect some uncertainty
    
    def test_information_consistency(self):
        """Test information consistency check."""
        input_text = "What is the capital of France?"
        output_text = "Paris is the capital of France."
        
        result = self.validator._check_information_consistency(input_text, output_text)
        
        assert isinstance(result, float)
        assert 0 <= result <= 1.0
        assert result > 0.0  # Should have some consistency
    
    def test_statistical_analysis(self):
        """Test statistical analysis."""
        text = "This is a test text with multiple words and sentences. It has some complexity."
        result = self.validator._perform_statistical_analysis(text)
        
        assert isinstance(result, dict)
        assert "total_words" in result
        assert "unique_words" in result
        assert "lexical_diversity" in result
        assert "avg_sentence_length" in result
        assert "sentence_length_variance" in result
        assert "sentence_count" in result
        
        assert result["total_words"] > 0
        assert result["unique_words"] > 0
        assert 0 <= result["lexical_diversity"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
