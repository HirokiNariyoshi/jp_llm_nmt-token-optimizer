"""
Test with realistic longer prompt to see token optimization benefits
"""

from token_optimizer import TokenOptimizer
from deep_translator import GoogleTranslator
import tiktoken

# Realistic longer prompt
LONG_PROMPT = """
日本の企業が新しいウェブアプリケーションを開発する際に、
セキュリティとパフォーマンスを両立させるためのベストプラクティスを
詳しく説明してください。特に以下の点について：

1. ユーザー認証とアクセス制御の実装方法
2. データベースのクエリ最適化とインデックス設計
3. フロントエンドとバックエンドの通信の暗号化
4. スケーラビリティを考慮したアーキテクチャ設計
5. セッション管理とCSRF対策

具体的なコード例とともに、それぞれの実装における注意点も含めて
教えてください。
"""

def test_realistic():
    translator = GoogleTranslator(source='ja', target='en')
    enc = tiktoken.get_encoding("cl100k_base")
    
    # Translate and count tokens
    en_prompt = translator.translate(LONG_PROMPT)
    
    ja_tokens = len(enc.encode(LONG_PROMPT))
    en_tokens = len(enc.encode(en_prompt))
    
    savings = ja_tokens - en_tokens
    percent = (savings / ja_tokens) * 100
    
    print("=" * 70)
    print("📝 REALISTIC LONG PROMPT TEST")
    print("=" * 70)
    
    print(f"\n🇯🇵 Japanese Prompt:")
    print(LONG_PROMPT)
    print(f"\n📊 Japanese Tokens: {ja_tokens}")
    
    print(f"\n🇬🇧 English Translation:")
    print(en_prompt)
    print(f"\n📊 English Tokens: {en_tokens}")
    
    print(f"\n💾 Token Savings: {savings} tokens ({percent:.1f}%)")
    
    if savings > 0:
        print("✅ Optimization would save tokens on INPUT")
    else:
        print("❌ Optimization would INCREASE tokens on INPUT")
    
    # Now test actual response
    print("\n" + "=" * 70)
    print("🔬 Testing Actual Responses...")
    print("=" * 70)
    
    optimizer = TokenOptimizer(llm_model="qwen2.5:1.5b")
    
    print("\n⏳ Running optimized request...")
    result = optimizer.optimize_request(
        prompt=LONG_PROMPT,
        max_tokens=500,
        force_optimization=True
    )
    
    print(f"\n📊 Results:")
    print(f"   Original tokens: {result.metrics.original_tokens}")
    print(f"   Optimized tokens: {result.metrics.optimized_tokens}")
    print(f"   Tokens saved: {result.metrics.tokens_saved}")
    print(f"   Reduction: {result.metrics.token_reduction_percent:.1f}%")
    
    print(f"\n⏱️  Timing:")
    print(f"   Translation: {result.metrics.translation_time:.2f}s")
    print(f"   LLM: {result.metrics.llm_time:.2f}s")
    print(f"   Total: {result.metrics.total_time:.2f}s")
    
    print(f"\n📝 Response Preview:")
    print(result.content[:500] + "..." if len(result.content) > 500 else result.content)

if __name__ == "__main__":
    test_realistic()
