"""
Google Translate integration - free translation service.
"""

import time
from typing import Optional

from .models import TranslationResult


class GoogleTranslator:
    """Google Translate using deep-translator - free and simple."""
    
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
    """Manages Google Translate operations."""
    
    def __init__(self):
        """Initialize Google Translate service."""
        self.provider_name = "google"
        self.provider = GoogleTranslator()
    
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
