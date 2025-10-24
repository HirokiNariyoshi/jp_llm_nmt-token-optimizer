"""
Configuration management for TokenOptimizer.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class LLMConfig:
    """Configuration for Ollama local models."""
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000


@dataclass
class TranslationConfig:
    """Configuration for Google Translate."""
    source_lang: str = "ja"  # Japanese input
    target_lang: str = "en"  # English for LLM processing


@dataclass
class OptimizationConfig:
    """Configuration for optimization behavior."""
    enabled: bool = True
    token_threshold: int = 100  # Minimum tokens to consider optimization
    cost_threshold: float = 0.001  # Minimum cost savings to optimize
    always_optimize: bool = False  # Force optimization regardless of thresholds


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
    @staticmethod
    def get_llm_config(model: Optional[str] = None) -> LLMConfig:
        """Get LLM configuration for Ollama."""
        # Use Llama 3.2 3B - Meta's modern multilingual model with excellent Japanese support
        default_model = model or "llama3.2:3b"
        
        return LLMConfig(
            model=default_model
        )
    
    @staticmethod
    def get_translation_config() -> TranslationConfig:
        """Get translation configuration for Google Translate."""
        return TranslationConfig(
            source_lang="ja",  # Japanese input
            target_lang="en"   # English for processing
        )
    

    @staticmethod
    def get_optimization_config() -> OptimizationConfig:
        """Get optimization configuration."""
        return OptimizationConfig(
            enabled=True,
            token_threshold=int(os.getenv("TOKEN_THRESHOLD", "100"))
        )


# Global config instance
config = Config()
