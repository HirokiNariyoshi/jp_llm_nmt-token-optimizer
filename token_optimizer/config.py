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
    """Configuration for LLM providers."""
    provider: str  # "openai" or "anthropic"
    api_key: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000


@dataclass
class TranslationConfig:
    """Configuration for translation providers."""
    provider: str  # "deepl", "google", etc.
    api_key: Optional[str] = None
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
    def get_llm_config(provider: str = "ollama", model: Optional[str] = None) -> LLMConfig:
        """Get LLM configuration for Ollama."""
        if provider != "ollama":
            raise ValueError(f"Only 'ollama' provider is supported")
        
        api_key = ""  # Ollama doesn't need API key (runs locally)
        # Use Qwen2.5 1.5B - lightweight multilingual model with Japanese support
        default_model = model or "qwen2.5:1.5b"
        
        return LLMConfig(
            provider=provider,
            api_key=api_key,
            model=default_model
        )
    
    @staticmethod
    def get_translation_config(provider: str = "google") -> TranslationConfig:
        """Get translation configuration for Google Translate."""
        if provider != "google":
            raise ValueError(f"Only 'google' provider is supported")
        
        return TranslationConfig(
            provider=provider,
            api_key=None,
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
