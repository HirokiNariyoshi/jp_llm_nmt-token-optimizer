# TokenOptimizer - Japanese Query Optimizer

A Python library that reduces LLM API costs for Japanese users by translating queries to English for processing.

## Concept

Modern LLM tokenizers (GPT-4, Claude, etc.) are heavily optimized for English, making Japanese text ~2-3x more expensive in token usage. This library translates Japanese prompts to English, processes them with English-optimized LLMs, then translates responses back to Japanese - saving ~58% on token costs.

## Quick Start

### Interactive Mode

```bash
python optimize.py
# Enter your Japanese query when prompted
```

### Programmatic Usage

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

### Compare Mode (Accurate Measurement)

```python
# Query both paths for real token counts
response = optimizer.optimize_request(
    prompt="日本語のプロンプト",
    compare_mode=True  # Queries model twice for accuracy
)
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/HirokiNariyoshi/llm_nmt-token-optimizer.git
cd llm_nmt-token-optimizer
```

### 2. Create virtual environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate      # Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Ollama (for local testing)

See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed instructions.

```bash
ollama pull qwen2.5:1.5b
```

## Configuration

### For Local Development (Ollama)

No configuration needed! Just install Ollama and pull a model.

### For Production APIs (Optional)

Create a `.env` file for API keys:

```env
# LLM API Keys (if using cloud providers)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Optional: Redis for caching
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Note:** Currently only Ollama (local) and Google Translate (free) are fully supported.

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

- ✅ **Japanese→English optimization** - Reduces token usage by 53-58%
- ✅ **Local inference** - Free with Ollama (no API costs)
- ✅ **Free translation** - Google Translate via deep-translator
- ✅ **Compare mode** - Query both paths for accurate measurement
- ✅ **Interactive CLI** - Easy testing with `optimize.py`
- ✅ **Automatic optimization** - Smart decisions based on token analysis
- ✅ **Detailed metrics** - Token counts, cost savings, performance stats
- ✅ **Optional caching** - Redis support for repeated queries

## Performance

Real-world test results with `qwen2.5:1.5b`:

| Prompt Type | Japanese Tokens | English Tokens | Savings | % Reduction |
|-------------|----------------|----------------|---------|-------------|
| Short technical | 85 | 28 | 57 | 67.1% |
| Long conversational | 616 | 287 | 329 | 53.4% |
| Business query | 204 | 87 | 117 | 57.4% |

**Average savings: ~58% on input tokens**

Best use cases:
- Technical documentation queries
- Detailed instructions
- Complex conversational prompts
- High-volume Japanese API usage

## Modes

### Standard Mode
Uses tiktoken estimates for fast decision-making.

```python
response = optimizer.optimize_request(
    prompt="日本語プロンプト",
    compare_mode=False  # Default: fast estimation
)
```

### Compare Mode
Queries model twice (Japanese + English) for 100% accurate token measurements.

```python
response = optimizer.optimize_request(
    prompt="日本語プロンプト",
    compare_mode=True  # Queries model twice for real counts
)
```

## How It Works

### Standard Flow (Japanese → English Optimization)

1. **Input**: Japanese prompt from user
2. **Translation**: Translate Japanese → English (free Google Translate)
3. **Token Analysis**: Compare Japanese vs English token counts using tiktoken
4. **LLM Processing**: Send English prompt to model (saves tokens)
5. **Response**: Get English response from model
6. **Translation**: Translate English → Japanese for user
7. **Metrics**: Calculate total token savings and cost reduction

### Compare Mode (Accurate Measurement)

For 100% accurate token counts:
1. Query model with original Japanese prompt (measure real tokens used)
2. Query model with translated English prompt (measure real tokens used)
3. Compare actual token usage from both paths
4. Return optimized result with exact metrics

**Why this works:** Japanese characters consume 3-5x more tokens than English equivalents in most LLM tokenizers.

## Example

```python
from token_optimizer import TokenOptimizer

optimizer = TokenOptimizer(
    llm_provider="ollama",
    llm_model="qwen2.5:1.5b",
    translation_provider="google"
)

# Original Japanese prompt
japanese_prompt = """
量子コンピューティングの基本原理と、
現代のコンピューターとの違いについて詳しく説明してください。
特に、量子ビットと従来のビットの違いに焦点を当ててください。
"""

# Optimize and get response
response = optimizer.optimize_request(
    prompt=japanese_prompt,
    max_tokens=500,
    compare_mode=True  # Use real token counts
)

print(f"Response (Japanese): {response.content}")
print(f"\nMetrics:")
print(f"  Original tokens: {response.metrics.original_tokens}")
print(f"  Optimized tokens: {response.metrics.optimized_tokens}")
print(f"  Tokens saved: {response.metrics.tokens_saved}")
print(f"  Percentage saved: {response.metrics.percent_saved:.1f}%")
print(f"  Cost saved: ${response.metrics.cost_saved:.4f}")
```

## Project Structure

```
llm_nmt-token-optimizer/
├── token_optimizer/
│   ├── __init__.py
│   ├── optimizer.py      # Main TokenOptimizer class
│   ├── llm.py            # Ollama LLM provider
│   ├── translation.py    # Google Translate service
│   ├── tokens.py         # Token counting with tiktoken
│   └── config.py         # Configuration management
├── optimize.py           # Interactive CLI script
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── OLLAMA_SETUP.md      # Local Ollama setup guide
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

MIT License - see LICENSE file for details.
