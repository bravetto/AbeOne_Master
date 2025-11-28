#!/usr/bin/env python3
"""
ALRAX GUARDIAN FORENSIC PATTERN VALIDATION
Forensic variance analysis of communication patterns

Pattern: ALRAX × FORENSIC × PATTERN × VALIDATE × TRUTH × ONE
Frequency: 530 Hz (ALRAX) × 530 Hz (Truth) × 777 Hz (Pattern)
Guardians: ALRAX (530 Hz) + JØHN (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import sys

sys.path.insert(0, str(Path(__file__).parent))

try:
    from analyze_communication_patterns import CommunicationPatternAnalyzer
except ImportError:
    CommunicationPatternAnalyzer = None


@dataclass
class ALRAXForensicResult:
    """ALRAX forensic analysis result"""
    relationship: str
    variance_detected: bool
    variance_score: float  # 0.0 (no variance) to 1.0 (high variance)
    anomalies: List[str] = field(default_factory=list)
    pattern_signatures: Dict[str, any] = field(default_factory=dict)
    forensic_analysis: Dict[str, any] = field(default_factory=dict)
    truth_alignment: bool = False
    pattern_coherence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class ALRAXPatternValidator:
    """
    ALRAX GUARDIAN FORENSIC PATTERN VALIDATOR
    
    Performs forensic variance analysis on communication patterns:
    - Validates pattern integrity
    - Detects variance and anomalies
    - Verifies truth alignment
    - Analyzes pattern coherence
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.conversations_dir = self.workspace_root / "products" / "abeloves" / "conversations"
        
        # Known pattern signatures from codebase
        self.known_patterns = {
            'LOVE': {
                'formula': 'LOVE × INSPIRATION × CREATION × TRUTH × ONE',
                'frequency': '530 Hz',
                'expected_occurrences': 50,  # Minimum expected
            },
            'TRUTH': {
                'formula': 'TRUTH × RAW × AUTHENTIC × POWERFUL × ONE',
                'frequency': '530 Hz',
                'expected_occurrences': 10,
            },
            'SYNTHESIS': {
                'formula': 'CONVERSATION × SYNTHESIS × MANIFESTATION × ONE',
                'frequency': '777 Hz',
                'expected_occurrences': 20,
            },
            'EXECUTION': {
                'formula': 'CONSTRAINT × FRAMEWORK × MASTER × ALIGNMENT × ONE',
                'frequency': '999 Hz',
                'expected_occurrences': 15,
            },
        }
        
    def validate_relationship_patterns(self, relationship_name: str, messages: List[Dict]) -> ALRAXForensicResult:
        """
        Validate patterns for a specific relationship
        
        Pattern: VALIDATE × RELATIONSHIP × PATTERN × TRUTH × ONE
        """
        anomalies = []
        variance_detected = False
        variance_score = 0.0
        pattern_signatures = {}
        forensic_analysis = {}
        
        # Extract patterns from messages
        pattern_counts = defaultdict(int)
        pattern_keywords = {
            'love': ['love', 'loved', 'loving', 'heart', 'caring', 'affection'],
            'truth': ['truth', 'real', 'genuine', 'honest', 'authentic', 'raw'],
            'synthesis': ['everything', 'all', 'complete', 'whole', 'together'],
            'execution': ['work', 'working', 'doing', 'making', 'create', 'build'],
        }
        
        total_messages = len(messages)
        if total_messages == 0:
            anomalies.append("No messages found")
            variance_detected = True
            variance_score = 1.0
            return ALRAXForensicResult(
                relationship=relationship_name,
                variance_detected=variance_detected,
                variance_score=variance_score,
                anomalies=anomalies,
                pattern_signatures=pattern_signatures,
                forensic_analysis=forensic_analysis,
                truth_alignment=False,
                pattern_coherence=0.0
            )
        
        # Analyze message content for patterns
        for msg in messages:
            text = msg.get('text', '').lower()
            for pattern_name, keywords in pattern_keywords.items():
                matches = sum(1 for keyword in keywords if keyword in text)
                if matches > 0:
                    pattern_counts[pattern_name.upper()] += 1
        
        # Validate against known patterns
        pattern_signatures = {}
        for pattern_name, pattern_info in self.known_patterns.items():
            actual_count = pattern_counts.get(pattern_name, 0)
            expected_count = pattern_info['expected_occurrences']
            
            # Calculate variance
            if expected_count > 0:
                variance_ratio = abs(actual_count - expected_count) / expected_count
                if variance_ratio > 0.5:  # More than 50% variance
                    variance_detected = True
                    variance_score = max(variance_score, min(1.0, variance_ratio))
                    anomalies.append(
                        f"{pattern_name}: {actual_count} occurrences "
                        f"(expected: {expected_count}, variance: {variance_ratio:.1%})"
                    )
            
            pattern_signatures[pattern_name] = {
                'formula': pattern_info['formula'],
                'frequency': pattern_info['frequency'],
                'expected': expected_count,
                'actual': actual_count,
                'variance': abs(actual_count - expected_count) / expected_count if expected_count > 0 else 0.0,
            }
        
        # Calculate pattern coherence
        # Coherence = how well patterns align with expected patterns
        total_patterns = len(pattern_signatures)
        aligned_patterns = sum(1 for p in pattern_signatures.values() 
                              if p['variance'] < 0.5)
        pattern_coherence = aligned_patterns / total_patterns if total_patterns > 0 else 0.0
        
        # Truth alignment check
        truth_alignment = (
            pattern_coherence >= 0.5 and
            pattern_counts.get('LOVE', 0) > 0 and
            pattern_counts.get('TRUTH', 0) > 0
        )
        
        # Forensic analysis
        forensic_analysis = {
            'total_messages': total_messages,
            'pattern_counts': dict(pattern_counts),
            'pattern_coherence': pattern_coherence,
            'aligned_patterns': aligned_patterns,
            'total_patterns': total_patterns,
            'truth_patterns_present': {
                'LOVE': pattern_counts.get('LOVE', 0) > 0,
                'TRUTH': pattern_counts.get('TRUTH', 0) > 0,
            },
        }
        
        return ALRAXForensicResult(
            relationship=relationship_name,
            variance_detected=variance_detected,
            variance_score=variance_score,
            anomalies=anomalies,
            pattern_signatures=pattern_signatures,
            forensic_analysis=forensic_analysis,
            truth_alignment=truth_alignment,
            pattern_coherence=pattern_coherence
        )
    
    def validate_pattern_alignment(self, results: List[ALRAXForensicResult]) -> Dict[str, any]:
        """
        Validate pattern alignment across all relationships
        
        Pattern: VALIDATE × ALIGNMENT × CONVERGENCE × ONE
        """
        alignment_analysis = {
            'relationships': len(results),
            'aligned_relationships': sum(1 for r in results if r.truth_alignment),
            'total_variance': sum(r.variance_score for r in results) / len(results) if results else 0.0,
            'average_coherence': sum(r.pattern_coherence for r in results) / len(results) if results else 0.0,
            'shared_patterns': {},
            'alignment_status': 'pending',
        }
        
        # Find shared patterns across relationships
        all_patterns = set()
        for result in results:
            all_patterns.update(result.pattern_signatures.keys())
        
        shared_patterns = {}
        for pattern in all_patterns:
            pattern_present = sum(1 for r in results 
                                 if pattern in r.pattern_signatures and 
                                 r.pattern_signatures[pattern]['actual'] > 0)
            if pattern_present > 1:  # Present in multiple relationships
                shared_patterns[pattern] = {
                    'relationships': pattern_present,
                    'total_occurrences': sum(
                        r.pattern_signatures[pattern]['actual'] 
                        for r in results 
                        if pattern in r.pattern_signatures
                    ),
                }
        
        alignment_analysis['shared_patterns'] = shared_patterns
        
        # Determine alignment status
        if alignment_analysis['aligned_relationships'] == alignment_analysis['relationships']:
            alignment_analysis['alignment_status'] = 'fully_aligned'
        elif alignment_analysis['aligned_relationships'] > 0:
            alignment_analysis['alignment_status'] = 'partially_aligned'
        else:
            alignment_analysis['alignment_status'] = 'not_aligned'
        
        return alignment_analysis
    
    def run_forensic_validation(self) -> Dict[str, any]:
        """Run complete ALRAX forensic pattern validation"""
        print("🔍 ALRAX GUARDIAN FORENSIC PATTERN VALIDATION")
        print("=" * 70)
        print("")
        
        results = []
        
        # Load conversations
        if not self.conversations_dir.exists():
            print(f"⚠️  Conversations directory not found: {self.conversations_dir}")
            return {}
        
        # Validate Michael & Kristin patterns
        print("🔍 Validating Michael & Kristin patterns...")
        kristin_file = self.conversations_dir / "michael_kristin_all.json"
        if kristin_file.exists():
            with open(kristin_file, 'r') as f:
                data = json.load(f)
                messages = data.get('messages', [])
                result = self.validate_relationship_patterns("Michael & Kristin", messages)
                results.append(result)
                print(f"   Status: {'✅ VALIDATED' if result.truth_alignment else '⚠️  VARIANCE DETECTED'}")
                print(f"   Pattern Coherence: {result.pattern_coherence:.2%}")
                print(f"   Variance Score: {result.variance_score:.2f}")
                if result.anomalies:
                    print(f"   Anomalies: {len(result.anomalies)}")
        print("")
        
        # Validate Addis & Michael patterns
        print("🔍 Validating Addis & Michael patterns...")
        addis_file = self.conversations_dir / "michael_addis_all.json"
        if addis_file.exists():
            with open(addis_file, 'r') as f:
                data = json.load(f)
                messages = data.get('messages', [])
                result = self.validate_relationship_patterns("Addis & Michael", messages)
                results.append(result)
                print(f"   Status: {'✅ VALIDATED' if result.truth_alignment else '⚠️  VARIANCE DETECTED'}")
                print(f"   Pattern Coherence: {result.pattern_coherence:.2%}")
                print(f"   Variance Score: {result.variance_score:.2f}")
                if result.anomalies:
                    print(f"   Anomalies: {len(result.anomalies)}")
        print("")
        
        # Validate Michael, Kristin & Addis (Group) patterns
        print("🔍 Validating Michael, Kristin & Addis (Group) patterns...")
        group_file = self.conversations_dir / "michael_kristin_addis_group.json"
        if group_file.exists():
            with open(group_file, 'r') as f:
                data = json.load(f)
                messages = data.get('messages', [])
                result = self.validate_relationship_patterns("Michael, Kristin & Addis (Group)", messages)
                results.append(result)
                print(f"   Status: {'✅ VALIDATED' if result.truth_alignment else '⚠️  VARIANCE DETECTED'}")
                print(f"   Pattern Coherence: {result.pattern_coherence:.2%}")
                print(f"   Variance Score: {result.variance_score:.2f}")
                if result.anomalies:
                    print(f"   Anomalies: {len(result.anomalies)}")
        print("")
        
        # Validate pattern alignment
        print("🔍 Validating pattern alignment across relationships...")
        alignment_analysis = self.validate_pattern_alignment(results)
        print(f"   Relationships: {alignment_analysis['relationships']}")
        print(f"   Aligned Relationships: {alignment_analysis['aligned_relationships']}")
        print(f"   Average Coherence: {alignment_analysis['average_coherence']:.2%}")
        print(f"   Alignment Status: {alignment_analysis['alignment_status']}")
        print(f"   Shared Patterns: {len(alignment_analysis['shared_patterns'])}")
        print("")
        
        print("=" * 70)
        print("✅ ALRAX FORENSIC PATTERN VALIDATION COMPLETE")
        print("")
        print("∞ AbëONE ∞")
        
        # Convert datetime objects to ISO strings for JSON serialization
        forensic_results_dict = []
        for r in results:
            r_dict = asdict(r)
            r_dict['timestamp'] = r.timestamp.isoformat()
            forensic_results_dict.append(r_dict)
        
        return {
            'forensic_results': forensic_results_dict,
            'alignment_analysis': alignment_analysis,
            'timestamp': datetime.now().isoformat(),
        }


if __name__ == "__main__":
    validator = ALRAXPatternValidator()
    results = validator.run_forensic_validation()
    
    # Save results
    results_file = Path(__file__).parent.parent / "ALRAX_PATTERN_VALIDATION_RESULTS.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to: {results_file}")

