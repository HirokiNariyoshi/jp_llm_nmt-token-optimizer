"""
Main TokenOptimizer class - orchestrates the optimization pipeline.
"""

import time
from typing import Optional

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
        llm_model: str = "qwen2.5:1.5b",
        temperature: float = 0.7,
        optimization_threshold: int = 50
    ):
        """
        Initialize TokenOptimizer.
        
        Args:
            llm_model: Ollama model to use
            temperature: LLM sampling temperature
            optimization_threshold: Minimum tokens to consider optimization
        """
        self.llm_service = LLMService(llm_model, temperature)
        self.translation_service = TranslationService()
        self.token_counter = TokenCounter(llm_model)
        self.optimization_threshold = optimization_threshold
    
    def optimize_request(
        self,
        prompt: str,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        force_optimization: Optional[bool] = None
    ) -> OptimizationResponse:
        """
        Process a Japanese query with optional translation optimization.
        
        Args:
            prompt: Japanese prompt text
            max_tokens: Maximum tokens for response
            system_prompt: Optional Japanese system prompt
            force_optimization: Force enable/disable optimization (None=auto)
            
        Returns:
            OptimizationResponse with Japanese content and metrics
        """
        start_time = time.time()
        
        # Count original Japanese tokens
        original_input_tokens = self.token_counter.count_tokens(prompt)
        if system_prompt:
            original_input_tokens += self.token_counter.count_tokens(system_prompt)
        
        # Decide whether to optimize
        if force_optimization is None:
            force_optimization = original_input_tokens >= self.optimization_threshold
        
        if force_optimization:
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
        
        # Calculate metrics
        input_tokens = response["input_tokens"]
        output_tokens = response["output_tokens"]
        cost = self.token_counter.estimate_cost(input_tokens, output_tokens)
        
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
        Execute optimized request with single-translation approach.
        
        Translates JA→EN for input, instructs LLM to respond in Japanese natively.
        """
        translation_start = time.time()
        
        # Translate prompt to English
        prompt_en = self.translation_service.translate(prompt, "ja", "en")
        enhanced_prompt = f"{prompt_en.text}\n\nRespond in Japanese."
        
        # Translate system prompt if provided
        if system_prompt:
            system_en = self.translation_service.translate(system_prompt, "ja", "en")
            system_prompt_en = f"{system_en.text}\n\nRespond in Japanese."
        else:
            system_prompt_en = "Respond in Japanese."
        
        translation_time = time.time() - translation_start
        
        # Generate response - LLM generates Japanese natively
        llm_start = time.time()
        response = self.llm_service.generate(
            enhanced_prompt, max_tokens, system_prompt_en
        )
        llm_time = time.time() - llm_start
        
        # Calculate metrics
        optimized_input_tokens = response["input_tokens"]
        output_tokens = response["output_tokens"]
        
        original_cost = self.token_counter.estimate_cost(
            original_input_tokens, output_tokens
        )
        optimized_cost = self.token_counter.estimate_cost(
            optimized_input_tokens, output_tokens
        )
        
        metrics = OptimizationMetrics(
            original_tokens=original_input_tokens + output_tokens,
            optimized_tokens=optimized_input_tokens + output_tokens,
            tokens_saved=original_input_tokens - optimized_input_tokens,
            original_cost=original_cost,
            optimized_cost=optimized_cost,
            cost_saved=original_cost - optimized_cost,
            translation_time=translation_time,
            llm_time=llm_time,
            total_time=time.time() - start_time,
            used_optimization=True
        )
        
        return OptimizationResponse(
            content=response["content"],
            metrics=metrics,
            raw_response=response.get("raw_response")
        )
