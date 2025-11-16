"""
Ollama LLM integration - local and free.
"""

import time
from typing import Any, Dict, Optional

from .models import OptimizationMetrics
from .tokens import TokenCounter


class OllamaProvider:
    """Ollama local model provider - completely free."""

    def __init__(self, model: str, temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        self.token_counter = TokenCounter(model)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return self.token_counter.count_tokens(text)

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for token counts (always $0 for Ollama)."""
        return 0.0

    def generate(
        self, prompt: str, max_tokens: int = 1000, system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate completion using Ollama."""
        try:
            import requests

            # Ollama runs locally on port 11434
            api_url = "http://localhost:11434/api/chat"

            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": self.temperature, "num_predict": max_tokens},
            }

            start_time = time.time()
            response = requests.post(api_url, json=payload, timeout=120)
            generation_time = time.time() - start_time

            if response.status_code != 200:
                raise RuntimeError(
                    f"Ollama returned status {response.status_code}: {response.text}"
                )

            result = response.json()
            content = result["message"]["content"]

            # Estimate tokens since Ollama doesn't always return exact counts
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            input_tokens = self.count_tokens(full_prompt)
            output_tokens = self.count_tokens(content)

            return {
                "content": content,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "generation_time": generation_time,
                "model": self.model,
                "raw_response": result,
            }

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Could not connect to Ollama. Make sure Ollama is installed and running.\n"
                "Install: https://ollama.com/download\n"
                "Run: ollama serve"
            )
        except Exception as e:
            raise RuntimeError(f"Ollama API call failed: {str(e)}")


class LLMService:
    """Manages Ollama LLM operations."""

    def __init__(self, model: str, temperature: float = 0.7):
        """
        Initialize Ollama LLM service.

        Args:
            model: Ollama model name to use (e.g., "llama3.2:3b")
            temperature: Sampling temperature
        """
        self.provider_name = "ollama"
        self.provider = OllamaProvider(model, temperature)

    def generate(
        self, prompt: str, max_tokens: int = 1000, system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate completion from prompt.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt

        Returns:
            Dictionary with generation results
        """
        return self.provider.generate(prompt, max_tokens, system_prompt)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return self.provider.count_tokens(text)

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for request."""
        return self.provider.estimate_cost(input_tokens, output_tokens)
