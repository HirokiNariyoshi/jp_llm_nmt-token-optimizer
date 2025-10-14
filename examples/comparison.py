"""
Compare performance with and without optimization.
"""

import os
import sys
from token_optimizer import TokenOptimizer

def compare_approaches():
    """Compare direct vs optimized approaches."""
    
    optimizer = TokenOptimizer(
        llm_provider="ollama",
        llm_model="qwen2.5:1.5b",  # Lightweight model
        translation_provider="google",
        cache_enabled=False,
        optimization_threshold=1
    )
    
    # Test prompt
    prompt = """
    Write a comprehensive guide on machine learning model deployment best practices.
    Include sections on containerization, CI/CD pipelines, monitoring, scaling,
    and security considerations.
    """
    
    print("=" * 80)
    print("COMPARISON: Direct vs Optimized LLM Requests")
    print("=" * 80)
    
    # Direct request (force no optimization)
    print("\n🔵 Direct Request (English only)...")
    direct_response = optimizer.optimize_request(
        prompt=prompt,
        max_tokens=400,
        force_optimization=False
    )
    
    print("\n🟢 Optimized Request (EN → JA → LLM → JA → EN)...")
    optimized_response = optimizer.optimize_request(
        prompt=prompt,
        max_tokens=400,
        force_optimization=True
    )
    
    # Print comparison
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    print("\n📊 Token Usage:")
    print(f"{'Metric':<30} {'Direct':<15} {'Optimized':<15} {'Savings':<15}")
    print("-" * 80)
    print(f"{'Input tokens':<30} {direct_response.metrics.original_tokens:<15} "
          f"{optimized_response.metrics.optimized_tokens:<15} "
          f"{optimized_response.metrics.tokens_saved:<15}")
    print(f"{'Token reduction':<30} {'0%':<15} "
          f"{optimized_response.metrics.token_reduction_percent:.1f}%")
    
    print("\n💰 Cost Analysis:")
    print(f"{'Metric':<30} {'Direct':<15} {'Optimized':<15} {'Savings':<15}")
    print("-" * 80)
    print(f"{'Total cost':<30} ${direct_response.metrics.original_cost:<14.4f} "
          f"${optimized_response.metrics.optimized_cost:<14.4f} "
          f"${optimized_response.metrics.cost_saved:<14.4f}")
    print(f"{'Cost reduction':<30} {'0%':<15} "
          f"{optimized_response.metrics.cost_reduction_percent:.1f}%")
    
    print("\n⏱️  Time Analysis:")
    print(f"{'Metric':<30} {'Direct':<15} {'Optimized':<15} {'Overhead':<15}")
    print("-" * 80)
    print(f"{'Translation time':<30} {'-':<15} "
          f"{optimized_response.metrics.translation_time:.2f}s")
    print(f"{'LLM time':<30} {direct_response.metrics.llm_time:.2f}s"
          f"{optimized_response.metrics.llm_time:>15.2f}s")
    print(f"{'Total time':<30} {direct_response.metrics.total_time:.2f}s"
          f"{optimized_response.metrics.total_time:>15.2f}s"
          f"{optimized_response.metrics.total_time - direct_response.metrics.total_time:>15.2f}s")
    
    print("\n" + "=" * 80)
    print("\n✨ Summary:")
    if optimized_response.metrics.cost_saved > 0:
        print(f"✅ Optimization saved ${optimized_response.metrics.cost_saved:.4f} "
              f"({optimized_response.metrics.cost_reduction_percent:.1f}%)")
        print(f"✅ Token reduction: {optimized_response.metrics.token_reduction_percent:.1f}%")
        
        time_overhead = optimized_response.metrics.total_time - direct_response.metrics.total_time
        print(f"⚠️  Time overhead: {time_overhead:.2f}s due to translation")
    else:
        print("❌ Optimization did not provide savings for this request")
    
    print("=" * 80)


if __name__ == "__main__":
    print("Using Ollama with Gemma2 (multilingual with Japanese support!)")
    print("Make sure Ollama is running: ollama serve")
    print()
    compare_approaches()
