"""
Translation service abstraction layer.
"""

import time
from typing import Optional
from abc import ABC, abstractmethod

from .models import TranslationResult


class TranslationProvider(ABC):
    """Abstract base class for translation providers."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate text from source to target language."""
        pass


class GoogleTranslator(TranslationProvider):
    """Google Translate provider using deep-translator."""
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate using Google Translate."""
        try:
            from deep_translator import GoogleTranslator as GT
            
            # Map language codes
            source = "en" if source_lang.lower() == "en" else source_lang
            target = "ja" if target_lang.lower() == "ja" else target_lang
            
            translator = GT(source=source, target=target)
            translated = translator.translate(text)
            
            return TranslationResult(
                text=translated,
                source_lang=source_lang,
                target_lang=target_lang,
                provider="Google",
                cached=False
            )
            
        except ImportError:
            raise ImportError("deep-translator not installed. Install with: pip install deep-translator")
        except Exception as e:
            raise RuntimeError(f"Google translation failed: {str(e)}")


class TranslationService:
    """Manages translation operations with multiple providers."""
    
    def __init__(self, provider: str = "google", api_key: Optional[str] = None):
        """
        Initialize translation service.
        
        Args:
            provider: Translation provider name (only "google" supported)
            api_key: Not used for Google Translate
        """
        if provider.lower() != "google":
            raise ValueError(f"Only 'google' provider is supported")
        
        self.provider_name = "google"
        self.provider = GoogleTranslator(api_key)
    
    def translate(self, text: str, source_lang: str = "en", 
                  target_lang: str = "ja") -> TranslationResult:
        """
        Translate text between languages.
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            TranslationResult with translated text and metadata
        """
        start_time = time.time()
        result = self.provider.translate(text, source_lang, target_lang)
        result.translation_time = time.time() - start_time
        return result
