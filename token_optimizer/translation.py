"""
Translation service abstraction layer.
"""

import time
import hashlib
from typing import Optional
from abc import ABC, abstractmethod

from .models import TranslationResult
from .cache import CacheManager


class TranslationProvider(ABC):
    """Abstract base class for translation providers."""
    
    def __init__(self, api_key: Optional[str] = None, cache_manager: Optional[CacheManager] = None):
        self.api_key = api_key
        self.cache_manager = cache_manager
    
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate text from source to target language."""
        pass
    
    def _get_cache_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate cache key for translation."""
        content = f"{text}:{source_lang}:{target_lang}:{self.__class__.__name__}"
        return f"translation:{hashlib.md5(content.encode()).hexdigest()}"
    
    def translate_with_cache(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate with caching support."""
        # Check cache first
        if self.cache_manager:
            cache_key = self._get_cache_key(text, source_lang, target_lang)
            cached_result = self.cache_manager.get(cache_key)
            
            if cached_result:
                return TranslationResult(
                    text=cached_result,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    provider=self.__class__.__name__,
                    cached=True,
                    translation_time=0.0
                )
        
        # Perform translation
        start_time = time.time()
        result = self.translate(text, source_lang, target_lang)
        translation_time = time.time() - start_time
        result.translation_time = translation_time
        
        # Cache the result
        if self.cache_manager:
            cache_key = self._get_cache_key(text, source_lang, target_lang)
            self.cache_manager.set(cache_key, result.text)
        
        return result


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
    
    def __init__(self, provider: str = "google", api_key: Optional[str] = None, 
                 cache_manager: Optional[CacheManager] = None):
        """
        Initialize translation service.
        
        Args:
            provider: Translation provider name (only "google" supported)
            api_key: Not used for Google Translate
            cache_manager: Optional cache manager for translation caching
        """
        if provider.lower() != "google":
            raise ValueError(f"Only 'google' provider is supported")
        
        self.provider_name = "google"
        self.cache_manager = cache_manager
        self.provider = GoogleTranslator(api_key, cache_manager)
    
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
        return self.provider.translate_with_cache(text, source_lang, target_lang)
