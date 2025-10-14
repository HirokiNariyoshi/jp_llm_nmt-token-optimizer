"""
Basic usage example of TokenOptimizer.
"""

import os
from token_optimizer import TokenOptimizer

def main():
    # Initialize the optimizer
    optimizer = TokenOptimizer(
        llm_provider="ollama",
        llm_model="qwen2.5:1.5b",  # Lightweight multilingual model with Japanese support
        translation_provider="google",
        cache_enabled=False,
        optimization_threshold=50
    )
    
    # Example prompt
    prompt = """
    Explain the concept of quantum entanglement in detail. 
    Include the historical development, key experiments, 
    mathematical foundations, and practical applications 
    in quantum computing and cryptography.
    """
    
    print("=" * 60)
    print("TokenOptimizer Example")
    print("=" * 60)
    
    # First, analyze potential savings
    print("\n📊 Analyzing potential savings...")
    analysis = optimizer.analyze_potential_savings(prompt, output_tokens=500)
    
    print(f"\nEnglish tokens: {analysis['english_input_tokens']}")
    print(f"Japanese tokens: {analysis['japanese_input_tokens']}")
    print(f"Token reduction: {analysis['token_reduction_percent']:.1f}%")
    print(f"Estimated cost savings: ${analysis['cost_saved']:.4f}")
    print(f"Recommendation: {analysis['recommendation']}")
    
    # Process the request
    print("\n🚀 Processing request with optimization...")
    response = optimizer.optimize_request(
        prompt=prompt,
        max_tokens=500
    )
    
    print("\n📝 Response:")
    print("-" * 60)
    print(response.content[:200] + "..." if len(response.content) > 200 else response.content)
    print("-" * 60)
    
    print("\n📈 Metrics:")
    print(f"Used optimization: {response.metrics.used_optimization}")
    print(f"Original tokens: {response.metrics.original_tokens}")
    print(f"Optimized tokens: {response.metrics.optimized_tokens}")
    print(f"Tokens saved: {response.metrics.tokens_saved}")
    print(f"Token reduction: {response.metrics.token_reduction_percent:.1f}%")
    print(f"Original cost: ${response.metrics.original_cost:.4f}")
    print(f"Optimized cost: ${response.metrics.optimized_cost:.4f}")
    print(f"Cost saved: ${response.metrics.cost_saved:.4f}")
    print(f"Translation time: {response.metrics.translation_time:.2f}s")
    print(f"LLM time: {response.metrics.llm_time:.2f}s")
    print(f"Total time: {response.metrics.total_time:.2f}s")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("Using Ollama (local, completely free!)")
    print("Make sure Ollama is running: ollama serve")
    print()
    main()
