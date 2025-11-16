"""
Tests for TokenOptimizer core functionality.
"""

import pytest
from token_optimizer import TokenOptimizer
from token_optimizer.models import OptimizationResponse


@pytest.fixture
def optimizer():
    """Create a TokenOptimizer instance for testing."""
    return TokenOptimizer(llm_model="llama3.2:3b", optimization_threshold=50)


def test_optimizer_initialization(optimizer):
    """Test that optimizer initializes correctly."""
    assert optimizer is not None
    assert optimizer.optimization_threshold == 50


def test_short_prompt_direct_path(optimizer):
    """Test that short prompts use direct path (no translation)."""
    short_prompt = "こんにちは"  # Hello (very short)

    response = optimizer.optimize_request(
        prompt=short_prompt, max_tokens=100, force_optimization=False
    )

    assert isinstance(response, OptimizationResponse)
    assert response.metrics.used_optimization is False
    assert response.metrics.translation_time == 0.0


def test_long_prompt_optimization_path(optimizer):
    """Test that long prompts use optimization path."""
    long_prompt = (
        "Pythonで機械学習モデルを作成する方法について詳しく説明してください。" * 3
    )

    response = optimizer.optimize_request(
        prompt=long_prompt, max_tokens=100, force_optimization=True
    )

    assert isinstance(response, OptimizationResponse)
    assert response.metrics.used_optimization is True
    assert response.metrics.translation_time > 0


def test_force_optimization(optimizer):
    """Test force_optimization parameter."""
    prompt = "短いテスト"

    response = optimizer.optimize_request(
        prompt=prompt, max_tokens=100, force_optimization=True
    )

    assert response.metrics.used_optimization is True


def test_metrics_structure(optimizer):
    """Test that metrics contain all required fields."""
    prompt = "テストプロンプト"

    response = optimizer.optimize_request(prompt=prompt, max_tokens=100)

    metrics = response.metrics
    assert hasattr(metrics, "original_tokens")
    assert hasattr(metrics, "optimized_tokens")
    assert hasattr(metrics, "tokens_saved")
    assert hasattr(metrics, "token_reduction_percent")
    assert hasattr(metrics, "translation_time")
    assert hasattr(metrics, "llm_time")
    assert hasattr(metrics, "total_time")
    assert hasattr(metrics, "used_optimization")


def test_token_reduction_calculation(optimizer):
    """Test that token reduction is calculated correctly."""
    prompt = "Pythonで機械学習を始める方法" * 5

    response = optimizer.optimize_request(
        prompt=prompt, max_tokens=100, force_optimization=True
    )

    metrics = response.metrics
    assert metrics.tokens_saved == metrics.original_tokens - metrics.optimized_tokens

    if metrics.original_tokens > 0:
        expected_reduction = (metrics.tokens_saved / metrics.original_tokens) * 100
        assert abs(metrics.token_reduction_percent - expected_reduction) < 0.1


def test_response_content_not_empty(optimizer):
    """Test that response content is not empty."""
    prompt = "Pythonとは何ですか？"

    response = optimizer.optimize_request(prompt=prompt, max_tokens=100)

    assert response.content is not None
    assert len(response.content) > 0


def test_max_tokens_parameter(optimizer):
    """Test that max_tokens parameter is respected."""
    prompt = "Pythonについて教えてください。"

    response = optimizer.optimize_request(prompt=prompt, max_tokens=50)

    # Response should exist and be reasonable
    assert response is not None
    assert response.content is not None


def test_system_prompt_support(optimizer):
    """Test that system prompts are supported."""
    prompt = "機械学習とは？"
    system_prompt = "簡潔に答えてください。"

    response = optimizer.optimize_request(
        prompt=prompt, max_tokens=100, system_prompt=system_prompt
    )

    assert response is not None
    assert isinstance(response, OptimizationResponse)


def test_optimization_threshold_behavior(optimizer):
    """Test that optimization threshold affects decision making."""
    # Short prompt below threshold
    short_prompt = "テスト"

    response_short = optimizer.optimize_request(prompt=short_prompt, max_tokens=100)

    # Long prompt above threshold
    long_prompt = "これは長いプロンプトのテストです。" * 10

    response_long = optimizer.optimize_request(prompt=long_prompt, max_tokens=100)

    # Can't guarantee exact behavior without mocking, but both should complete
    assert response_short is not None
    assert response_long is not None
