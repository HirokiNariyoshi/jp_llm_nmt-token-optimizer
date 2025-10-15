# TokenOptimizer - Japanese Query Optimizer

A Python library that reduces LLM token usage for Japanese users by using single translation + native Japanese generation.

## Concept

Modern LLM tokenizers are heavily optimized for English, making Japanese text ~3-5x more token-intensive. This library translates Japanese prompts to English (saving input tokens), then instructs the LLM to generate responses directly in Japanese - avoiding problematic back-translation while maintaining high quality.

**Key Innovation:** Single translation (JA→EN) + LLM native Japanese generation = **High quality output with 13-64% token savings**

Perfect for local Ollama models - completely free!

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
    llm_model="qwen2.5:1.5b"  # Or any Ollama model
)

# Japanese input
response = optimizer.optimize_request(
    prompt="量子コンピューティングについて詳しく説明してください。",
    max_tokens=1000
)

# Japanese output
print(response.content)
print(f"Tokens saved: {response.metrics.tokens_saved}")
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
source venv/bin/activate     # Linux/Mac
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

No configuration needed! Just:

1. Install Ollama
2. Pull a model (`ollama pull qwen2.5:1.5b`)
3. Run `python optimize.py`

Everything runs locally and is completely free.

## Architecture

```
┌────────────────────────────────────────────────────────┐
│                    User Application                    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   TokenOptimizer                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Cost Analysis & Decision Engine         │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────┬─────────────────────────┬──────────────┘
                │                         │
    ┌───────────▼─────────┐   ┌──────────▼──────────┐
    │   Direct LLM Path   │   │   Optimized Path    │
    └───────────┬─────────┘   └──────────┬──────────┘
                │                         │
                │              ┌──────────▼─────────┐
                │              │    JA → EN (NMT)   │
                │              └──────────┬─────────┘
                │                         │
                ▼                         ▼
    ┌──────────────────────────────────────────┐
    │              LLM Provider                │
    └──────────────────┬───────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │     EN → JA (NMT)    │
            └──────────────────────┘
```

## Features

- ✅ **Single-translation optimization** - JA→EN input, LLM native JA output
- ✅ **High quality output** - 8-9/10 quality (vs 3/10 with double translation)
- ✅ **Perfect code formatting** - Preserves markdown ``` blocks correctly
- ✅ **13-64% token savings** - Best with longer, complex prompts
- ✅ **Local inference** - Free with Ollama (no API costs)
- ✅ **Free translation** - Google Translate via deep-translator
- ✅ **Interactive CLI** - Easy testing with `optimize.py`
- ✅ **Automatic optimization** - Smart decisions based on token analysis
- ✅ **Detailed metrics** - Token counts, cost savings, performance stats

**Token savings breakdown:**

- Short prompts (<50 tokens): May use MORE tokens (English can be longer)
- Long prompts (>100 tokens): 13-64% savings (realistic use case)

**Quality improvements over double-translation:**

- No formatting corruption (`` ` vs 「」)
- Natural Japanese (LLM native vs Google Translate)
- Complete information (no truncation)
- Professional output quality

Best use cases:

- Long technical documentation queries (100+ tokens)
- Detailed instructions and explanations
- Complex conversational prompts
- High-volume Japanese API usage
- **Any situation where code formatting matters**

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

### Improved Single-Translation Approach

**Old method (BROKEN - 3/10 quality):**

```
JA prompt → EN translation → LLM (EN response) → JA translation → JA output
                                                  ↑ This breaks formatting!
```

**New method (WORKING - 8-9/10 quality):**

```
JA prompt → EN translation → LLM (instructed: respond in JA) → JA output
         ↑                                                     ↑
    Saves tokens                                   Native Japanese!
```

### Optimization Flow

1. **Input**: Japanese prompt from user
2. **Translation**: Translate Japanese → English (free Google Translate)
3. **Enhancement**: Add instruction "Please respond in Japanese"
4. **LLM Processing**: Send English prompt with Japanese instruction
5. **Response**: LLM generates Japanese response natively
6. **Output**: Return Japanese response directly (no back-translation!)
7. **Metrics**: Calculate total token savings and quality

### Why This Works Better

- **Single translation** (not double) eliminates error source
- **LLM native Japanese** is more natural than Google Translate back-translation
- **Preserves formatting** - markdown code blocks stay intact
- **Faster processing** - one translation instead of two
- **Higher quality** - leverages multilingual LLM capabilities

**Token savings come from:**

- Input: Japanese (245 tokens) → English (88 tokens) = **64% savings on input**
- Output: LLM generates Japanese directly (no translation cost)
- Total: 13-64% overall savings depending on prompt length

## Example

```python
from token_optimizer import TokenOptimizer

# Initialize with your preferred Ollama model
optimizer = TokenOptimizer(llm_model="qwen2.5:1.5b")

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
