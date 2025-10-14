"""
Test: Can we save tokens by translating Japanese→English for English-optimized models?
"""

import tiktoken
from deep_translator import GoogleTranslator

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens using tiktoken (GPT-4/Claude tokenizer)"""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

# Test prompts in Japanese (common use case in Japan)
japanese_prompts = [
    # Short technical query
    """量子コンピューティングについて詳しく説明してください。
    歴史的な発展、主要な実験、数学的基礎、
    量子計算と暗号化における実用的な応用を含めてください。""",
    
    # Medium conversational query
    """来月、親友のサプライズバースデーパーティーを企画しています。
    彼女は30歳になり、アウトドア活動、ヴィンテージの美学、
    植物やガーデニングに関連することが大好きです。
    仕事のストレスや個人的な課題で大変な一年を過ごしてきたので、
    本当に特別なものにしたいと思っています。""",
    
    # Long business query
    """当社は新しいEコマースプラットフォームの立ち上げを計画しており、
    技術スタックの選択について助言が必要です。私たちのチームは
    React、Node.js、Pythonに精通していますが、規模拡大、セキュリティ、
    パフォーマンス、保守性のバランスを取りたいと考えています。
    クラウドインフラストラクチャ、データベース設計、マイクロサービス
    アーキテクチャ、API設計のベストプラクティスについて
    推奨事項を提供していただけますか？"""
]

print("=" * 80)
print("REVERSE OPTIMIZATION TEST: Japanese → English Translation")
print("=" * 80)
print()

translator = GoogleTranslator(source='ja', target='en')

total_ja_tokens = 0
total_en_tokens = 0

for i, ja_prompt in enumerate(japanese_prompts, 1):
    print(f"\n📝 Test {i}:")
    print(f"Japanese prompt: {ja_prompt[:100]}...")
    
    # Count Japanese tokens
    ja_tokens = count_tokens(ja_prompt)
    
    # Translate to English
    en_prompt = translator.translate(ja_prompt)
    
    # Count English tokens
    en_tokens = count_tokens(en_prompt)
    
    # Calculate savings
    tokens_saved = ja_tokens - en_tokens
    percent_saved = (tokens_saved / ja_tokens * 100) if ja_tokens > 0 else 0
    
    print(f"\n  Japanese tokens: {ja_tokens}")
    print(f"  English tokens:  {en_tokens}")
    print(f"  Tokens saved:    {tokens_saved} ({percent_saved:.1f}%)")
    
    if tokens_saved > 0:
        print(f"  ✅ English is MORE efficient!")
    else:
        print(f"  ❌ Japanese is more efficient")
    
    total_ja_tokens += ja_tokens
    total_en_tokens += en_tokens

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
total_saved = total_ja_tokens - total_en_tokens
total_percent = (total_saved / total_ja_tokens * 100) if total_ja_tokens > 0 else 0

print(f"\nTotal Japanese tokens: {total_ja_tokens}")
print(f"Total English tokens:  {total_en_tokens}")
print(f"Total tokens saved:    {total_saved} ({total_percent:.1f}%)")
print()

if total_saved > 0:
    print("✅ VIABLE! Translating Japanese→English saves tokens!")
    print(f"   For Japanese users, this could reduce costs by {total_percent:.1f}%")
    print()
    print("💡 New Project Direction:")
    print("   'Japanese Query Optimizer for English-Optimized LLMs'")
    print("   JA Input → EN (translate) → LLM → EN → JA (translate)")
else:
    print("❌ Not viable - Japanese is already more efficient")

print("\n" + "=" * 80)
