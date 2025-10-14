"""
Main TokenOptimizer class - orchestrates the optimization pipeline.
"""

import time
from typing import Optional, Dict, Any

from .config import Config
from .llm import LLMService
from .translation import TranslationService
from .tokens import TokenCounter
from .models import OptimizationResponse, OptimizationMetrics


class TokenOptimizer:
    """
    Optimizer for Japanese queries using English-optimized LLMs.
    Translates Japanese→English for processing, then back to Japanese.
    """
    
    def __init__(
        self,
        llm_model: Optional[str] = None,
        temperature: float = 0.7,
        optimization_threshold: int = 100
    ):
        """
        Initialize TokenOptimizer.
        
        Args:
            llm_model: Ollama model to use (defaults to qwen2.5:1.5b)
            temperature: LLM sampling temperature
            optimization_threshold: Minimum tokens to consider optimization
        """
        # Load configurations
        config = Config()
        llm_config = config.get_llm_config(llm_model)
        translation_config = config.get_translation_config()
        
        # Initialize services
        self.llm_service = LLMService(
            llm_config.model,
            temperature
        )
        
        self.translation_service = TranslationService()
        
        self.token_counter = TokenCounter(llm_config.model)
        self.optimization_threshold = optimization_threshold
    
    def optimize_request(
        self,
        prompt: str,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        force_optimization: Optional[bool] = None,
        compare_mode: bool = False
    ) -> OptimizationResponse:
        """
        Process a Japanese query with optional translation optimization.
        
        Args:
            prompt: Japanese prompt text
            max_tokens: Maximum tokens for response
            system_prompt: Optional Japanese system prompt
            force_optimization: Force enable/disable optimization (None=auto)
            compare_mode: If True, query both paths for accurate token comparison
                         (slower but more accurate)
            
        Returns:
            OptimizationResponse with Japanese content and metrics
        """
        start_time = time.time()
        
        # In compare mode, query both paths for accurate measurement
        if compare_mode:
            return self._compare_both_paths(
                prompt, max_tokens, system_prompt, start_time
            )
        
        # Count original Japanese tokens
        original_input_tokens = self.token_counter.count_tokens(prompt)
        if system_prompt:
            original_input_tokens += self.token_counter.count_tokens(system_prompt)
        
        # Decide whether to optimize
        should_optimize = force_optimization
        if should_optimize is None:
            # Auto-decide based on threshold and token analysis
            should_optimize = (
                original_input_tokens >= self.optimization_threshold
            )
        
        if should_optimize:
            return self._optimized_request(
                prompt, max_tokens, system_prompt,
                original_input_tokens, start_time
            )
        else:
            return self._direct_request(
                prompt, max_tokens, system_prompt,
                original_input_tokens, start_time
            )
    
    def _direct_request(
        self,
        prompt: str,
        max_tokens: int,
        system_prompt: Optional[str],
        original_input_tokens: int,
        start_time: float
    ) -> OptimizationResponse:
        """Execute direct LLM request in Japanese without translation."""
        
        # Generate response directly in Japanese
        response = self.llm_service.generate(prompt, max_tokens, system_prompt)
        
        total_time = time.time() - start_time
        
        # Calculate costs
        input_tokens = response["input_tokens"]
        output_tokens = response["output_tokens"]
        
        cost = self.token_counter.estimate_cost(input_tokens, output_tokens)
        
        # Create metrics (no optimization used)
        metrics = OptimizationMetrics(
            original_tokens=input_tokens + output_tokens,
            optimized_tokens=input_tokens + output_tokens,
            tokens_saved=0,
            original_cost=cost,
            optimized_cost=cost,
            cost_saved=0.0,
            translation_time=0.0,
            llm_time=response["generation_time"],
            total_time=total_time,
            used_optimization=False
        )
        
        return OptimizationResponse(
            content=response["content"],
            metrics=metrics,
            raw_response=response.get("raw_response")
        )
    
    def _optimized_request(
        self,
        prompt: str,
        max_tokens: int,
        system_prompt: Optional[str],
        original_input_tokens: int,
        start_time: float
    ) -> OptimizationResponse:
        """
        Execute optimized LLM request by translating Japanese→English→Japanese.
        This reduces token usage for English-optimized models.
        """
        
        translation_start = time.time()
        
        # Translate Japanese prompt to English for LLM
        prompt_en = self.translation_service.translate(
            prompt, source_lang="ja", target_lang="en"
        )
        
        # Translate system prompt if provided
        system_prompt_en = None
        if system_prompt:
            system_result = self.translation_service.translate(
                system_prompt, source_lang="ja", target_lang="en"
            )
            system_prompt_en = system_result.text
        
        translation_to_en_time = time.time() - translation_start
        
        # Count English tokens (optimized - should be lower)
        en_input_tokens = self.token_counter.count_tokens(prompt_en.text)
        if system_prompt_en:
            en_input_tokens += self.token_counter.count_tokens(system_prompt_en)
        
        # Generate response in English
        response = self.llm_service.generate(
            prompt_en.text, max_tokens, system_prompt_en
        )
        
        # Translate English response back to Japanese
        translation_back_start = time.time()
        response_ja = self.translation_service.translate(
            response["content"], source_lang="en", target_lang="ja"
        )
        translation_from_en_time = time.time() - translation_back_start
        
        total_translation_time = translation_to_en_time + translation_from_en_time
        total_time = time.time() - start_time
        
        # Calculate costs
        optimized_input_tokens = response["input_tokens"]
        output_tokens = response["output_tokens"]
        
        original_cost = self.token_counter.estimate_cost(
            original_input_tokens, output_tokens
        )
        optimized_cost = self.token_counter.estimate_cost(
            optimized_input_tokens, output_tokens
        )
        
        # Create metrics
        metrics = OptimizationMetrics(
            original_tokens=original_input_tokens + output_tokens,
            optimized_tokens=optimized_input_tokens + output_tokens,
            tokens_saved=original_input_tokens - optimized_input_tokens,
            original_cost=original_cost,
            optimized_cost=optimized_cost,
            cost_saved=original_cost - optimized_cost,
            translation_time=total_translation_time,
            llm_time=response["generation_time"],
            total_time=total_time,
            used_optimization=True
        )
        
        return OptimizationResponse(
            content=response_ja.text,
            metrics=metrics,
            raw_response=response.get("raw_response")
        )
    
    def _compare_both_paths(
        self,
        prompt: str,
        max_tokens: int,
        system_prompt: Optional[str],
        start_time: float
    ) -> OptimizationResponse:
        """
        Query both direct and optimized paths for accurate token comparison.
        This is slower but provides real token counts from the model.
        """
        
        # Path 1: Direct Japanese request
        print("  [Compare Mode] Querying with direct Japanese...")
        direct_response = self.llm_service.generate(prompt, max_tokens, system_prompt)
        direct_input_tokens = direct_response["input_tokens"]
        direct_output_tokens = direct_response["output_tokens"]
        
        # Path 2: Optimized (Japanese→English→Japanese)
        print("  [Compare Mode] Querying with English translation...")
        translation_start = time.time()
        
        # Translate to English
        prompt_en = self.translation_service.translate(
            prompt, source_lang="ja", target_lang="en"
        )
        
        system_prompt_en = None
        if system_prompt:
            system_result = self.translation_service.translate(
                system_prompt, source_lang="ja", target_lang="en"
            )
            system_prompt_en = system_result.text
        
        translation_to_en_time = time.time() - translation_start
        
        # Generate in English
        optimized_response = self.llm_service.generate(
            prompt_en.text, max_tokens, system_prompt_en
        )
        optimized_input_tokens = optimized_response["input_tokens"]
        optimized_output_tokens = optimized_response["output_tokens"]
        
        # Translate response back to Japanese
        translation_back_start = time.time()
        response_ja = self.translation_service.translate(
            optimized_response["content"], source_lang="en", target_lang="ja"
        )
        translation_from_en_time = time.time() - translation_back_start
        
        total_translation_time = translation_to_en_time + translation_from_en_time
        total_time = time.time() - start_time
        
        # Calculate real savings using actual token counts from both queries
        tokens_saved = direct_input_tokens - optimized_input_tokens
        
        direct_cost = self.token_counter.estimate_cost(
            direct_input_tokens, direct_output_tokens
        )
        optimized_cost = self.token_counter.estimate_cost(
            optimized_input_tokens, optimized_output_tokens
        )
        
        print(f"  [Compare Mode] Direct: {direct_input_tokens} input tokens")
        print(f"  [Compare Mode] Optimized: {optimized_input_tokens} input tokens")
        print(f"  [Compare Mode] Saved: {tokens_saved} tokens ({tokens_saved/direct_input_tokens*100:.1f}%)")
        
        # Create metrics with real comparison data
        metrics = OptimizationMetrics(
            original_tokens=direct_input_tokens + direct_output_tokens,
            optimized_tokens=optimized_input_tokens + optimized_output_tokens,
            tokens_saved=tokens_saved,
            original_cost=direct_cost,
            optimized_cost=optimized_cost,
            cost_saved=direct_cost - optimized_cost,
            translation_time=total_translation_time,
            llm_time=optimized_response["generation_time"],
            total_time=total_time,
            used_optimization=True
        )
        
        # Return the optimized (translated) response
        return OptimizationResponse(
            content=response_ja.text,
            metrics=metrics,
            raw_response=optimized_response.get("raw_response")
        )
    
    def analyze_potential_savings(self, prompt: str, output_tokens: int = 500) -> Dict[str, Any]:
        """
        Analyze potential token and cost savings for a Japanese prompt.
        
        Args:
            prompt: Japanese prompt text
            output_tokens: Estimated output tokens
            
        Returns:
            Dictionary with savings analysis
        """
        # Count original Japanese tokens
        ja_tokens = self.token_counter.count_tokens(prompt)
        
        # Translate to get English token count
        prompt_en = self.translation_service.translate(
            prompt, source_lang="ja", target_lang="en"
        )
        en_tokens = self.token_counter.count_tokens(prompt_en.text)
        
        # Calculate savings
        input_tokens_saved = ja_tokens - en_tokens
        total_tokens_saved = input_tokens_saved  # Output tokens same in both
        
        ja_cost = self.token_counter.estimate_cost(ja_tokens, output_tokens)
        en_cost = self.token_counter.estimate_cost(en_tokens, output_tokens)
        cost_saved = ja_cost - en_cost
        
        return {
            "japanese_input_tokens": ja_tokens,
            "english_input_tokens": en_tokens,
            "input_tokens_saved": input_tokens_saved,
            "token_reduction_percent": (input_tokens_saved / ja_tokens * 100) if ja_tokens > 0 else 0,
            "japanese_cost": ja_cost,
            "english_cost": en_cost,
            "cost_saved": cost_saved,
            "cost_reduction_percent": (cost_saved / ja_cost * 100) if ja_cost > 0 else 0,
            "recommendation": "optimize" if input_tokens_saved > 50 else "direct"
        }
