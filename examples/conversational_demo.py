"""
Example with pure conversational text to demonstrate maximum cost savings.
This uses everyday language without numbers or technical terms.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from token_optimizer import TokenOptimizer

load_dotenv()


def main():
    # Initialize the optimizer with a LOW threshold to force optimization
    optimizer = TokenOptimizer(
        llm_provider="ollama",
        llm_model="qwen2.5:1.5b",  # Lightweight model for low RAM
        translation_provider="google",
        cache_enabled=False,
        optimization_threshold=1  # Force optimization
    )
    
    # Pure conversational prompt without numbers or technical terms
    conversational_prompt = """
    I've been feeling really overwhelmed lately with everything going on in my life. 
    Work has been incredibly stressful because we're going through major changes in 
    our department, and everyone seems to be on edge all the time. My manager keeps 
    changing priorities, so I never know what I should be focusing on, and it feels 
    like nothing I do is ever quite right or enough.
    
    On top of that, my personal relationships have been struggling too. My best friend 
    moved to another city last month, and even though we video call regularly, it's 
    just not the same as being able to meet up for coffee or go for walks together 
    like we used to do almost every weekend. I miss having that person I could just 
    talk to about anything without having to explain the whole background story every time.
    
    My family has been asking when I'm going to visit them, but honestly I'm so tired 
    all the time that the thought of traveling and making small talk with relatives 
    just exhausts me even more. I know they mean well and they love me, but sometimes 
    I wish they would understand that I need some space to figure things out without 
    feeling guilty about not being there for every family gathering or celebration.
    
    I've also been neglecting my hobbies and the things that usually make me happy. 
    I used to love reading books and going to museums, but lately I just come home 
    and scroll through my phone or watch random videos until it's time to sleep. 
    Even my weekends feel empty and unproductive, which makes me feel even worse 
    about myself and my life choices.
    
    I know I probably need to make some changes, but I don't even know where to start. 
    Everything feels interconnected and overwhelming, like if I pull on one thread, 
    the whole thing will unravel. Can you help me think through this and maybe give 
    me some perspective or suggestions on how to approach these different challenges 
    in a way that feels manageable rather than completely overwhelming?
    """
    
    print("=" * 70)
    print("PURE CONVERSATIONAL TEXT DEMO")
    print("=" * 70)
    print()
    print("📝 Prompt length:", len(conversational_prompt.split()), "words")
    print("   (Pure everyday language, no numbers/technical terms)")
    print()
    
    # Process with optimization
    print("🚀 Processing with optimization...")
    print()
    
    response = optimizer.optimize_request(
        prompt=conversational_prompt,
        max_tokens=600
    )
    
    # Display results
    print()
    print("=" * 70)
    print("RESPONSE (first 400 chars)")
    print("=" * 70)
    print(response.content[:400] + "...")
    print()
    
    print("=" * 70)
    print("OPTIMIZATION METRICS")
    print("=" * 70)
    print()
    
    metrics = response.metrics
    
    # Token analysis
    print("📊 TOKEN USAGE:")
    print(f"  Original (English):  {metrics.original_tokens} tokens")
    print(f"  Optimized (Japanese): {metrics.optimized_tokens} tokens")
    print(f"  Tokens saved:        {metrics.tokens_saved} tokens")
    print(f"  Reduction:           {metrics.token_reduction_percent:.1f}%")
    print()
    
    # Cost analysis
    print("💰 COST SAVINGS:")
    print(f"  Without optimization: ${metrics.original_cost:.6f}")
    print(f"  With optimization:    ${metrics.optimized_cost:.6f}")
    
    if metrics.cost_saved > 0:
        print(f"  💵 SAVED:             ${metrics.cost_saved:.6f} ({metrics.cost_reduction_percent:.1f}%)")
    else:
        print(f"  Additional cost:      ${abs(metrics.cost_saved):.6f} ({abs(metrics.cost_reduction_percent):.1f}% more)")
    print()
    
    # Time analysis
    print("⏱️  PERFORMANCE:")
    print(f"  Translation time:  {metrics.translation_time:.2f}s")
    print(f"  LLM time:          {metrics.llm_time:.2f}s")
    print(f"  Total time:        {metrics.total_time:.2f}s")
    print()
    
    # Optimization status
    if metrics.used_optimization:
        if metrics.tokens_saved > 0:
            print("✅ SUCCESS! Japanese compression saved tokens and money!")
            print(f"   For a large-scale deployment, these savings multiply significantly.")
        else:
            print("⚠️  Japanese used more tokens for this prompt type.")
            print("   This tokenizer may be optimized for English.")
    else:
        print("ℹ️  Direct English was more efficient (optimizer made smart choice)")
    
    print()
    print("=" * 70)
    print()
    print("💡 NOTE: Token savings depend on:")
    print("   - Language pair (Japanese vs English)")
    print("   - Tokenizer used by the LLM model")
    print("   - Content type (conversational vs technical)")
    print("   - Prompt length (longer = more potential savings)")
    print()


if __name__ == "__main__":
    print("Using Ollama with Gemma2 (multilingual with Japanese support!)")
    print()
    main()
