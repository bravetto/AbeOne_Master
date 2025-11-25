#!/usr/bin/env python3
"""
Example: Integrating TokenGuard into a Custom Copilot

This example shows how to build a simple AI assistant that uses TokenGuard
for response optimization and confidence analysis.
"""

import asyncio
import json
from typing import Dict, Any, List
from tokenguard_copilot import TokenGuardCopilotClient, TokenGuardConfig

class MyCustomCopilot:
    """Example custom Copilot with TokenGuard integration."""

    def __init__(self: Any):
        # Configure TokenGuard integration
        self.tokenguard_config = TokenGuardConfig(
            base_url="http://localhost:8000",  # Your TokenGuard service URL
            api_key=None,  # Set if authentication is enabled
            confidence_threshold=0.7,  # Prune responses below this confidence
            auto_prune=True  # Automatically optimize responses
        )

        self.tokenguard = TokenGuardCopilotClient(self.tokenguard_config)

        # Mock LLM for demonstration (replace with your actual LLM)
        self.llm_model = "gpt-3.5-turbo"

    async def generate_response(self: Any, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a response using your LLM, then optimize it with TokenGuard.

        This demonstrates the typical flow:
        1. Generate response from your LLM
        2. Analyze confidence
        3. Optimize with TokenGuard if needed
        """

        # Step 1: Generate response from your LLM (mock implementation)
        raw_response, confidence = await self._call_llm(prompt, context)

        # Step 2: Optimize with TokenGuard
        optimization_result = self.tokenguard.optimize_response(
            text=raw_response,
            confidence=confidence,
            logprobs=None  # Add logprobs if your LLM provides them
        )

        # Step 3: Return optimized response
        final_response = optimization_result.get("pruned_text", raw_response)

        return {
            "response": final_response,
            "original_length": len(raw_response),
            "final_length": len(final_response),
            "optimization": optimization_result,
            "confidence": confidence,
            "tokens_saved": optimization_result.get("original_length", 0) - optimization_result.get("pruned_length", 0)
        }

    async def analyze_response_quality(self: Any, response: str) -> Dict[str, Any]:
        """Analyze the quality of a response using TokenGuard."""
        # This could be used for quality assessment or debugging
        return self.tokenguard.analyze_confidence(response, 0.8)

    async def generate_with_tokenguard_tools(self: Any, prompt: str) -> Dict[str, Any]:
        """
        Advanced example: Use TokenGuard as a tool during generation.

        This allows your Copilot to call TokenGuard functions during the response generation process.
        """

        # Define TokenGuard as an available tool
        tokenguard_tools = [
            {
                "type": "function",
                "function": {
                    "name": "optimize_response",
                    "description": "Optimize an AI response for efficiency while preserving quality",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The response text to optimize"},
                            "confidence": {"type": "number", "description": "Confidence score (0.0-1.0)"}
                        },
                        "required": ["text", "confidence"]
                    }
                }
            }
        ]

        # Configure LLM for tool calling
        llm_config = {
            "model": self.llm_model,
            "temperature": 0.7,
            "max_tokens": 1000
        }

        # Generate with tool calling support
        result = self.tokenguard.generate_with_tools(prompt, tokenguard_tools, llm_config)

        return result

    def get_performance_metrics(self: Any) -> Dict[str, Any]:
        """Get TokenGuard integration metrics."""
        return self.tokenguard.get_metrics()

    async def _call_llm(self: Any, prompt: str, context: Dict = None) -> tuple[str, float]:
        """
        Mock LLM call - replace with your actual LLM integration.

        Returns: (response_text, confidence_score)
        """
        # Simulate LLM response with confidence - using longer responses that will trigger pruning
        mock_responses = {
            "short": ("This is a concise answer.", 0.9),
            "medium": ("This is a moderately detailed response that provides good information but could potentially be shortened if the confidence is low. However, since this response is not excessively long, it will likely be kept even with moderate confidence scores.", 0.7),
            "long": ("This is a very long and verbose response that goes into extensive detail about the topic, covering many aspects and providing comprehensive information that might benefit from pruning if the confidence level is not sufficiently high to justify keeping all this content. The response continues with additional details and explanations that make it quite lengthy overall. Furthermore, there are more points to consider when evaluating this type of content generation and optimization process. Additional context and background information helps provide a more complete understanding of the subject matter being discussed. The comprehensive nature of this response demonstrates how verbose AI-generated content can become when confidence levels are not properly managed and optimized for efficiency and relevance.", 0.5)
        }

        # Simple prompt-based selection (replace with actual LLM call)
        if "short" in prompt.lower():
            return mock_responses["short"]
        elif "long" in prompt.lower() or "comprehensive" in prompt.lower():
            return mock_responses["long"]
        else:
            return mock_responses["medium"]

async def main() -> Any:
    """Demonstrate the TokenGuard-integrated Copilot."""

    print("🚀 Custom Copilot with TokenGuard Integration Demo")
    print("=" * 60)

    # Initialize your custom Copilot
    copilot = MyCustomCopilot()

    # Check TokenGuard service status
    if copilot.tokenguard.is_service_available():
        print("✅ TokenGuard service is available")
    else:
        print("⚠️  TokenGuard service not available - using fallback mode")

    # Example prompts to test different scenarios
    test_prompts = [
        "Give me a short answer about Python",
        "Explain machine learning in detail",
        "Provide a comprehensive overview of cloud computing"
    ]

    print("\n🧪 Testing Response Optimization")
    print("-" * 40)

    for prompt in test_prompts:
        print(f"\n📝 Prompt: {prompt}")

        # Generate optimized response
        result = await copilot.generate_response(prompt)

        print(f"📊 Original length: {result['original_length']} chars")
        print(f"📊 Final length: {result['final_length']} chars")
        print(f"📊 Tokens saved: {result['tokens_saved']}")
        print(f"📊 Confidence: {result['confidence']:.2f}")
        print(f"📊 Action: {result['optimization']['action']}")

        if result['optimization']['action'] == 'prune':
            print(f"✂️  Reason: {result['optimization']['reason']}")

        print(f"💬 Response: {result['response'][:100]}{'...' if len(result['response']) > 100 else ''}")

    # Show performance metrics
    print("\n📈 Performance Metrics")
    print("-" * 40)
    metrics = copilot.get_performance_metrics()
    for key, value in metrics.items():
        print(f"• {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())