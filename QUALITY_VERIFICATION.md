# Quality Verification Guide
## 🔬 How to Verify Quality

### Method 1: Manual Side-by-Side Comparison (Most Reliable)

Run the same prompt through both paths and compare:

```bash
python quality_verification.py
```

This will show you:
- 🔵 **Direct path**: Japanese → LLM → Japanese (baseline)
- 🟢 **Optimized path**: Japanese → English → LLM → English → Japanese

You can then **manually judge** which response is better.

**Test across different domains:**
- Technical questions (programming, science)
- Business/formal communication
- Creative/casual queries
- Factual questions

### Method 2: Semantic Similarity (Automated)

Install semantic similarity tools:

```bash
pip install sentence-transformers numpy
```

Then run automated quality checks:

```bash
python quality_metrics.py
```

This uses embeddings to calculate **semantic similarity** between responses:
- **0.95-1.00**: Nearly identical (excellent!)
- **0.90-0.95**: Minor differences (very good)
- **0.85-0.90**: Noticeable but acceptable
- **0.80-0.85**: Borderline - review needed
- **< 0.80**: Significant quality loss