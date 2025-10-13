# TokenOptimizer - Japanese Query Optimizer

A Python library that reduces LLM API costs for Japanese users by translating queries to English for processing.

## Concept

Modern LLM tokenizers (GPT-4, Claude, etc.) are heavily optimized for English, making Japanese text ~2-3x more expensive in token usage. This library translates Japanese prompts to English, processes them with English-optimized LLMs, then translates responses back to Japanese - saving ~58% on token costs.

## Quick Start

```python
from token_optimizer import TokenOptimizer

optimizer = TokenOptimizer(
    llm_provider="ollama",
    llm_model="qwen2.5:1.5b",
    translation_provider="google"
)

# Japanese input
response = optimizer.optimize_request(
    prompt="量子コンピューティングについて詳しく説明してください。",
    max_tokens=1000
)

# Japanese output
print(response.content)
print(f"Tokens saved: {response.metrics.tokens_saved}")
print(f"Cost saved: ${response.metrics.cost_saved:.4f}")
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
# LLM API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Translation API Keys
DEEPL_API_KEY=your_deepl_key

# Optional: Redis for caching
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Application                      │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   TokenOptimizer                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Cost Analysis & Decision Engine         │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────┬─────────────────────────┬───────────────┘
                │                         │
    ┌───────────▼─────────┐   ┌──────────▼──────────┐
    │  Direct LLM Path    │   │   Optimized Path    │
    └───────────┬─────────┘   └──────────┬──────────┘
                │                         │
                │              ┌──────────▼──────────┐
                │              │  JA → EN (NMT)      │
                │              └──────────┬──────────┘
                │                         │
                ▼                         ▼
    ┌──────────────────────────────────────────┐
    │     LLM Provider (English-optimized)      │
    └──────────────────┬───────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   EN → JA (NMT)      │
            └──────────────────────┘
```

## Features

- Multi-LLM support (OpenAI GPT, Anthropic Claude)
- Multiple translation providers (DeepL, Google Translate)
- Automatic optimization decisions based on token analysis
- Redis caching for repeated translations
- Detailed cost and token metrics
- Configurable optimization thresholds

## Performance

Typical results:

- Token reduction: 30-50% for complex prompts
- Cost savings vary by model and prompt complexity
- Best for: technical documents, detailed instructions, complex queries

## Testing

```bash
pytest tests/ -v --cov=token_optimizer
```

## License

MIT License
