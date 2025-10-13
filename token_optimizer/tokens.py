"""
Token counting utilities for different LLM providers.
"""

import tiktoken
from typing import Optional


class TokenCounter:
    """Count tokens for different LLM models."""
    
    # Cost per 1K tokens (input/output) - as of 2024
    COSTS = {
        "gpt-4o": (0.0025, 0.01),
        "gpt-4o-mini": (0.00015, 0.0006),
        "gpt-4-turbo": (0.01, 0.03),
        "gpt-3.5-turbo": (0.0005, 0.0015),
        "claude-3-5-sonnet-20241022": (0.003, 0.015),
        "claude-3-opus-20240229": (0.015, 0.075),
        "claude-3-sonnet-20240229": (0.003, 0.015),
        "claude-3-haiku-20240307": (0.00025, 0.00125),
    }
    
    def __init__(self, model: str):
        self.model = model
        self._encoder: Optional[tiktoken.Encoding] = None
        
    @property
    def encoder(self) -> tiktoken.Encoding:
        """Lazy load the tokenizer encoder."""
        if self._encoder is None:
            try:
                # Try to get encoding for specific model
                self._encoder = tiktoken.encoding_for_model(self.model)
            except KeyError:
                # Fall back to cl100k_base (used by GPT-4 and Claude)
                self._encoder = tiktoken.get_encoding("cl100k_base")
        return self._encoder
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in text."""
        return len(self.encoder.encode(text))
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate the cost for a request.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        # Get costs for model, default to GPT-4 pricing
        input_cost_per_1k, output_cost_per_1k = self.COSTS.get(
            self.model, 
            self.COSTS.get("gpt-4o", (0.0025, 0.01))
        )
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        return input_cost + output_cost
    
    @staticmethod
    def compare_languages(japanese_text: str, english_text: str, model: str = "gpt-4o") -> dict:
        """
        Compare token counts between Japanese and English versions.
        Japanese typically uses more tokens in English-optimized models.
        
        Returns:
            Dictionary with comparison metrics showing English efficiency
        """
        counter = TokenCounter(model)
        
        ja_tokens = counter.count_tokens(japanese_text)
        en_tokens = counter.count_tokens(english_text)
        
        tokens_saved = ja_tokens - en_tokens
        percent_saved = (tokens_saved / ja_tokens * 100) if ja_tokens > 0 else 0
        
        return {
            "japanese_tokens": ja_tokens,
            "english_tokens": en_tokens,
            "tokens_saved": tokens_saved,
            "percent_saved": percent_saved,
            "compression_ratio": en_tokens / ja_tokens if ja_tokens > 0 else 1.0
        }
