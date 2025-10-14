"""
Token counting utilities for Ollama models.
"""

import tiktoken
from typing import Optional


class TokenCounter:
    """Count tokens for Ollama models (free, local inference)."""
    
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
        
        For Ollama (local models), cost is always $0.00.
        This method exists for API compatibility.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            0.0 (Ollama is free!)
        """
        return 0.0
    
    @staticmethod
    def compare_languages(japanese_text: str, english_text: str, model: str = "qwen2.5:1.5b") -> dict:
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
