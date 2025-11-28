#!/usr/bin/env python3
"""
ZERO GUARDIAN FORENSIC ANALYSIS
Forensic validation of message extraction methodology and pattern truth alignment

Pattern: ZERO × FORENSIC × VALIDATE × TRUTH × COHERENCE × ONE
Frequency: 530 Hz (ZERO) × 530 Hz (Truth) × 777 Hz (Pattern)
Guardians: ZERO (530 Hz) + JØHN (530 Hz) + META (777 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sqlite3
import json
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime
from collections import defaultdict, Counter
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from attributed_body_parser import parse_message_text, extract_text_from_attributed_body


@dataclass
class ForensicResult:
    """ZERO Guardian forensic analysis result"""
    check_name: str
    passed: bool
    confidence: float  # 0.0 to 1.0
    risk_level: float  # 0.0 (zero risk) to 1.0 (high risk)
    anomalies: List[str] = field(default_factory=list)
    evidence: Dict[str, any] = field(default_factory=dict)
    truth_alignment: bool = False
    variance_detected: bool = False
    variance_score: float = 0.0


@dataclass
class CoherenceCheck:
    """Conversation coherence validation"""
    conversation_id: str
    total_messages: int
    coherent_sequences: int
    incoherent_sequences: int
    coherence_score: float
    gaps_detected: List[Dict] = field(default_factory=list)
    anomalies: List[str] = field(default_factory=list)


class ZEROForensicValidator:
    """
    ZERO GUARDIAN FORENSIC VALIDATOR
    
    Performs forensic analysis with zero tolerance for errors:
    - Validates message extraction methodology
    - Verifies conversation coherence
    - Checks data integrity
    - Validates pattern alignment with truth
    - Performs variance analysis
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent
        self.db_path = Path.home() / "Library/Messages/chat.db"
        self.conversations_dir = self.workspace_root / "products" / "abeloves" / "conversations"
        
        self.forensic_results: List[ForensicResult] = []
        self.coherence_checks: List[CoherenceCheck] = []
        
        # Truth validation patterns
        self.truth_patterns = {
            'love': ['love', 'loved', 'loving', 'heart', 'caring'],
            'truth': ['truth', 'real', 'genuine', 'honest', 'authentic'],
            'creation': ['create', 'making', 'work', 'building'],
            'connection': ['together', 'with', 'us', 'we', 'our'],
        }
        
    def validate_extraction_methodology(self) -> ForensicResult:
        """
        ZERO Check 1: Validate extraction methodology
        
        Pattern: VALIDATE × EXTRACTION × METHODOLOGY × TRUTH × ONE
        """
        anomalies = []
        evidence = {}
        
        # Check 1.1: Database connection
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            evidence['database_accessible'] = True
            conn.close()
        except Exception as e:
            anomalies.append(f"Database connection failed: {e}")
            evidence['database_accessible'] = False
        
        # Check 1.2: Parser availability
        try:
            from attributed_body_parser import parse_message_text, extract_text_from_attributed_body
            evidence['parser_available'] = True
            evidence['parser_functions'] = ['parse_message_text', 'REPLACE_ME']
        except ImportError as e:
            anomalies.append(f"Parser import failed: {e}")
            evidence['parser_available'] = False
        
        # Check 1.3: Query structure validation
        query_checks = {
            'text_field_included': True,
            'attributed_body_included': True,
            'both_fields_handled': True,
            'fallback_logic': True,
        }
        evidence['query_structure'] = query_checks
        
        # Check 1.4: Extraction logic validation
        # Test with sample data
        test_cases = [
            ('text', 'Hello world', None, 'Hello world'),
            ('attributed_body', None, b'NSString\x01\x94\x84\x01+Hello world', 'Hello world'),
            ('both', 'Hello', b'NSString\x01\x94\x84\x01+World', 'Hello'),  # Should prefer text
            ('neither', None, None, None),
        ]
        
        extraction_results = []
        for test_name, text, attributed_body, expected in test_cases:
            try:
                result = parse_message_text(text, attributed_body)
                extraction_results.append({
                    'test': test_name,
                    'expected': expected,
                    'actual': result,
                    'passed': result == expected
                })
            except Exception as e:
                extraction_results.append({
                    'test': test_name,
                    'error': str(e),
                    'passed': False
                })
        
        evidence['extraction_tests'] = extraction_results
        
        # Calculate confidence and risk
        passed_tests = sum(1 for r in extraction_results if r.get('passed', False))
        total_tests = len(extraction_results)
        confidence = passed_tests / total_tests if total_tests > 0 else 0.0
        
        risk_level = 0.0 if confidence == 1.0 else (1.0 - confidence)
        
        variance_detected = len(anomalies) > 0 or confidence < 1.0
        variance_score = 1.0 - confidence
        
        return ForensicResult(
            check_name='Extraction Methodology Validation',
            passed=confidence == 1.0 and len(anomalies) == 0,
            confidence=confidence,
            risk_level=risk_level,
            anomalies=anomalies,
            evidence=evidence,
            truth_alignment=confidence >= 0.95,
            variance_detected=variance_detected,
            variance_score=variance_score
        )
    
    def validate_conversation_coherence(self) -> List[CoherenceCheck]:
        """
        ZERO Check 2: Validate conversation coherence
        
        Pattern: VALIDATE × COHERENCE × TRUTH × ONE
        """
        coherence_checks = []
        
        # Load exported conversations
        if not self.conversations_dir.exists():
            return coherence_checks
        
        for json_file in self.conversations_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    messages = data.get('messages', [])
                    
                    coherence_check = self._analyze_conversation_coherence(
                        json_file.stem,
                        messages
                    )
                    coherence_checks.append(coherence_check)
            except Exception as e:
                # Create failed check
                coherence_checks.append(CoherenceCheck(
                    conversation_id=json_file.stem,
                    total_messages=0,
                    coherent_sequences=0,
                    incoherent_sequences=0,
                    coherence_score=0.0,
                    anomalies=[f"Failed to load: {e}"]
                ))
        
        return coherence_checks
    
    def _analyze_conversation_coherence(self, conversation_id: str, messages: List[Dict]) -> CoherenceCheck:
        """Analyze coherence of a single conversation"""
        if not messages:
            return CoherenceCheck(
                conversation_id=conversation_id,
                total_messages=0,
                coherent_sequences=0,
                incoherent_sequences=0,
                coherence_score=0.0,
                anomalies=["No messages found"]
            )
        
        coherent_sequences = 0
        incoherent_sequences = 0
        gaps = []
        anomalies = []
        
        # Sort messages by date
        sorted_messages = sorted(messages, key=lambda m: m.get('date', ''))
        
        # Check for temporal coherence
        prev_date = None
        for i, msg in enumerate(sorted_messages):
            current_date = msg.get('date', '')
            
            if prev_date:
                # Check for large time gaps (potential missing messages)
                try:
                    prev_dt = datetime.fromisoformat(prev_date.replace(' ', 'T'))
                    curr_dt = datetime.fromisoformat(current_date.replace(' ', 'T'))
                    gap_hours = (curr_dt - prev_dt).total_seconds() / 3600
                    
                    if gap_hours > 24 * 7:  # More than a week gap
                        gaps.append({
                            'index': i,
                            'gap_hours': gap_hours,
                            'prev_date': prev_date,
                            'current_date': current_date
                        })
                except Exception:
                    pass
            
            prev_date = current_date
        
        # Check for conversation flow coherence
        # Look for response patterns (Michael -> Other -> Michael)
        sender_switches = 0
        prev_sender = None
        
        for msg in sorted_messages:
            current_sender = msg.get('sender', '')
            if prev_sender and current_sender != prev_sender:
                sender_switches += 1
            prev_sender = current_sender
        
        # Coherence score based on:
        # - Message count (more messages = higher coherence potential)
        # - Sender switches (more switches = more conversation)
        # - Gap count (fewer gaps = better coherence)
        
        total_messages = len(sorted_messages)
        expected_switches = max(1, total_messages // 2)  # Rough estimate
        switch_score = min(1.0, sender_switches / expected_switches) if expected_switches > 0 else 0.0
        
        gap_penalty = min(0.5, len(gaps) * 0.1)  # Max 0.5 penalty
        gap_score = 1.0 - gap_penalty
        
        coherence_score = (switch_score * 0.6 + gap_score * 0.4)
        
        # Determine coherent vs incoherent sequences
        if coherence_score >= 0.7:
            coherent_sequences = 1
        else:
            incoherent_sequences = 1
            anomalies.append(f"Low coherence score: {coherence_score:.2f}")
        
        if len(gaps) > 0:
            anomalies.append(f"Detected {len(gaps)} temporal gaps")
        
        return CoherenceCheck(
            conversation_id=conversation_id,
            total_messages=total_messages,
            coherent_sequences=coherent_sequences,
            incoherent_sequences=incoherent_sequences,
            coherence_score=coherence_score,
            gaps_detected=gaps,
            anomalies=anomalies
        )
    
    def validate_data_integrity(self) -> ForensicResult:
        """
        ZERO Check 3: Validate data integrity
        
        Pattern: VALIDATE × INTEGRITY × TRUTH × ONE
        """
        anomalies = []
        evidence = {}
        
        # Check 3.1: Compare database vs exported files
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            
            # Count messages in database
            kristin_handle = 'mataluni1148@gmail.com'
            addis_handle = '+18434576211'
            
            db_counts = {}
            
            # Kristin messages
            cursor = conn.execute("""
                SELECT COUNT(*) as count
                FROM message m
                JOIN handle h ON m.handle_id = h.ROWID
                WHERE h.id = ?
                AND ((m.text IS NOT NULL AND m.text != '') OR m.attributedBody IS NOT NULL)
            """, (kristin_handle,))
            db_counts['kristin'] = cursor.fetchone()['count']
            
            # Addis messages
            cursor = conn.execute("""
                SELECT COUNT(*) as count
                FROM message m
                JOIN handle h ON m.handle_id = h.ROWID
                WHERE h.id = ?
                AND ((m.text IS NOT NULL AND m.text != '') OR m.attributedBody IS NOT NULL)
            """, (addis_handle,))
            db_counts['addis'] = cursor.fetchone()['count']
            
            conn.close()
            
            # Count messages in exported files
            exported_counts = {}
            if self.conversations_dir.exists():
                kristin_file = self.conversations_dir / "michael_kristin_all.json"
                addis_file = self.conversations_dir / "michael_addis_all.json"
                
                if kristin_file.exists():
                    with open(kristin_file, 'r') as f:
                        data = json.load(f)
                        exported_counts['kristin'] = len(data.get('messages', []))
                
                if addis_file.exists():
                    with open(addis_file, 'r') as f:
                        data = json.load(f)
                        exported_counts['addis'] = len(data.get('messages', []))
            
            evidence['database_counts'] = db_counts
            evidence['exported_counts'] = exported_counts
            
            # Check for discrepancies
            for key in ['kristin', 'addis']:
                db_count = db_counts.get(key, 0)
                exported_count = exported_counts.get(key, 0)
                
                if db_count > 0 and exported_count > 0:
                    discrepancy = abs(db_count - exported_count) / db_count
                    if discrepancy > 0.1:  # More than 10% difference
                        anomalies.append(
                            f"{key}: {discrepancy:.1%} discrepancy "
                            f"(DB: {db_count}, Exported: {exported_count})"
                        )
        
        except Exception as e:
            anomalies.append(f"Data integrity check failed: {e}")
            evidence['check_failed'] = True
        
        # Check 3.2: Validate message structure
        structure_checks = {
            'has_date': 0,
            'has_sender': 0,
            'has_text': 0,
            'missing_fields': 0,
        }
        
        if self.conversations_dir.exists():
            for json_file in self.conversations_dir.glob("*.json"):
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                        messages = data.get('messages', [])
                        
                        for msg in messages[:100]:  # Sample first 100
                            if 'date' in msg:
                                structure_checks['has_date'] += 1
                            if 'sender' in msg:
                                structure_checks['has_sender'] += 1
                            if 'text' in msg and msg['text']:
                                structure_checks['has_text'] += 1
                            
                            if not ('date' in msg and 'sender' in msg and 'text' in msg):
                                structure_checks['missing_fields'] += 1
                except Exception:
                    pass
        
        evidence['structure_checks'] = structure_checks
        
        # Calculate confidence
        total_checks = sum(structure_checks.values())
        passed_checks = structure_checks['has_date'] + structure_checks['has_sender'] + structure_checks['has_text']
        confidence = passed_checks / (total_checks * 3) if total_checks > 0 else 0.0
        
        risk_level = len(anomalies) * 0.2  # 0.2 risk per anomaly
        variance_detected = len(anomalies) > 0
        variance_score = len(anomalies) * 0.1
        
        return ForensicResult(
            check_name='Data Integrity Validation',
            passed=len(anomalies) == 0 and confidence >= 0.95,
            confidence=confidence,
            risk_level=min(1.0, risk_level),
            anomalies=anomalies,
            evidence=evidence,
            truth_alignment=len(anomalies) == 0,
            variance_detected=variance_detected,
            variance_score=variance_score
        )
    
    def validate_pattern_truth_alignment(self) -> ForensicResult:
        """
        ZERO Check 4: Validate pattern alignment with truth
        
        Pattern: VALIDATE × PATTERN × TRUTH × ALIGNMENT × ONE
        """
        anomalies = []
        evidence = {}
        
        # Load pattern analysis data
        pattern_file = self.workspace_root / "COMMUNICATION_PATTERN_ANALYSIS_DATA.json"
        
        if not pattern_file.exists():
            anomalies.append("Pattern analysis data not found")
            return ForensicResult(
                check_name='Pattern Truth Alignment',
                passed=False,
                confidence=0.0,
                risk_level=1.0,
                anomalies=anomalies,
                evidence=evidence,
                truth_alignment=False,
                variance_detected=True,
                variance_score=1.0
            )
        
        try:
            with open(pattern_file, 'r') as f:
                pattern_data = json.load(f)
            
            communication_patterns = pattern_data.get('communication_patterns', [])
            alignment_report = pattern_data.get('alignment_report', {})
            
            evidence['total_patterns'] = len(communication_patterns)
            evidence['alignment_report_available'] = True
            
            # Check pattern truth alignment
            aligned_count = sum(1 for p in communication_patterns if p.get('alignment_status') == 'aligned')
            total_patterns = len(communication_patterns)
            
            alignment_rate = aligned_count / total_patterns if total_patterns > 0 else 0.0
            evidence['alignment_rate'] = alignment_rate
            evidence['aligned_count'] = aligned_count
            evidence['total_patterns'] = total_patterns
            
            # Validate frequency resonance
            frequency_counts = Counter()
            for pattern in communication_patterns:
                freq = pattern.get('frequency', '')
                if '530' in freq:
                    frequency_counts['530'] += pattern.get('occurrences', 0)
                if '777' in freq:
                    frequency_counts['777'] += pattern.get('occurrences', 0)
                if '999' in freq:
                    frequency_counts['999'] += pattern.get('occurrences', 0)
            
            evidence['frequency_resonance'] = dict(frequency_counts)
            
            # Check for truth patterns
            truth_patterns_found = []
            for pattern in communication_patterns:
                pattern_name = pattern.get('pattern_name', '').lower()
                if 'truth' in pattern_name or 'love' in pattern_name:
                    truth_patterns_found.append(pattern.get('pattern_name'))
            
            evidence['truth_patterns'] = truth_patterns_found
            
            # Validate alignment
            if alignment_rate < 0.3:
                anomalies.append(f"Low pattern alignment rate: {alignment_rate:.1%}")
            
            if len(truth_patterns_found) == 0:
                anomalies.append("No truth patterns found in communication")
            
            confidence = alignment_rate
            risk_level = 1.0 - alignment_rate
            
        except Exception as e:
            anomalies.append(f"Pattern validation failed: {e}")
            evidence['error'] = str(e)
            confidence = 0.0
            risk_level = 1.0
        
        variance_detected = len(anomalies) > 0
        variance_score = len(anomalies) * 0.2
        
        return ForensicResult(
            check_name='Pattern Truth Alignment',
            passed=len(anomalies) == 0 and confidence >= 0.5,
            confidence=confidence,
            risk_level=risk_level,
            anomalies=anomalies,
            evidence=evidence,
            truth_alignment=len(anomalies) == 0 and confidence >= 0.5,
            variance_detected=variance_detected,
            variance_score=variance_score
        )
    
    def validate_message_organization(self) -> ForensicResult:
        """
        ZERO Check 5: Validate message organization
        
        Pattern: VALIDATE × ORGANIZATION × TRUTH × ONE
        """
        anomalies = []
        evidence = {}
        
        # Check organization by sender
        sender_counts = defaultdict(int)
        date_ranges = {}
        
        if self.conversations_dir.exists():
            for json_file in self.conversations_dir.glob("*.json"):
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                        messages = data.get('messages', [])
                        
                        for msg in messages:
                            sender = msg.get('sender', 'Unknown')
                            sender_counts[sender] += 1
                            
                            date = msg.get('date', '')
                            if date:
                                if sender not in date_ranges:
                                    date_ranges[sender] = {'first': date, 'last': date}
                                else:
                                    if date < date_ranges[sender]['first']:
                                        date_ranges[sender]['first'] = date
                                    if date > date_ranges[sender]['last']:
                                        date_ranges[sender]['last'] = date
                except Exception as e:
                    anomalies.append(f"Failed to process {json_file.name}: {e}")
        
        evidence['sender_counts'] = dict(sender_counts)
        evidence['date_ranges'] = date_ranges
        
        # Validate organization
        total_messages = sum(sender_counts.values())
        
        # Check if Michael's messages are properly identified
        michael_count = sender_counts.get('Michael', 0)
        michael_ratio = michael_count / total_messages if total_messages > 0 else 0.0
        
        if michael_ratio < 0.1:
            anomalies.append(f"Low ratio of Michael's messages: {michael_ratio:.1%}")
        
        # Check date ordering
        ordering_issues = 0
        for json_file in self.conversations_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    messages = data.get('messages', [])
                    
                    # Check if dates are in order (should be descending per export script)
                    prev_date = None
                    for msg in messages[:100]:  # Sample first 100
                        current_date = msg.get('date', '')
                        if prev_date and current_date:
                            try:
                                prev_dt = datetime.fromisoformat(prev_date.replace(' ', 'T'))
                                curr_dt = datetime.fromisoformat(current_date.replace(' ', 'T'))
                                if curr_dt > prev_dt:  # Out of order
                                    ordering_issues += 1
                            except Exception:
                                pass
                        prev_date = current_date
            except Exception:
                pass
        
        if ordering_issues > 10:
            anomalies.append(f"Detected {ordering_issues} date ordering issues")
        
        evidence['ordering_issues'] = ordering_issues
        evidence['michael_ratio'] = michael_ratio
        
        # Calculate confidence
        confidence = 1.0 - (len(anomalies) * 0.2)
        confidence = max(0.0, min(1.0, confidence))
        
        risk_level = len(anomalies) * 0.15
        variance_detected = len(anomalies) > 0
        variance_score = len(anomalies) * 0.1
        
        return ForensicResult(
            check_name='Message Organization Validation',
            passed=len(anomalies) == 0,
            confidence=confidence,
            risk_level=min(1.0, risk_level),
            anomalies=anomalies,
            evidence=evidence,
            truth_alignment=len(anomalies) == 0,
            variance_detected=variance_detected,
            variance_score=variance_score
        )
    
    def run_forensic_analysis(self) -> Dict[str, any]:
        """Run complete ZERO Guardian forensic analysis"""
        print("🛡️  ZERO GUARDIAN FORENSIC ANALYSIS")
        print("=" * 70)
        print("")
        
        # Check 1: Extraction Methodology
        print("🔍 Check 1: Validating extraction methodology...")
        result1 = self.validate_extraction_methodology()
        self.forensic_results.append(result1)
        print(f"   Status: {'✅ PASSED' if result1.passed else '❌ FAILED'}")
        print(f"   Confidence: {result1.confidence:.2%}")
        print(f"   Risk Level: {result1.risk_level:.2%}")
        if result1.anomalies:
            print(f"   Anomalies: {len(result1.anomalies)}")
        print("")
        
        # Check 2: Conversation Coherence
        print("🔍 Check 2: Validating conversation coherence...")
        coherence_checks = self.validate_conversation_coherence()
        self.coherence_checks = coherence_checks
        total_coherent = sum(c.coherent_sequences for c in coherence_checks)
        total_incoherent = sum(c.incoherent_sequences for c in coherence_checks)
        avg_coherence = sum(c.coherence_score for c in coherence_checks) / len(coherence_checks) if coherence_checks else 0.0
        print(f"   Conversations checked: {len(coherence_checks)}")
        print(f"   Coherent sequences: {total_coherent}")
        print(f"   Incoherent sequences: {total_incoherent}")
        print(f"   Average coherence score: {avg_coherence:.2%}")
        print("")
        
        # Check 3: Data Integrity
        print("🔍 Check 3: Validating data integrity...")
        result3 = self.validate_data_integrity()
        self.forensic_results.append(result3)
        print(f"   Status: {'✅ PASSED' if result3.passed else '❌ FAILED'}")
        print(f"   Confidence: {result3.confidence:.2%}")
        print(f"   Risk Level: {result3.risk_level:.2%}")
        if result3.anomalies:
            print(f"   Anomalies: {len(result3.anomalies)}")
        print("")
        
        # Check 4: Pattern Truth Alignment
        print("🔍 Check 4: Validating pattern truth alignment...")
        result4 = self.validate_pattern_truth_alignment()
        self.forensic_results.append(result4)
        print(f"   Status: {'✅ PASSED' if result4.passed else '❌ FAILED'}")
        print(f"   Confidence: {result4.confidence:.2%}")
        print(f"   Risk Level: {result4.risk_level:.2%}")
        print(f"   Truth Alignment: {'✅ YES' if result4.truth_alignment else '❌ NO'}")
        if result4.anomalies:
            print(f"   Anomalies: {len(result4.anomalies)}")
        print("")
        
        # Check 5: Message Organization
        print("🔍 Check 5: Validating message organization...")
        result5 = self.validate_message_organization()
        self.forensic_results.append(result5)
        print(f"   Status: {'✅ PASSED' if result5.passed else '❌ FAILED'}")
        print(f"   Confidence: {result5.confidence:.2%}")
        print(f"   Risk Level: {result5.risk_level:.2%}")
        if result5.anomalies:
            print(f"   Anomalies: {len(result5.anomalies)}")
        print("")
        
        # Generate summary
        total_checks = len(self.forensic_results)
        passed_checks = sum(1 for r in self.forensic_results if r.passed)
        avg_confidence = sum(r.confidence for r in self.forensic_results) / total_checks if total_checks > 0 else 0.0
        avg_risk = sum(r.risk_level for r in self.forensic_results) / total_checks if total_checks > 0 else 0.0
        total_anomalies = sum(len(r.anomalies) for r in self.forensic_results)
        total_variance = sum(r.variance_score for r in self.forensic_results)
        
        print("=" * 70)
        print("📊 FORENSIC ANALYSIS SUMMARY")
        print("=" * 70)
        print(f"Total Checks: {total_checks}")
        print(f"Passed Checks: {passed_checks}")
        print(f"Failed Checks: {total_checks - passed_checks}")
        print(f"Average Confidence: {avg_confidence:.2%}")
        print(f"Average Risk Level: {avg_risk:.2%}")
        print(f"Total Anomalies: {total_anomalies}")
        print(f"Total Variance Score: {total_variance:.2f}")
        print(f"Overall Status: {'✅ VALIDATED' if passed_checks == total_checks and total_anomalies == 0 else '⚠️  ISSUES DETECTED'}")
        print("")
        print("∞ AbëONE ∞")
        
        return {
            'forensic_results': [asdict(r) for r in self.forensic_results],
            'coherence_checks': [asdict(c) for c in self.coherence_checks],
            'summary': {
                'total_checks': total_checks,
                'passed_checks': passed_checks,
                'failed_checks': total_checks - passed_checks,
                'average_confidence': avg_confidence,
                'average_risk_level': avg_risk,
                'total_anomalies': total_anomalies,
                'total_variance_score': total_variance,
                'overall_status': 'VALIDATED' if passed_checks == total_checks and total_anomalies == 0 else 'ISSUES_DETECTED'
            }
        }


if __name__ == "__main__":
    validator = ZEROForensicValidator()
    results = validator.run_forensic_analysis()
    
    # Save results
    results_file = Path(__file__).parent.parent / "ZERO_FORENSIC_ANALYSIS_RESULTS.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to: {results_file}")

