# TokenOptimizer - Japanese LLM Token Optimizer

Reduce LLM token usage for Japanese queries by 15-25% while maintaining high quality output.

## How It Works

Japanese text uses 3-5x more tokens than English in most LLM tokenizers. This library:

1. Translates Japanese prompts → English (saves input tokens)
2. Instructs the LLM to respond in Japanese natively (avoids back-translation)
3. Returns high-quality Japanese output directly

**Result:** 15-25% token savings

## Installation

```bash
# 1. Clone and setup
git clone https://github.com/HirokiNariyoshi/llm_nmt-token-optimizer.git
cd llm_nmt-token-optimizer
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

# 2. Install and setup Ollama
# Download from https://ollama.ai
ollama serve  # Start Ollama server
ollama pull qwen2.5:1.5b  # Download model (986MB)
```

## Quick Start

### Interactive CLI

```bash
python optimize.py
```

### Python API

```python
from token_optimizer import TokenOptimizer

optimizer = TokenOptimizer(llm_model="qwen2.5:1.5b")

response = optimizer.optimize_request(
    prompt="Pythonで機械学習モデルを作る方法を教えてください。",
    max_tokens=500
)

print(response.content)  # Japanese output
print(f"Tokens saved: {response.metrics.tokens_saved}")
```

## Features

- ✅ **13-64% token savings** on realistic prompts (100+ tokens)
- ✅ **High quality output** - 8-9/10 vs 3/10 with double translation
- ✅ **Perfect formatting** - Preserves code blocks, markdown, etc.
- ✅ **Free** - Uses Ollama (local) + Google Translate (free API)
- ✅ **Fast** - Single translation vs double translation

## When To Use

**✅ Best for:**

- Long technical queries (>100 tokens)
- Code examples and documentation
- Detailed explanations
- Situations where quality matters

**❌ Not ideal for:**

- Very short prompts (<50 tokens) - English may be longer than Japanese
- Real-time chat - Translation adds latency (~1s)

## Configuration

The optimizer automatically decides whether to translate based on token analysis. You can override:

```python
# Force optimization
response = optimizer.optimize_request(
    prompt="...",
    force_optimization=True
)

# Force direct (no translation)
response = optimizer.optimize_request(
    prompt="...",
    force_optimization=False
)

# Auto-decide (default, threshold=50 tokens)
optimizer = TokenOptimizer(
    llm_model="qwen2.5:1.5b",
    optimization_threshold=50
)
```

## Architecture

```
JA prompt → EN translation → LLM (instructed: respond in JA) → JA output
         ↑ Saves tokens                                        ↑ Native quality
```

vs old broken approach:

```
JA → EN → LLM → EN → JA
                  ↑ This back-translation corrupts formatting!
```

## Project Structure

```
llm_nmt-token-optimizer/
├── token_optimizer/          # Core library
│   ├── optimizer.py         # Main optimizer logic
│   ├── llm.py              # Ollama integration
│   ├── translation.py      # Google Translate wrapper
│   └── tokens.py           # Token counting
├── optimize.py             # Interactive CLI
└── requirements.txt        # Dependencies
```

## Contributing

Contributions welcome! This is a research project exploring LLM token optimization for Japanese users.

## License

MIT License
