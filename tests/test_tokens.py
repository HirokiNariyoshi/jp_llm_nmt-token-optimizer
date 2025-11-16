"""
Tests for token counting functionality.
"""

import pytest

from token_optimizer.tokens import TokenCounter


@pytest.fixture
def counter():
    """Create a TokenCounter instance."""
    return TokenCounter(model="llama3.2:3b")


def test_token_counter_initialization(counter):
    """Test TokenCounter initializes correctly."""
    assert counter is not None


def test_count_english_tokens(counter):
    """Test counting English tokens."""
    text = "This is a test sentence."
    count = counter.count_tokens(text)

    assert isinstance(count, int)
    assert count > 0
    assert count < 20  # Reasonable range


def test_count_japanese_tokens(counter):
    """Test counting Japanese tokens."""
    text = "これはテスト文です。"
    count = counter.count_tokens(text)

    assert isinstance(count, int)
    assert count > 0


def test_empty_string_tokens(counter):
    """Test counting tokens in empty string."""
    count = counter.count_tokens("")
    assert count == 0


def test_japanese_uses_more_tokens(counter):
    """Test that Japanese text uses more tokens than English."""
    english = "Hello, how are you?"
    japanese = "こんにちは、お元気ですか？"

    english_count = counter.count_tokens(english)
    japanese_count = counter.count_tokens(japanese)

    # Japanese should use more tokens for similar content
    assert japanese_count >= english_count


def test_cost_estimation(counter):
    """Test cost estimation functionality."""
    input_tokens = 100
    output_tokens = 50

    cost = counter.estimate_cost(input_tokens, output_tokens)

    assert isinstance(cost, float)
    assert cost >= 0


def test_long_text_token_count(counter):
    """Test token counting for longer text."""
    long_text = "This is a longer test sentence. " * 50
    count = counter.count_tokens(long_text)

    assert isinstance(count, int)
    assert count > 100  # Should be substantial for repeated text


def test_special_characters(counter):
    """Test token counting with special characters."""
    text = "Test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
    count = counter.count_tokens(text)

    assert isinstance(count, int)
    assert count > 0


def test_unicode_handling(counter):
    """Test handling of various Unicode characters."""
    texts = [
        "日本語",  # Japanese
        "한글",  # Korean
        "中文",  # Chinese
        "Español",  # Spanish with accent
        "🎉🎊",  # Emojis
    ]

    for text in texts:
        count = counter.count_tokens(text)
        assert isinstance(count, int)
        assert count > 0
