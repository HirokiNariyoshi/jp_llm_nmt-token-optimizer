"""
Quick Quality Test - Simple comparison of direct vs optimized responses
"""

from token_optimizer import TokenOptimizer
import time

def quick_quality_test():
    """Run a quick quality comparison test."""
    
    # Simple test prompt
    test_prompt = "Pythonで1から10までの偶数のリストを作る方法を教えてください。"
    
    print("=" * 70)
    print("🔬 Quick Quality Test")
    print("=" * 70)
    print(f"\n📝 Test Prompt (Japanese):")
    print(f"   {test_prompt}")
    print()
    
    optimizer = TokenOptimizer(llm_model="qwen2.5:1.5b")
    
    # Test 1: Direct path (force_optimization=False)
    print("⏳ Testing Direct Path (Japanese → LLM → Japanese)...")
    start = time.time()
    direct = optimizer.optimize_request(
        prompt=test_prompt,
        max_tokens=200,
        force_optimization=False
    )
    direct_time = time.time() - start
    
    print(f"✅ Direct completed in {direct_time:.1f}s")
    print()
    
    # Test 2: Optimized path (force_optimization=True)
    print("⏳ Testing Optimized Path (JA → EN → LLM → EN → JA)...")
    start = time.time()
    optimized = optimizer.optimize_request(
        prompt=test_prompt,
        max_tokens=200,
        force_optimization=True
    )
    optimized_time = time.time() - start
    
    print(f"✅ Optimized completed in {optimized_time:.1f}s")
    print()
    
    # Display results
    print("=" * 70)
    print("📊 RESULTS COMPARISON")
    print("=" * 70)
    
    print("\n🔵 DIRECT PATH (Baseline):")
    print("-" * 70)
    print(direct.content)
    print("-" * 70)
    print(f"Tokens: {direct.metrics.original_tokens}")
    print(f"Time: {direct_time:.1f}s")
    
    print("\n🟢 OPTIMIZED PATH (Translation):")
    print("-" * 70)
    print(optimized.content)
    print("-" * 70)
    print(f"Tokens: {optimized.metrics.optimized_tokens}")
    print(f"Time: {optimized_time:.1f}s")
    print(f"Savings: {optimized.metrics.tokens_saved} tokens ({optimized.metrics.token_reduction_percent:.1f}%)")
    
    print("\n" + "=" * 70)
    print("💭 MANUAL QUALITY ASSESSMENT")
    print("=" * 70)
    print("""
Compare the two responses above and assess:

1. ✓ Correctness - Do both give the right answer?
2. ✓ Completeness - Is all information preserved?
3. ✓ Natural Language - Does the optimized version sound natural?
4. ✓ Code Quality - If code is included, is it correct?
5. ✓ Overall - Would you notice a difference without seeing both?

Rate the quality:
[ ] Excellent - No noticeable difference
[ ] Good - Minor differences, both acceptable
[ ] Acceptable - Some quality loss but usable
[ ] Poor - Significant quality degradation

Document your assessment in TESTING_RESULTS.md
    """)
    
    # Calculate length ratio
    len_ratio = min(len(direct.content), len(optimized.content)) / max(len(direct.content), len(optimized.content))
    
    print(f"\n📏 Length Ratio: {len_ratio:.2f}")
    print(f"   (1.0 = same length, lower = more difference)")
    
    return {
        "direct": direct.content,
        "optimized": optimized.content,
        "savings": optimized.metrics.tokens_saved,
        "percent_saved": optimized.metrics.token_reduction_percent
    }

if __name__ == "__main__":
    print("\n🧪 Running Quick Quality Test...")
    print("This will compare direct vs optimized responses.\n")
    
    try:
        results = quick_quality_test()
        
        print("\n✅ Test complete!")
        print(f"\nToken savings: {results['savings']} ({results['percent_saved']:.1f}%)")
        print("\nNext step: Review the responses above and assess quality.")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        print("\nMake sure:")
        print("1. Ollama is running (ollama serve)")
        print("2. Model is downloaded (ollama pull qwen2.5:1.5b)")
