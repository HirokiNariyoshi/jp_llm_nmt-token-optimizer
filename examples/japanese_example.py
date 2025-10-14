"""
Example demonstrating Japanese query optimization.
Shows how translating to English reduces token usage.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from token_optimizer import TokenOptimizer


def main():
    # Initialize optimizer
    optimizer = TokenOptimizer(
        llm_provider="ollama",
        llm_model="qwen2.5:1.5b",
        translation_provider="google",
        optimization_threshold=10  # Low threshold for demo
    )
    
    # Japanese technical query
    japanese_prompt = """
    量子コンピューティングについて詳しく説明してください。
    歴史的な発展、主要な実験、数学的基礎、
    量子計算と暗号化における実用的な応用を含めてください。
    """
    
    print("=" * 70)
    print("Japanese Query Optimization Demo")
    print("=" * 70)
    print()
    print("📝 Japanese Input:")
    print(japanese_prompt.strip())
    print()
    
    # Analyze potential savings
    print("📊 Analyzing token efficiency...")
    analysis = optimizer.analyze_potential_savings(japanese_prompt, output_tokens=500)
    
    print(f"\n  Japanese tokens: {analysis['japanese_input_tokens']}")
    print(f"  English tokens:  {analysis['english_input_tokens']}")
    print(f"  Tokens saved:    {analysis['input_tokens_saved']} ({analysis['token_reduction_percent']:.1f}%)")
    print(f"  Cost saved:      ${analysis['cost_saved']:.6f}")
    print(f"  Recommendation:  {analysis['recommendation']}")
    
    # Process request
    print("\n🚀 Processing with optimization...")
    response = optimizer.optimize_request(
        prompt=japanese_prompt,
        max_tokens=500
    )
    
    print("\n" + "=" * 70)
    print("Results")
    print("=" * 70)
    print()
    print("📝 Japanese Response:")
    print(response.content[:300] + "..." if len(response.content) > 300 else response.content)
    print()
    
    print("📈 Optimization Metrics:")
    print(f"  Used optimization:  {response.metrics.used_optimization}")
    print(f"  Original tokens:    {response.metrics.original_tokens}")
    print(f"  Optimized tokens:   {response.metrics.optimized_tokens}")
    print(f"  Tokens saved:       {response.metrics.tokens_saved}")
    print(f"  Token reduction:    {response.metrics.token_reduction_percent:.1f}%")
    print(f"  Cost saved:         ${response.metrics.cost_saved:.6f}")
    print(f"  Translation time:   {response.metrics.translation_time:.2f}s")
    print(f"  LLM time:           {response.metrics.llm_time:.2f}s")
    print(f"  Total time:         {response.metrics.total_time:.2f}s")
    print()
    
    if response.metrics.tokens_saved > 0:
        print("✅ Success! English translation reduced token usage.")
        print(f"   This saves ~{response.metrics.token_reduction_percent:.1f}% on API costs.")
    else:
        print("ℹ️  Optimization not beneficial for this query.")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("Japanese Query Optimizer for English-Optimized LLMs")
    print("Make sure Ollama is running: ollama serve")
    print()
    main()
