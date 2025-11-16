"""
Data models for TokenOptimizer.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class OptimizationMetrics:
    """Metrics for optimization performance."""

    original_tokens: int
    optimized_tokens: int
    tokens_saved: int
    original_cost: float
    optimized_cost: float
    cost_saved: float
    translation_time: float
    llm_time: float
    total_time: float
    used_optimization: bool

    @property
    def token_reduction_percent(self) -> float:
        """Calculate percentage of LLM tokens saved."""
        if self.original_tokens == 0:
            return 0.0
        return (self.tokens_saved / self.original_tokens) * 100

    @property
    def cost_reduction_percent(self) -> float:
        """Calculate percentage of cost saved."""
        if self.original_cost == 0:
            return 0.0
        return (self.cost_saved / self.original_cost) * 100

    @property
    def time_overhead_percent(self) -> float:
        """Calculate translation time as percentage of total time."""
        if self.total_time == 0:
            return 0.0
        return (self.translation_time / self.total_time) * 100


@dataclass
class OptimizationResponse:
    """Response from optimized LLM request."""

    content: str
    metrics: OptimizationMetrics
    raw_response: Optional[Dict[str, Any]] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "content": self.content,
            "metrics": {
                "original_tokens": self.metrics.original_tokens,
                "optimized_tokens": self.metrics.optimized_tokens,
                "tokens_saved": self.metrics.tokens_saved,
                "token_reduction_percent": self.metrics.token_reduction_percent,
                "original_cost": self.metrics.original_cost,
                "optimized_cost": self.metrics.optimized_cost,
                "cost_saved": self.metrics.cost_saved,
                "cost_reduction_percent": self.metrics.cost_reduction_percent,
                "translation_time": self.metrics.translation_time,
                "time_overhead_percent": self.metrics.time_overhead_percent,
                "llm_time": self.metrics.llm_time,
                "total_time": self.metrics.total_time,
                "used_optimization": self.metrics.used_optimization,
            },
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class TranslationResult:
    """Result from translation operation."""

    text: str
    source_lang: str
    target_lang: str
    provider: str
    cached: bool = False
    translation_time: float = 0.0
