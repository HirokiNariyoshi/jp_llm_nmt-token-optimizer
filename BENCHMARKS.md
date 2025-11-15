# Performance Benchmarks

## Token Reduction Analysis

Benchmark results across different prompt sizes using Llama 3.2 3B model.

### Test Results

| Prompt Size | Original Tokens | Optimized Tokens | Reduction | Translation Time | Total Time |
|-------------|----------------|------------------|-----------|------------------|------------|
| Short (50 tokens) | 53 | 48 | 9.4% | 1.2s | 8.5s |
| Medium (100 tokens) | 105 | 42 | 60.0% | 1.8s | 10.2s |
| Long (200 tokens) | 212 | 78 | 63.2% | 2.5s | 12.8s |
| Very Long (500 tokens) | 534 | 186 | 65.2% | 4.1s | 18.3s |

### Key Findings

1. **Optimal Range**: Best results with prompts >100 tokens (60-65% reduction)
2. **Translation Overhead**: Typically 15-25% of total request time
3. **Break-even Point**: ~50 tokens (below this, English may be longer than Japanese)
4. **Consistency**: Token reduction remains stable at ~65% for prompts >200 tokens

## Cost Savings Analysis

Based on GPT-4 pricing ($0.03/1K input tokens):

| Monthly Volume | Without Optimizer | With Optimizer | Monthly Savings | Annual Savings |
|----------------|-------------------|----------------|-----------------|----------------|
| 1M tokens | $30 | $10.50 | $19.50 | $234 |
| 10M tokens | $300 | $105 | $195 | $2,340 |
| 100M tokens | $3,000 | $1,050 | $1,950 | $23,400 |
| 1B tokens | $30,000 | $10,500 | $19,500 | $234,000 |

## Comparison with Alternatives

| Approach | Token Reduction | Translation Quality | Setup Complexity | Cost |
|----------|----------------|---------------------|------------------|------|
| **This Optimizer** | ~65% | High (NLLB) | Low | Free |
| Direct Japanese | 0% | Native | None | Baseline |
| Basic MT (Google Translate API) | ~60% | Medium | Low | $20/1M chars |
| GPT-4 Translation | ~65% | Highest | Medium | $30/1M tokens |

## Real-World Example

**Prompt**: "Pythonで機械学習モデルを作成し、scikit-learnを使ってランダムフォレスト分類器を実装する方法を、サンプルコード付きで詳しく説明してください。"

**Results**:
- Original (Japanese): 86 tokens
- Optimized (English): 39 tokens
- Reduction: 54.7%
- Translation time: 3.2s
- Total time: 12.7s
- Cost savings: 54.7% on GPT-4 API calls

## Test Environment

- **Model**: Llama 3.2 3B (via Ollama)
- **Translation**: NLLB-200 distilled 600M
- **Hardware**: AMD Ryzen 9 5900X, 32GB RAM
- **Python**: 3.10
- **Date**: November 2025

## Methodology

1. Test prompts curated from real-world Japanese technical queries
2. Each prompt tested 3 times, median values reported
3. Token counting using tiktoken (cl100k_base)
4. Translation time measured separately from LLM inference time
5. Cost estimates based on current GPT-4 pricing

## Limitations

1. Results may vary with different LLM models
2. Translation quality depends on domain (technical content performs best)
3. Very short prompts (<50 tokens) may not benefit from optimization
4. Translation adds latency (not suitable for real-time streaming applications)
