"""
Japanese Query Optimizer - Main Interactive Script

Demonstrates token savings by translating Japanese queries to English
for processing by English-optimized LLMs.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from token_optimizer import TokenOptimizer

# Configuration
TEST_MODE = False  # Set to True to use hardcoded example
COMPARE_MODE = False  # Set to True to query both paths for accurate comparison (2x slower)

# Test prompt (long conversational example)
TEST_PROMPT = """
来月、親友のサプライズバースデーパーティーを企画していますが、
創造的なアイデアが必要です。彼女は30歳になり、アウトドア活動、
ヴィンテージの美学、植物やガーデニングに関連することが大好きです。
仕事のストレスや個人的な課題で大変な一年を過ごしてきたので、
本当に特別なものにしたいと思っています。

パーティーは私の庭で行う予定です。庭にはたくさんの花や木があり、
かなり広いスペースがあります。夕暮れ時、おそらく午後6時頃に
何かできればと思っています。照明が本当に美しい時間帯です。
約25人が来る予定で、ほとんどが大学時代の親しい友人と、
彼女が本当に気に入っている同僚数人です。

予算は800ドルから1000ドルで、豪華で高価なものよりも、
親密で個人的な雰囲気にしたいと考えています。彼女は大音量の音楽や
派手なものは好きではないので、良い食事、温かい会話、そして
私たちみんながどれだけ彼女を大切に思っているかを示す
心のこもった演出のある、居心地の良いガーデンパーティーを
考えています。

装飾、アクティビティ、食事の選択肢、そして彼女を本当に愛されていると
感じさせる特別な瞬間やサプライズ要素のアイデアをブレインストーミング
するのを手伝っていただけますか？また、彼女は非常に観察力があり、
通常は物事を見抜いてしまうので、彼女に気づかれずにすべてを調整する
ためのヒントもいただけると助かります。
"""


def main():
    print("=" * 70)
    print("Japanese Query Optimizer")
    print("Reduces token usage by ~58% for English-optimized LLMs")
    print("=" * 70)
    print()
    
    # Initialize optimizer
    optimizer = TokenOptimizer(
        llm_provider="ollama",
        llm_model="qwen2.5:1.5b",
        translation_provider="google",
        cache_enabled=False,
        optimization_threshold=10
    )
    
    # Get prompt based on mode
    if TEST_MODE:
        print("📝 Using test mode with hardcoded prompt")
        print()
        japanese_prompt = TEST_PROMPT
        print("Prompt preview:")
        print(japanese_prompt[:200] + "...\n")
    else:
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
    print(f"📊 Analyzing query ({word_count} words)...")
    print()
    
    # Analyze potential savings
    analysis = optimizer.analyze_potential_savings(japanese_prompt, output_tokens=500)
    
    print("Token Efficiency Analysis:")
    print(f"  Japanese tokens:  {analysis['japanese_input_tokens']}")
    print(f"  English tokens:   {analysis['english_input_tokens']}")
    print(f"  Tokens saved:     {analysis['input_tokens_saved']} ({analysis['token_reduction_percent']:.1f}%)")
    print(f"  Cost saved:       ${analysis['cost_saved']:.6f}")
    print(f"  Recommendation:   {analysis['recommendation']}")
    print()
    
    if analysis['input_tokens_saved'] <= 0:
        print("⚠️  English translation would not save tokens for this query.")
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
        print()
    
    # Process request
    if COMPARE_MODE:
        print("🚀 Processing with compare mode (querying both paths)...")
        print("   This queries the model twice for accurate measurement")
    else:
        print("🚀 Processing with optimization...")
    print()
    
    response = optimizer.optimize_request(
        prompt=japanese_prompt,
        max_tokens=800 if TEST_MODE else 500,
        compare_mode=COMPARE_MODE
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
    print(f"  Translation time: {metrics.translation_time:.2f}s")
    print(f"  LLM time:         {metrics.llm_time:.2f}s")
    print(f"  Total time:       {metrics.total_time:.2f}s")
    print()
    
    # Status summary
    if COMPARE_MODE:
        print("ℹ️  Compare mode: Token counts are from actual model responses")
        print("   (not tiktoken estimates)")
        print()
    
    if metrics.used_optimization:
        if metrics.tokens_saved > 0:
            print("✅ Optimization successful! English translation reduced token usage.")
            print(f"   For high-volume applications, this saves ~{metrics.token_reduction_percent:.1f}% on API costs.")
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
