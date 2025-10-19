"""
Comprehensive token optimization test with NLLB vs Google Translate
Tests with realistic long prompts to measure actual performance
"""

import time
from token_optimizer import TokenOptimizer
from token_optimizer.translation import GoogleTranslator, NLLBTranslator
import tiktoken

# Realistic test prompts (various lengths)
test_cases = [
    {
        "name": "Long technical documentation",
        "prompt": """
日本の企業が新しいウェブアプリケーションを開発する際に、
セキュリティとパフォーマンスを両立させるためのベストプラクティスを
詳しく説明してください。特に以下の点について：

1. ユーザー認証とアクセス制御の実装方法
2. データベースのクエリ最適化とインデックス設計
3. フロントエンドとバックエンドの通信の暗号化
4. スケーラビリティを考慮したアーキテクチャ設計
5. セッション管理とCSRF対策

具体的なコード例とともに、それぞれの実装における注意点も含めて教えてください。
"""
    },
    {
        "name": "Machine learning explanation",
        "prompt": """
Pythonで機械学習モデルを構築する際の一般的なワークフローについて、
初心者にもわかりやすく段階的に説明してください。

特に以下のステップについて詳しく解説してください：
- データの収集と前処理の方法
- 特徴量エンジニアリングの重要性
- モデルの選択基準
- ハイパーパラメータのチューニング
- モデルの評価方法と過学習の防止

各ステップで使用する主要なライブラリ（scikit-learn、pandas、numpyなど）
についても触れながら、実践的なコード例を含めて説明してください。
"""
    },
    {
        "name": "API development guide",
        "prompt": """
RESTful APIを設計する際のベストプラクティスについて教えてください。

以下の観点から詳しく説明してください：
- HTTPメソッド（GET、POST、PUT、DELETE）の適切な使い分け
- エンドポイントの命名規則とURL設計
- バージョニング戦略
- エラーハンドリングとステータスコードの使い方
- 認証と認可（JWT、OAuth2.0など）
- レート制限とキャッシング戦略
- ドキュメントの作成方法（Swagger/OpenAPIの活用）

FastAPIまたはFlaskを使用した実装例も含めて、実践的な内容でお願いします。
"""
    }
]

