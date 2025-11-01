"""
Japanese Query Optimizer - Interactive CLI

Demonstrates token savings by translating Japanese queries to English
for processing by English-optimized LLMs.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from token_optimizer import TokenOptimizer


def main():
    print("=" * 70)
    print("Japanese Query Optimizer")
    print("Reduces LLM token usage by ~65% for English-optimized LLMs")
    print("=" * 70)
    print()
    
    # Initialize optimizer
    optimizer = TokenOptimizer(
        llm_model="llama3.2:3b",
        optimization_threshold=50
    )
    
    # Get user input
    print("📝 Enter your Japanese query (press Enter twice when done):")
    print()
    lines = []
    while True:
        line = input()
        if line == "" and len(lines) > 0:
            break
        if line:
            lines.append(line)
    japanese_prompt = "\n".join(lines)
    
    if not japanese_prompt.strip():
        print("❌ No prompt entered. Exiting.")
        return
    print()
    
    # Word count
    word_count = len(japanese_prompt.split())
    print(f"📊 Processing query ({word_count} words)...")
    print()
    
    # Process request
    print("🚀 Optimizing with translation...")
    print()
    
    response = optimizer.optimize_request(
        prompt=japanese_prompt,
        max_tokens=500
    )
    
    # Display results
    print("=" * 70)
    print("RESPONSE")
    print("=" * 70)
    print()
    
    # Show first 500 chars
    if len(response.content) > 500:
        print(response.content[:500] + "...")
        print(f"\n(Response truncated - {len(response.content)} total characters)")
    else:
        print(response.content)
    
    print()
    print("=" * 70)
    print("OPTIMIZATION METRICS")
    print("=" * 70)
    print()
    
    metrics = response.metrics
    
    # Token analysis
    print("📊 TOKEN USAGE:")
    print(f"  Original tokens:  {metrics.original_tokens}")
    print(f"  Optimized tokens: {metrics.optimized_tokens}")
    print(f"  Tokens saved:     {metrics.tokens_saved}")
    print(f"  Reduction:        {metrics.token_reduction_percent:.1f}%")
    print()
    
    # Cost analysis
    print("💰 COST SAVINGS:")
    print(f"  Without optimization: ${metrics.original_cost:.6f}")
    print(f"  With optimization:    ${metrics.optimized_cost:.6f}")
    print(f"  Saved:                ${metrics.cost_saved:.6f}")
    print(f"  Cost reduction:       {metrics.cost_reduction_percent:.1f}%")
    print()
    
    # Time analysis
    print("⏱️  PERFORMANCE:")
    print(f"  Translation time: {metrics.translation_time:.2f}s ({metrics.time_overhead_percent:.1f}% of total)")
    print(f"  LLM time:         {metrics.llm_time:.2f}s")
    print(f"  Total time:       {metrics.total_time:.2f}s")
    print()
    
    # Status summary
    if metrics.used_optimization:
        if metrics.tokens_saved > 0:
            print("✅ Optimization successful! English translation reduced LLM token usage.")
            print(f"   Token reduction: {metrics.token_reduction_percent:.1f}%")
            print(f"   Translation overhead: {metrics.translation_time:.1f}s ({metrics.time_overhead_percent:.0f}% of time)")
        else:
            print("⚠️  Optimization used but no savings (English similar to Japanese for this query)")
    else:
        print("ℹ️  Direct Japanese used (was more efficient than translating)")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    print("Make sure Ollama is running: ollama serve")
    print()
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
