# Quick Start - Install Ollama and Test

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Token Optimizer - Ollama Setup" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is installed
Write-Host "Checking for Ollama..." -ForegroundColor Yellow
$ollamaInstalled = Get-Command ollama -ErrorAction SilentlyContinue

if (-not $ollamaInstalled) {
    Write-Host "❌ Ollama not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Ollama:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://ollama.com/download" -ForegroundColor White
    Write-Host "2. Download and install for Windows" -ForegroundColor White
    Write-Host "3. Run this script again" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Ollama is installed!" -ForegroundColor Green
Write-Host ""

# Check if qwen2.5:7b is downloaded
Write-Host "Checking for Qwen2.5 model..." -ForegroundColor Yellow
$models = ollama list
if ($models -match "qwen2.5:7b") {
    Write-Host "✅ Qwen2.5:7b is already downloaded!" -ForegroundColor Green
}
else {
    Write-Host "⏬ Downloading Qwen2.5:7b (~4.7GB)..." -ForegroundColor Yellow
    Write-Host "This may take a few minutes..." -ForegroundColor Gray
    ollama pull qwen2.5:7b
    Write-Host "✅ Download complete!" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Ready to test!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Run basic example
Write-Host "Running basic example..." -ForegroundColor Yellow
Write-Host ""
python examples\basic_usage.py

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Try other examples:" -ForegroundColor Yellow
Write-Host "  python examples\comparison.py" -ForegroundColor White
Write-Host "  python examples\conversational_demo.py" -ForegroundColor White
Write-Host ""
