# Japanese LLM Token Optimizer

Reduce LLM token usage for Japanese queries by **~65%** on realistic prompts (100+ tokens) while maintaining high quality output.

Available as both a **Python library** and **REST API** for easy integration.

## How It Works

Japanese text uses 3-5x more tokens than English in most LLM tokenizers. This library:

1. Translates Japanese prompts → English using **Meta's NLLB** neural machine translation
2. Instructs the LLM to respond in Japanese natively (avoids back-translation)
3. Returns high-quality Japanese output directly

**Result:** **~65% LLM token reduction** on prompts ≥100 tokens

## Installation

**Requirements:**

- Python 3.8+ (Python 3.10+ recommended)
- 4GB RAM minimum (8GB recommended for smooth operation)
- Ollama installed and running

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
ollama pull llama3.2:3b  # Download model (~2GB)

# Note: NLLB translation model (600MB) will auto-download on first use
```

## Quick Start

### REST API (Docker)

```bash
# Start the API
docker-compose up -d

# Test with curl
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Pythonで機械学習を始める方法は？", "max_tokens": 500}'

# View interactive docs
open http://localhost:8000/docs
```

**API Response:**

```json
{
  "content": "機械学習を始めるには...",
  "metrics": {
    "token_reduction_percent": 54.7,
    "tokens_saved": 47,
    "translation_time": 3.2,
    "total_time": 12.7
  }
}
```

See [examples/api_clients.md](examples/api_clients.md) for Python, JavaScript, and curl examples.

### Python Library

```python
from token_optimizer import TokenOptimizer

optimizer = TokenOptimizer(llm_model="llama3.2:3b")

response = optimizer.optimize_request(
    prompt="Pythonで機械学習モデルを作る方法を教えてください。",
    max_tokens=500
)

print(response.content)  # Japanese output
print(f"Tokens saved: {response.metrics.tokens_saved}")
```

### Interactive CLI

```bash
python optimize.py
```

**Example output:**

```
Japanese Query Optimizer
Reduces LLM token usage by ~65% for English-optimized LLMs
======================================================================

Enter your Japanese query (press Enter twice when done):

Pythonで機械学習モデルを作る方法を教えてください。

Processing query (1 words)...
Optimizing with translation...

======================================================================
RESPONSE
======================================================================

機械学習モデルを作成するには... (Japanese response here)

======================================================================
OPTIMIZATION METRICS
======================================================================

TOKEN USAGE:
  Original tokens:  86
  Optimized tokens: 39
  Tokens saved:     47
  Reduction:        54.7%

COST SAVINGS:
  Without optimization: $0.000000
  With optimization:    $0.000000
  Saved:                $0.000000
  Cost reduction:       0.0%

PERFORMANCE:
  Translation time: 3.2s (25% of total)
  LLM time:         9.5s
  Total time:       12.7s

Optimization successful! English translation reduced LLM token usage.
Token reduction: 54.7%
Translation overhead: 3.2s (25% of time)
```

## Configuration

```python
from token_optimizer import TokenOptimizer

optimizer = TokenOptimizer(llm_model="llama3.2:3b")

response = optimizer.optimize_request(
    prompt="Pythonで機械学習モデルを作る方法を教えてください。",
    max_tokens=500
)

print(response.content)  # Japanese output
print(f"Tokens saved: {response.metrics.tokens_saved}")
```

## Features

- ~65% LLM token reduction on realistic prompts (100+ tokens)
- High-quality translation using Meta's NLLB neural machine translation
- Preserves code blocks, markdown, and formatting
- Free and offline - local processing, no API keys needed

## Performance Metrics

The optimizer provides metrics for each request:

- **LLM Token Reduction**: Tokens saved on the LLM side (~65% for prompts ≥100 tokens)
- **Translation Time**: Time spent on JA→EN translation (typically 1-3s)
- **Time Overhead**: Translation time as percentage of total request time
- **Cost Savings**: Estimated cost reduction for paid APIs (GPT-4, Claude, etc.)

Note: Translation uses NLLB's internal tokenization (different from LLM tokens), so we track translation impact via time rather than token counts.

## When To Use

Best for:

- Long technical queries (>100 tokens)
- Code examples and documentation
- Detailed explanations

Not ideal for:

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
    llm_model="llama3.2:3b",
    optimization_threshold=50
)
```

## Architecture

```
JA prompt → EN translation → LLM (instructed: respond in JA) → JA output
         ↑ Saves tokens                                        ↑ Native quality
```

## Project Structure

```
llm_nmt-token-optimizer/
├── token_optimizer/          # Core library
│   ├── optimizer.py         # Main optimizer logic
│   ├── llm.py              # Ollama integration
│   ├── translation.py      # NLLB translation
│   ├── tokens.py           # Token counting
│   └── models.py           # Data models
├── api.py                   # FastAPI REST server
├── optimize.py             # Interactive CLI
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Python dependencies
└── examples/               # API client examples
    └── api_clients.md      # Python, JS, curl examples
```

## API Endpoints

- **POST /optimize** - Optimize a Japanese query
- **GET /health** - Health check endpoint
- **GET /** - API information
- **GET /docs** - Interactive API documentation (Swagger UI)
- **GET /redoc** - Alternative API docs (ReDoc)

## Troubleshooting

**"Could not connect to Ollama"**

- Ensure Ollama is installed: https://ollama.com/download
- Start Ollama server: `ollama serve`
- Verify it's running: `ollama list`

**"Model requires more system memory"**

- Close other applications to free RAM
- Try a smaller model: `ollama pull qwen2.5:1.5b`
- Use the smaller model: `TokenOptimizer(llm_model="qwen2.5:1.5b")`

**"NLLB model loading is slow"**

- First run downloads 600MB model (one-time)
- Subsequent runs load from cache (~10-20 seconds)
- Model stays in memory after first translation

**Translation seems stuck**

- NLLB processes on CPU (can be slow on older hardware)
- Typical translation time: 1-5s depending on text length
- Progress isn't shown during translation

## License

MIT License
