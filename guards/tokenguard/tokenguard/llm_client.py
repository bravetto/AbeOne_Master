"""
LLM Client for interacting with language model providers.
"""
import os
import logging
import httpx
from typing import Dict, Any, Iterator, Optional, List, AsyncGenerator

logger = logging.getLogger(__name__)

from .config import config

class LLMClient:
    """A client for interacting with LLM providers, starting with OpenAI."""

    def __init__(self: Any):
        """
        Initializes the LLM client using settings from the global config.
        """
        self.api_key = config.llm_api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("LLM API key not found. Set TOKENGUARD_LLM_API_KEY or OPENAI_API_KEY.")
            raise ValueError("LLM API key is required but was not found.")
        self.base_url = config.llm_base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _prepare_payload(self: Any, prompt: str, llm_config: Dict[str, Any], stream: bool, tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Prepares the payload for the OpenAI API request."""
        payload = {
            "model": llm_config.get("model", "gpt-4"),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": llm_config.get("max_tokens", 4096),
            "stream": stream,
            "logprobs": True,
            "top_logprobs": 5,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"  # Let the model decide when to use tools

        return payload

    def generate_stream(self: Any, prompt: str, llm_config: Dict[str, Any], tools: Optional[List[Dict[str, Any]]] = None) -> Iterator[Dict[str, Any]]:
        """
        Generates a response from the LLM using streaming.

        Args:
            prompt: The prompt to send to the LLM.
            llm_config: Configuration for the LLM.

        Yields:
            A dictionary representing each chunk of the streaming response.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
        """
        payload = self._prepare_payload(prompt, llm_config, stream=True, tools=tools)

        with httpx.stream("POST", f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=60) as response:
            response.raise_for_status()
            logger.info(f"Successfully initiated streaming connection to {llm_config.get('model')}.")
            for line in response.iter_lines():
                if line.startswith("data: "):
                    line = line[6:]
                    if line.strip() == "[DONE]":
                        logger.info("Streaming generation complete.")
                        break
                    try:
                        import json
                        chunk = json.loads(line)
                        yield chunk
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to decode stream chunk: {line}")
                        continue

    async def agenerate_stream(self: Any, prompt: str, llm_config: Dict[str, Any], tools: Optional[List[Dict[str, Any]]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Asynchronously generates a response from the LLM using streaming.

        Args:
            prompt: The prompt to send to the LLM.
            llm_config: Configuration for the LLM.

        Yields:
            A dictionary representing each chunk of the streaming response.

        Raises:
            httpx.HTTPStatusError: If the API returns an error.
        """
        payload = self._prepare_payload(prompt, llm_config, stream=True, tools=tools)

        async with httpx.AsyncClient() as client:
            async with client.stream("POST", f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=60) as response:
                response.raise_for_status()
                logger.info(f"Successfully initiated async streaming connection to {llm_config.get('model')}.")
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        line = line[6:]
                        if line.strip() == "[DONE]":
                            logger.info("Async streaming generation complete.")
                            break
                        try:
                            import json
                            chunk = json.loads(line)
                            yield chunk
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to decode async stream chunk: {line}")
                            continue

    async def agenerate_stream_aclosing(self: Any, prompt: str, llm_config: Dict[str, Any], tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        """Mock async context manager for testing - converts generator to async iterable."""
        payload = self._prepare_payload(prompt, llm_config, stream=True, tools=tools)

        async with httpx.AsyncClient() as client:
            async with client.stream("POST", f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=60) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        line = line[6:]
                        if line.strip() == "[DONE]":
                            return
                        try:
                            import json
                            chunk = json.loads(line)
                            yield chunk
                        except json.JSONDecodeError:
                            continue
