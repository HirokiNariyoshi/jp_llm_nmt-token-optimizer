# Ollama Setup Guide - Local & Free

This project uses Ollama to run models locally for testing and development. **No API keys required, completely free!**

For Japanese query optimization, the system translates Japanese→English to reduce token usage with English-optimized models.

## Step 1: Install Ollama

### Windows:

1. Go to https://ollama.com/download
2. Download and run the Windows installer
3. Ollama will start automatically

### Verify Installation:

```powershell
ollama --version
```

## Step 2: Download Qwen2.5 Model

Qwen2.5 1.5B is a lightweight multilingual model with good Japanese support:

```powershell
ollama pull qwen2.5:1.5b
```

This downloads the model (~986MB) - only needed once!

## Step 3: Start Ollama Server

Ollama should start automatically, but if needed:

```powershell
ollama serve
```

## Step 4: Run the Optimizer

```powershell
# Interactive mode - enter your own Japanese query
python optimize.py

# Or edit optimize.py and set TEST_MODE = True for demo
# Set COMPARE_MODE = True to query both paths for accurate measurement
```

### Recommended Models:

- **qwen2.5:1.5b** (default) - Lightweight, good Japanese support (~986MB)
- **qwen2.5:7b** - More capable but requires more RAM (~4.7GB)
- **gemma2:2b** - Google's lightweight model (~1.6GB)
- **gemma2:9b** - Larger version (~5.4GB)


### Download a model:

```powershell
ollama pull qwen2.5:1.5b
```

### List installed models:

```powershell
ollama list
```

### Change model in code:

```python
optimizer = TokenOptimizer(
    llm_model="qwen2.5:7b"  # Larger model for better quality
)
```

## Why Ollama?

✅ **Completely FREE** - No API costs (im broke)
✅ **Privacy** - Everything runs locally on your machine
✅ **No limits** - Use as much as you want
✅ **Fast** - Good performance with lightweight models
✅ **Easy testing** - Perfect for development and validation

## System Requirements

- **Minimum:** 4GB RAM (for qwen2.5:1.5b)
- **Recommended:** 8GB+ RAM (for larger models)
- **Storage:** 1-5GB per model

## Troubleshooting

### Error: "Could not connect to Ollama"

```powershell
# Make sure Ollama is running
ollama serve
```

### Model not found

```powershell
# Download the model first
ollama pull qwen2.5:1.5b
```

### Slow performance

- Use smaller models (qwen2.5:1.5b instead of :7b)
- Close other applications
- Upgrade RAM if possible

## Next Steps

Now that Ollama is set up, you can test Japanese query optimization:

```powershell
# Interactive mode
python optimize.py

# Test mode (edit optimize.py and set TEST_MODE = True)
python optimize.py

# Compare mode for accurate measurement (set COMPARE_MODE = True)
python optimize.py
```

Expected results: **20% or more token savings** when translating Japanese to English for processing!
