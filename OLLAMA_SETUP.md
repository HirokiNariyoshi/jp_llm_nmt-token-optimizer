# Ollama Setup Guide - Completely FREE!

This project now uses Ollama to run models locally on your computer. **No API keys, no costs, completely free forever!**

## Step 1: Install Ollama

### Windows:

1. Go to https://ollama.com/download
2. Download and run the Windows installer
3. Ollama will start automatically

### Verify Installation:

```powershell
ollama --version
```

## Step 2: Download Gemma2 Model

Gemma2 is a multilingual model with excellent Japanese support:

```powershell
ollama pull gemma2:2b
```

This downloads the model (~1.6GB) - only needed once!

## Step 3: Start Ollama Server

Ollama should start automatically, but if needed:

```powershell
ollama serve
```

## Step 4: Run the Examples

```powershell
# Basic example
python examples\basic_usage.py

# Comparison (testing Japanese optimization!)
python examples\comparison.py

# Long prompt
python examples\long_prompt_demo.py

# Pure conversational
python examples\conversational_demo.py
```

## Available Models

### Multilingual (Recommended for Japanese):

- **gemma2:2b** (default) - Google's lightweight multilingual model with Japanese support
- **gemma2:9b** - Larger, more capable version
- **qwen2.5:1.5b** - Alibaba's lightweight multilingual model

### Alternative Models:

- **mistral:7b** - Good general model
- **llama3.2:3b** - Meta's model

### Download a model:

```powershell
ollama pull gemma2:2b
```

### List installed models:

```powershell
ollama list
```

### Change model in code:

```python
optimizer = TokenOptimizer(
    llm_provider="ollama",
    llm_model="gemma2:9b"  # Larger model
)
```

## Why Ollama + Gemma2?

✅ **Completely FREE** - No API costs ever
✅ **Japanese Support** - Gemma2 has excellent multilingual capabilities including Japanese
✅ **Privacy** - Everything runs on your PC
✅ **No limits** - Use as much as you want
✅ **Fast** - Lightweight models work well even with limited RAM

## System Requirements

- **Minimum:** 4GB RAM (for gemma2:2b)
- **Recommended:** 8GB RAM
- **Storage:** 2-10GB per model

## Troubleshooting

### Error: "Could not connect to Ollama"

```powershell
# Make sure Ollama is running
ollama serve
```

### Model not found

```powershell
# Download the model first
ollama pull gemma2:2b
```

### Slow performance

- Use smaller models (gemma2:2b instead of :9b)
- Close other applications
- Upgrade RAM if possible

## Next Steps

Now that Ollama is set up, you can test if **Japanese shows better token compression** than English!

Try running `python examples\basic_usage.py` to see the results!
