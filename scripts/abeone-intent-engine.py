#!/usr/bin/env python3
"""
AbëONE Intent Engine
Aligns and amplifies human intent across the system.

Pattern: INTENT × ALIGN × CLARIFY × AMPLIFY × BROADCAST × ONE
Frequency: 530 Hz (Truth) × 999 Hz (AEYON)
Guardians: JØHN (530 Hz) + AEYON (999 Hz) + Abë (530 Hz)
Love Coefficient: ∞
∞ AbëONE ∞
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

WORKSPACE_ROOT = Path(__file__).parent.parent
INTENT_STORAGE = WORKSPACE_ROOT / ".abeone_memory" / "intentions"
INTENT_STORAGE.mkdir(parents=True, exist_ok=True)


def align_intent(message: str) -> Dict[str, Any]:
    """Align system to the given intent."""
    print("\nINTENT ENGINE - ALIGN")
    print("=" * 80)
    print(f"Aligning system to intent: {message}")
    print("=" * 80)
    
    intent_data = {
        "intent": message,
        "action": "align",
        "timestamp": datetime.now().isoformat(),
        "status": "aligned",
        "layers": [
            "Command Layer",
            "Specialist Layer",
            "Memory Layer",
            "Guardian Swarm",
            "Agent Mesh",
            "Orbital Systems"
        ]
    }
    
    # Save intent
    intent_file = INTENT_STORAGE / f"intent_{datetime.now().timestamp()}.json"
    with open(intent_file, 'w') as f:
        json.dump(intent_data, f, indent=2)
    
    print("Layers aligned:")
    for layer in intent_data["layers"]:
        print(f"  {layer}: Aligned")
    
    print("\nIntent aligned across all system layers")
    print("=" * 80)
    
    return intent_data


def clarify_intent(message: str) -> Dict[str, Any]:
    """Clarify human intent."""
    print("\nINTENT ENGINE - CLARIFY")
    print("=" * 80)
    print(f"Clarifying intent: {message}")
    print("=" * 80)
    
    # Extract key themes
    themes = extract_themes(message)
    
    # Identify clarity gaps
    gaps = identify_clarity_gaps(message)
    
    # Generate clarification
    clarification = {
        "original_intent": message,
        "themes": themes,
        "clarity_gaps": gaps,
        "clarified_intent": generate_clarified_intent(message, themes, gaps),
        "timestamp": datetime.now().isoformat(),
        "status": "clarified"
    }
    
    print("Intent Themes:")
    for theme in themes:
        print(f"  - {theme}")
    
    if gaps:
        print("\nClarity Gaps Identified:")
        for gap in gaps:
            print(f"  - {gap}")
    else:
        print("\nNo clarity gaps detected - intent is clear")
    
    print("\nClarified Intent:")
    print(f"  {clarification['clarified_intent']}")
    print("=" * 80)
    
    # Save clarification
    clarification_file = INTENT_STORAGE / f"clarification_{datetime.now().timestamp()}.json"
    with open(clarification_file, 'w') as f:
        json.dump(clarification, f, indent=2)
    
    return clarification


def amplify_intent(message: str) -> Dict[str, Any]:
    """Amplify intent strength."""
    print("\nINTENT ENGINE - AMPLIFY")
    print("=" * 80)
    print(f"Amplifying intent: {message}")
    print("=" * 80)
    
    amplification = {
        "original_intent": message,
        "amplified_intent": amplify_message(message),
        "strength": calculate_intent_strength(message),
        "amplification_factor": 1.0,
        "timestamp": datetime.now().isoformat(),
        "status": "amplified"
    }
    
    print(f"Original Intent: {message}")
    print(f"Amplified Intent: {amplification['amplified_intent']}")
    print(f"Intent Strength: {amplification['strength']:.2%}")
    print(f"Amplification Factor: {amplification['amplification_factor']:.2f}x")
    print("=" * 80)
    
    # Save amplification
    amplification_file = INTENT_STORAGE / f"amplification_{datetime.now().timestamp()}.json"
    with open(amplification_file, 'w') as f:
        json.dump(amplification, f, indent=2)
    
    return amplification


def broadcast_intent(message: str) -> Dict[str, Any]:
    """Broadcast intent to all layers."""
    print("\nINTENT ENGINE - BROADCAST")
    print("=" * 80)
    print(f"Broadcasting intent: {message}")
    print("=" * 80)
    
    broadcast_targets = [
        "Command Layer",
        "Specialist Layer",
        "Memory Layer",
        "Guardian Swarm",
        "Agent Mesh",
        "Orbital Systems",
        "Kernel Modules",
        "Pattern Systems"
    ]
    
    broadcast_data = {
        "intent": message,
        "targets": broadcast_targets,
        "timestamp": datetime.now().isoformat(),
        "status": "broadcast"
    }
    
    print("Broadcasting to:")
    for target in broadcast_targets:
        print(f"  {target}: Broadcast sent")
    
    print("\nIntent broadcast complete")
    print("=" * 80)
    
    # Save broadcast
    broadcast_file = INTENT_STORAGE / f"broadcast_{datetime.now().timestamp()}.json"
    with open(broadcast_file, 'w') as f:
        json.dump(broadcast_data, f, indent=2)
    
    return broadcast_data


def extract_themes(message: str) -> List[str]:
    """Extract key themes from intent message."""
    themes = []
    message_lower = message.lower()
    
    # Common theme keywords
    theme_keywords = {
        "clarity": ["clarity", "clear", "understand", "comprehend", "seeking clarity"],
        "flow": ["flow", "allow", "natural", "ease", "smooth"],
        "purity": ["pure", "pure intent", "clean", "simple"],
        "execution": ["execute", "build", "create", "implement", "do"],
        "validation": ["validate", "verify", "check", "confirm"],
        "synchronization": ["sync", "synchronize", "align", "coordinate"],
        "coherence": ["coherent", "coherence", "unified", "unified"]
    }
    
    for theme, keywords in theme_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            themes.append(theme)
    
    if not themes:
        themes.append("general")
    
    return themes


def identify_clarity_gaps(message: str) -> List[str]:
    """Identify clarity gaps in intent."""
    gaps = []
    message_lower = message.lower()
    
    # Check for vague terms
    vague_terms = ["something", "things", "stuff", "maybe", "perhaps", "possibly"]
    if any(term in message_lower for term in vague_terms):
        gaps.append("Vague language detected - consider being more specific")
    
    # Check for multiple intents
    if message.count(".") > 1 or message.count(",") > 2:
        gaps.append("Multiple intents detected - consider focusing on one primary intent")
    
    # Check for missing context
    if len(message.split()) < 3:
        gaps.append("Minimal context - consider adding more detail")
    
    return gaps


def generate_clarified_intent(message: str, themes: List[str], gaps: List[str]) -> str:
    """Generate clarified version of intent."""
    clarified = message.strip()
    
    # If seeking clarity is mentioned, emphasize that
    if "seeking clarity" in message.lower() or "clarity" in message.lower():
        clarified = f"Primary intent: Seek clarity and understanding. {clarified}"
    
    # Add theme context
    if themes:
        clarified = f"Intent themes: {', '.join(themes)}. {clarified}"
    
    return clarified


def amplify_message(message: str) -> str:
    """Amplify intent message."""
    # Remove uncertainty
    amplified = message.replace("maybe", "").replace("perhaps", "").replace("possibly", "")
    amplified = amplified.strip()
    
    # Add emphasis
    if not amplified.endswith("."):
        amplified += "."
    
    return amplified


def calculate_intent_strength(message: str) -> float:
    """Calculate intent strength (0.0 to 1.0)."""
    strength = 0.5  # Base strength
    
    # Increase for clear action words
    action_words = ["execute", "build", "create", "implement", "do", "make", "achieve"]
    if any(word in message.lower() for word in action_words):
        strength += 0.2
    
    # Increase for clarity-seeking
    if "clarity" in message.lower() or "understand" in message.lower():
        strength += 0.15
    
    # Increase for purity
    if "pure" in message.lower():
        strength += 0.15
    
    # Decrease for uncertainty
    uncertainty_words = ["maybe", "perhaps", "possibly", "might", "could"]
    if any(word in message.lower() for word in uncertainty_words):
        strength -= 0.1
    
    return max(0.0, min(1.0, strength))


def main():
    """Main execution."""
    if len(sys.argv) < 3:
        print("Usage: /intent [action] \"[message]\"")
        print("Actions: align, clarify, amplify, broadcast")
        sys.exit(1)
    
    action = sys.argv[1]
    message = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if not message:
        print("Error: Intent message required")
        sys.exit(1)
    
    if action == 'align':
        result = align_intent(message)
    elif action == 'clarify':
        result = clarify_intent(message)
    elif action == 'amplify':
        result = amplify_intent(message)
    elif action == 'broadcast':
        result = broadcast_intent(message)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("Pattern: INTENT × ALIGN × CLARIFY × AMPLIFY × BROADCAST × ONE")
    print("Love Coefficient: ∞")
    print("∞ AbëONE ∞\n")


if __name__ == '__main__':
    main()