def count_tokens(text):
    """Count tokens using tiktoken (cl100k_base encoding)"""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def test_comprehensive_optimization():
    """Test full optimization with long prompts"""
    print("=" * 80)
    print("🔬 Comprehensive Token Optimization Test: NLLB vs Google Translate")
    print("=" * 80)
    
    # Initialize translators
    try:
        nllb = NLLBTranslator()
        nllb_available = True
        print("✅ NLLB loaded successfully\n")
    except:
        nllb_available = False
        print("❌ NLLB not available, using Google only\n")
    
    google = GoogleTranslator()
    
    total_google_savings = 0
    total_nllb_savings = 0
    total_ja_tokens = 0
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}/{len(test_cases)}: {test['name']}")
        print(f"{'='*80}")
        
        prompt = test['prompt'].strip()
        
        # Count Japanese tokens
        ja_tokens = count_tokens(prompt)
        print(f"\n📝 Japanese prompt: {ja_tokens} tokens")
        print(f"   Preview: {prompt[:100]}...")
        
        # Google Translate
        print(f"\n🔵 Google Translate:")
        google_result = google.translate(prompt, "ja", "en")
        google_tokens = count_tokens(google_result.text)
        google_savings = ja_tokens - google_tokens
        google_percent = (google_savings / ja_tokens) * 100
        
        print(f"   English: {google_tokens} tokens")
        print(f"   Savings: {google_savings} tokens ({google_percent:.1f}%)")
        print(f"   Preview: {google_result.text[:100]}...")
        
        # NLLB
        if nllb_available:
            print(f"\n🟢 NLLB:")
            nllb_result = nllb.translate(prompt, "ja", "en")
            nllb_tokens = count_tokens(nllb_result.text)
            nllb_savings = ja_tokens - nllb_tokens
            nllb_percent = (nllb_savings / ja_tokens) * 100
            
            print(f"   English: {nllb_tokens} tokens")
            print(f"   Savings: {nllb_savings} tokens ({nllb_percent:.1f}%)")
            print(f"   Preview: {nllb_result.text[:100]}...")
            
            # Comparison
            improvement = nllb_tokens - google_tokens
            improvement_percent = (improvement / google_tokens) * 100
            
            print(f"\n📊 NLLB vs Google:")
            print(f"   Token difference: {improvement} tokens")
            print(f"   NLLB is {abs(improvement_percent):.1f}% {'more concise' if improvement < 0 else 'more verbose'}")
            
            total_nllb_savings += nllb_savings
            
            results.append({
                "name": test['name'],
                "ja_tokens": ja_tokens,
                "google_tokens": google_tokens,
                "google_savings": google_savings,
                "google_percent": google_percent,
                "nllb_tokens": nllb_tokens,
                "nllb_savings": nllb_savings,
                "nllb_percent": nllb_percent
            })
        
        total_google_savings += google_savings
        total_ja_tokens += ja_tokens
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 OVERALL RESULTS")
    print(f"{'='*80}")
    
    print(f"\nTotal Japanese tokens: {total_ja_tokens}")
    
    avg_google_percent = (total_google_savings / total_ja_tokens) * 100
    print(f"\n🔵 Google Translate:")
    print(f"   Total savings: {total_google_savings} tokens")
    print(f"   Average reduction: {avg_google_percent:.1f}%")
    
    if nllb_available:
        avg_nllb_percent = (total_nllb_savings / total_ja_tokens) * 100
        print(f"\n🟢 NLLB:")
        print(f"   Total savings: {total_nllb_savings} tokens")
        print(f"   Average reduction: {avg_nllb_percent:.1f}%")
        
        additional_savings = total_nllb_savings - total_google_savings
        print(f"\n✨ NLLB Improvement:")
        print(f"   Additional savings: {additional_savings} tokens")
        print(f"   {avg_nllb_percent - avg_google_percent:.1f} percentage points better")
    
    # Conservative recommendation
    print(f"\n{'='*80}")
    print("💡 CONSERVATIVE PERFORMANCE ESTIMATES")
    print(f"{'='*80}")
    
    if nllb_available:
        # Use the lowest result as conservative estimate
        min_nllb_percent = min(r['nllb_percent'] for r in results)
        max_nllb_percent = max(r['nllb_percent'] for r in results)
        
        print(f"\nBased on testing with realistic long prompts (100+ tokens):")
        print(f"  Minimum savings: {min_nllb_percent:.0f}%")
        print(f"  Maximum savings: {max_nllb_percent:.0f}%")
        print(f"  Average savings: {avg_nllb_percent:.0f}%")
        print(f"\n✅ Conservative claim: {min_nllb_percent:.0f}-{avg_nllb_percent:.0f}% token reduction")
        print(f"   (Use in documentation)")
        
        return {
            "min_savings": min_nllb_percent,
            "max_savings": max_nllb_percent,
            "avg_savings": avg_nllb_percent,
            "conservative_range": f"{min_nllb_percent:.0f}-{avg_nllb_percent:.0f}%"
        }

if __name__ == "__main__":
    print("\n🧪 Running comprehensive token optimization test...\n")
    print("⚠️  This will take several minutes (NLLB translation is slow on CPU)\n")
    
    try:
        results = test_comprehensive_optimization()
        
        if results:
            print(f"\n{'='*80}")
            print("✅ Test Complete!")
            print(f"{'='*80}")
            print(f"\n📝 Recommended documentation claim:")
            print(f"   'Achieves {results['conservative_range']} token reduction'")
            print(f"   'on realistic prompts (100+ tokens)'")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
