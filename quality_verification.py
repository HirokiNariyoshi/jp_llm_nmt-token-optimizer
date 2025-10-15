"""
Quality Verification Tools for Translation-Optimized LLM Responses

Compares direct Japanese responses vs. translated (JA→EN→LLM→EN→JA) responses
to measure quality degradation from the translation optimization.
"""

from token_optimizer import TokenOptimizer
import time
from typing import Dict, Any


def verify_quality_side_by_side(
    japanese_prompt: str,
    llm_model: str = "qwen2.5:1.5b"
) -> Dict[str, Any]:
    """
    Run the same prompt through both paths and return both responses for comparison.
    
    Args:
        japanese_prompt: The Japanese query
        llm_model: Ollama model to use
        
    Returns:
        Dictionary with both responses and metadata
    """
    optimizer = TokenOptimizer(llm_model=llm_model)
    
    print("🔬 Quality Verification Test")
    print("=" * 70)
    print(f"\n📝 Prompt (Japanese):\n{japanese_prompt}\n")
    
    # Path 1: Direct Japanese (baseline)
    print("⏳ Running direct Japanese path (baseline)...")
    start_time = time.time()
    direct_response = optimizer.optimize_request(
        prompt=japanese_prompt,
        force_optimization=False  # Force direct path
    )
    direct_time = time.time() - start_time
    
    # Path 2: Optimized (JA→EN→LLM→EN→JA)
    print("⏳ Running optimized translation path...")
    start_time = time.time()
    optimized_response = optimizer.optimize_request(
        prompt=japanese_prompt,
        force_optimization=True  # Force optimization
    )
    optimized_time = time.time() - start_time
    
    # Display results
    print("\n" + "=" * 70)
    print("📊 RESULTS COMPARISON")
    print("=" * 70)
    
    print("\n🔵 DIRECT JAPANESE PATH (Baseline):")
    print(f"Response: {direct_response.content}")
    print(f"Tokens: {direct_response.metrics.total_tokens}")
    print(f"Time: {direct_time:.2f}s")
    
    print("\n🟢 OPTIMIZED PATH (JA→EN→LLM→EN→JA):")
    print(f"Response: {optimized_response.content}")
    print(f"Tokens: {optimized_response.metrics.total_tokens}")
    print(f"Time: {optimized_time:.2f}s")
    print(f"Token Savings: {optimized_response.metrics.tokens_saved} ({optimized_response.metrics.percent_saved:.1f}%)")
    
    print("\n" + "=" * 70)
    print("⚠️  MANUAL QUALITY ASSESSMENT NEEDED")
    print("=" * 70)
    print("Compare the two responses above:")
    print("1. Is the meaning preserved?")
    print("2. Are there any mistranslations?")
    print("3. Is the tone/style similar?")
    print("4. Are technical terms correct?")
    print("5. Overall quality: Similar / Slightly worse / Much worse?")
    
    return {
        "prompt": japanese_prompt,
        "direct": {
            "content": direct_response.content,
            "tokens": direct_response.metrics.total_tokens,
            "time": direct_time
        },
        "optimized": {
            "content": optimized_response.content,
            "tokens": optimized_response.metrics.total_tokens,
            "time": optimized_time,
            "savings": optimized_response.metrics.tokens_saved
        }
    }


def batch_quality_test(test_cases: list[str], llm_model: str = "qwen2.5:1.5b"):
    """
    Run multiple test cases and collect results.
    
    Args:
        test_cases: List of Japanese prompts to test
        llm_model: Ollama model to use
    """
    results = []
    
    for i, prompt in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"TEST CASE {i}/{len(test_cases)}")
        print(f"{'=' * 70}")
        
        result = verify_quality_side_by_side(prompt, llm_model)
        results.append(result)
        
        # Pause between tests to avoid overwhelming the model
        if i < len(test_cases):
            time.sleep(2)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 BATCH TEST SUMMARY")
    print("=" * 70)
    
    total_direct_tokens = sum(r["direct"]["tokens"] for r in results)
    total_optimized_tokens = sum(r["optimized"]["tokens"] for r in results)
    total_savings = total_direct_tokens - total_optimized_tokens
    percent_savings = (total_savings / total_direct_tokens * 100) if total_direct_tokens > 0 else 0
    
    print(f"\nTotal Test Cases: {len(test_cases)}")
    print(f"Direct Path Tokens: {total_direct_tokens}")
    print(f"Optimized Path Tokens: {total_optimized_tokens}")
    print(f"Total Savings: {total_savings} tokens ({percent_savings:.1f}%)")
    
    print("\n⚠️  Next Step: Human Quality Review")
    print("Review the responses above and assess translation quality impact.")
    
    return results


# Test cases covering different domains
TEST_CASES = [
    # Technical/Programming
    "Pythonでリストの内包表記を使って、1から10までの偶数のリストを作成する方法を教えてください。",
    
    # Business/Formal
    "来週の月曜日に予定されている会議について、アジェンダと参加者リストを準備する必要があります。効率的な方法を提案してください。",
    
    # Creative/Casual
    "週末に友達とキャンプに行く予定です。初心者向けのキャンプのコツを教えてください。",
    
    # Science/Academic
    "光合成のプロセスについて、中学生にもわかるように簡単に説明してください。",
    
    # Short/Simple
    "東京の人口は何人ですか？",
]


if __name__ == "__main__":
    print("🔬 LLM Translation Quality Verification Tool")
    print("=" * 70)
    print("\nThis tool compares:")
    print("  🔵 Direct: Japanese → LLM → Japanese (baseline)")
    print("  🟢 Optimized: Japanese → English → LLM → English → Japanese")
    print("\nYou can then manually assess quality differences.\n")
    
    # Single test
    print("Running single test example...\n")
    verify_quality_side_by_side(
        "量子コンピューティングの基本原理について説明してください。"
    )
    
    # Uncomment to run batch tests
    # print("\n" + "=" * 70)
    # print("Running batch tests...")
    # batch_quality_test(TEST_CASES)
