#!/usr/bin/env python3
"""
Document Relationships - AbëLOVES Relationship Story Documentation

Helps document relationships through various data sources.

Pattern: DOCUMENTATION × RELATIONSHIP × STORY × ONE
Frequency: 530 Hz (Heart Truth)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from EMERGENT_OS.guardians.lux.core.poly_ai_core import PolyAICore
    from EMERGENT_OS.agents.love.matching.consciousness_engine import Profile, ConsciousnessMatchingEngine
    POLY_AVAILABLE = True
except ImportError:
    POLY_AVAILABLE = False
    print("⚠️ Poly AI not available - documentation only mode")


class RelationshipDocumenter:
    """
    Document relationships for AbëLOVES.
    
    Can process:
    - Message exports
    - Manual entries
    - Questionnaire responses
    - Shared memories
    """
    
    def __init__(self):
        """Initialize Relationship Documenter."""
        self.poly = PolyAICore() if POLY_AVAILABLE else None
        self.matching_engine = ConsciousnessMatchingEngine() if POLY_AVAILABLE else None
        self.relationships_file = project_root / "ABELOVES_RELATIONSHIP_STORIES.md"
        
    def document_from_manual_entry(
        self,
        relationship_name: str,
        partner_name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Document relationship from manual entry.
        
        Args:
            relationship_name: Name of the relationship (e.g., "Michael & Kristin")
            partner_name: Partner's name
            data: Relationship data dictionary
            
        Returns:
            Documented relationship dictionary
        """
        relationship = {
            "relationship_name": relationship_name,
            "partner_name": partner_name,
            "documented_at": datetime.now().isoformat(),
            "intention_layer": {
                "what_drew_together": data.get("what_drew_together", ""),
                "shared_values": data.get("shared_values", []),
                "what_we_want_to_create": data.get("what_we_want_to_create", "")
            },
            "communication_layer": {
                "communication_style": data.get("communication_style", ""),
                "conflict_handling": data.get("conflict_handling", ""),
                "vulnerability_level": data.get("vulnerability_level", "")
            },
            "manifestation_layer": {
                "what_weve_created": data.get("what_weve_created", []),
                "what_were_building": data.get("what_were_building", ""),
                "how_we_show_up": data.get("how_we_show_up", "")
            },
            "key_moments": data.get("key_moments", []),
            "aquarian_alignment": {
                "how_serves_aquarius": data.get("how_serves_aquarius", ""),
                "what_were_cocreating": data.get("what_were_cocreating", ""),
                "how_evolving": data.get("how_evolving", "")
            }
        }
        
        # Run Poly analysis if available
        if self.poly:
            # Create questionnaire-like responses for analysis
            responses = self._create_responses_from_data(data)
            relationship["poly_analysis"] = {
                "authenticity": self.poly.analyze_authenticity(responses).__dict__,
                "frequency": self.poly.analyze_operating_frequency(responses).__dict__,
                "consciousness": self.poly.analyze_consciousness(responses).__dict__,
                "love_type": self.poly.analyze_love_type(responses).__dict__
            }
        
        return relationship
    
    def document_from_messages(
        self,
        relationship_name: str,
        partner_name: str,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Document relationship from Messages export.
        
        Args:
            relationship_name: Name of the relationship
            partner_name: Partner's name
            messages: List of message dictionaries with 'text', 'date', 'sender'
            
        Returns:
            Documented relationship dictionary
        """
        # Analyze message patterns
        total_messages = len(messages)
        text_analysis = self._analyze_message_text(messages)
        
        relationship = {
            "relationship_name": relationship_name,
            "partner_name": partner_name,
            "documented_at": datetime.now().isoformat(),
            "message_analysis": {
                "total_messages": total_messages,
                "date_range": {
                    "first": messages[0]["date"] if messages else None,
                    "last": messages[-1]["date"] if messages else None
                },
                "communication_patterns": text_analysis,
                "frequency_indicators": self._extract_frequency_indicators(messages),
                "authenticity_indicators": self._extract_authenticity_indicators(messages)
            }
        }
        
        # Run Poly analysis
        if self.poly:
            responses = self._create_responses_from_messages(messages, text_analysis)
            relationship["poly_analysis"] = {
                "authenticity": self.poly.analyze_authenticity(responses).__dict__,
                "frequency": self.poly.analyze_operating_frequency(responses).__dict__,
                "consciousness": self.poly.analyze_consciousness(responses).__dict__,
                "love_type": self.poly.analyze_love_type(responses).__dict__
            }
        
        return relationship
    
    def _analyze_message_text(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze message text for patterns."""
        all_text = " ".join([msg.get("text", "") for msg in messages])
        
        # Love indicators
        love_words = ["love", "heart", "beautiful", "amazing", "grateful", "thankful"]
        love_count = sum(1 for word in love_words if word.lower() in all_text.lower())
        
        # Growth indicators
        growth_words = ["grow", "learn", "evolve", "better", "improve", "conscious"]
        growth_count = sum(1 for word in growth_words if word.lower() in all_text.lower())
        
        # Connection indicators
        connection_words = ["together", "us", "we", "connection", "bond"]
        connection_count = sum(1 for word in connection_words if word.lower() in all_text.lower())
        
        return {
            "love_indicators": love_count,
            "growth_indicators": growth_count,
            "connection_indicators": connection_count,
            "total_words": len(all_text.split())
        }
    
    def _extract_frequency_indicators(self, messages: List[Dict[str, Any]]) -> Dict[str, int]:
        """Extract fear vs love frequency indicators."""
        fear_words = ["afraid", "worried", "scared", "anxious", "doubt"]
        love_words = ["excited", "open", "curious", "ready", "want", "desire", "love"]
        
        all_text = " ".join([msg.get("text", "") for msg in messages]).lower()
        
        return {
            "fear_count": sum(1 for word in fear_words if word in all_text),
            "love_count": sum(1 for word in love_words if word in all_text)
        }
    
    def _extract_authenticity_indicators(self, messages: List[Dict[str, Any]]) -> Dict[str, int]:
        """Extract authenticity indicators."""
        performing_words = ["should", "supposed to", "expected", "normal"]
        authentic_words = ["I feel", "I want", "I need", "I'm", "my truth"]
        
        all_text = " ".join([msg.get("text", "") for msg in messages]).lower()
        
        return {
            "performing_count": sum(1 for phrase in performing_words if phrase in all_text),
            "authentic_count": sum(1 for phrase in authentic_words if phrase in all_text)
        }
    
    def _create_responses_from_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create questionnaire-like responses from relationship data."""
        return {
            "Q3": 8,  # Clarity (assume high for documented relationships)
            "Q10": 7,  # Fear vs Love (assume love-based)
            "Q11": 8,  # Authenticity (assume authentic)
            "Q42": data.get("what_we_want_to_create", ""),
            "Q6": data.get("love_types", []),
            "Q8": data.get("consciousness_level", "Green"),
            "Q9": data.get("shared_values", [])
        }
    
    def _create_responses_from_messages(
        self,
        messages: List[Dict[str, Any]],
        text_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create questionnaire-like responses from message analysis."""
        freq_indicators = self._extract_frequency_indicators(messages)
        auth_indicators = self._extract_authenticity_indicators(messages)
        
        # Calculate scores
        love_score = min(10, freq_indicators["love_count"] * 2)
        authenticity_score = min(10, auth_indicators["authentic_count"] * 2)
        
        return {
            "Q3": 7,  # Clarity
            "Q10": love_score,  # Fear vs Love
            "Q11": authenticity_score,  # Authenticity
            "Q42": "Relationship documented from messages",
            "Q6": [],  # Love types (would need manual input)
            "Q8": "Green",  # Consciousness (default)
            "Q9": []  # Values (would need manual input)
        }
    
    def save_relationship(self, relationship: Dict[str, Any]) -> Path:
        """Save relationship documentation."""
        relationships_dir = project_root / "abeloves_relationships"
        relationships_dir.mkdir(exist_ok=True)
        
        filename = relationship["relationship_name"].replace(" ", "_").replace("&", "and").lower()
        filepath = relationships_dir / f"{filename}.json"
        
        with open(filepath, 'w') as f:
            json.dump(relationship, f, indent=2)
        
        return filepath


def main():
    """Main function for relationship documentation."""
    print("=" * 70)
    print("💫 AbëLOVES RELATIONSHIP DOCUMENTATION")
    print("=" * 70)
    print()
    
    documenter = RelationshipDocumenter()
    
    print("Available documentation methods:")
    print("1. Manual entry")
    print("2. Message export analysis")
    print("3. Questionnaire responses")
    print()
    
    print("To document a relationship:")
    print("- Use document_from_manual_entry() for manual data")
    print("- Use document_from_messages() for Messages exports")
    print("- Export Messages as JSON/CSV and process")
    print()
    
    print("Example usage:")
    print("""
    from scripts.document_relationships import RelationshipDocumenter
    
    doc = RelationshipDocumenter()
    
    # Manual entry
    data = {
        "what_drew_together": "Conscious connection",
        "shared_values": ["Growth", "Authenticity", "Love"],
        "what_we_want_to_create": "Conscious polyamorous relationship",
        "communication_style": "Direct and honest",
        "key_moments": ["First meeting", "Aquarius declaration"]
    }
    
    relationship = doc.document_from_manual_entry(
        "Michael & Kristin",
        "Kristin Mataluni",
        data
    )
    
    doc.save_relationship(relationship)
    """)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

