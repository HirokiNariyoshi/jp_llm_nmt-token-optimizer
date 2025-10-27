"""
Translation service using Meta's NLLB (No Language Left Behind).
"""

import time
from typing import Optional

from .models import TranslationResult


class NLLBTranslator:
    """Neural Machine Translation using Meta's NLLB-200."""
    
    def __init__(self, model_name: str = "facebook/nllb-200-distilled-600M"):
        """Initialize NLLB translator."""
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            print(f"Loading NLLB model ({model_name})... This may take a minute on first run.")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Language code mapping
            self.lang_codes = {
                "ja": "jpn_Jpan",
                "en": "eng_Latn"
            }
            
            print("✓ NLLB model loaded successfully!")
            
        except ImportError:
            raise ImportError(
                "transformers not installed. Install with: "
                "pip install transformers sentencepiece"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load NLLB model: {str(e)}")
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translate using NLLB."""
        try:
            # Get language codes
            src_code = self.lang_codes.get(source_lang.lower(), "eng_Latn")
            tgt_code = self.lang_codes.get(target_lang.lower(), "jpn_Jpan")
            
            # Set source language
            self.tokenizer.src_lang = src_code
            
            # Encode input
            inputs = self.tokenizer(text, return_tensors="pt", padding=True)
            
            # Get target language token ID
            tgt_lang_id = self.tokenizer.convert_tokens_to_ids(tgt_code)
            
            # Generate translation
            translated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=tgt_lang_id,
                max_length=512,
                num_beams=5,
                early_stopping=True
            )
            
            # Decode output
            translated_text = self.tokenizer.decode(
                translated_tokens[0],
                skip_special_tokens=True
            )
            
            return TranslationResult(
                text=translated_text,
                source_lang=source_lang,
                target_lang=target_lang,
                provider="NLLB",
                cached=False
            )
            
        except Exception as e:
            raise RuntimeError(f"NLLB translation failed: {str(e)}")


class TranslationService:
    """Translation service using NLLB."""
    
    def __init__(self):
        """Initialize NLLB translation service."""
        self.provider = NLLBTranslator()
        self.provider_name = "nllb"
    
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
