"""
Example with a long conversational prompt to demonstrate cost savings.
This shows how the optimizer excels with longer, descriptive prompts.
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
        llm_model="qwen2.5:1.5b",  # Lightweight model
        translation_provider="google",
        cache_enabled=False,
        optimization_threshold=10  # Very low threshold to force optimization
    )
    
    # Long, conversational prompt
    long_prompt = """
    I'm planning a surprise birthday party for my best friend next month and I need some 
    creative ideas. She's turning 30 and loves outdoor activities, vintage aesthetics, 
    and anything related to plants and gardening. I want to make this really special 
    because she's been through a tough year with work stress and personal challenges.
    
    The party will be at my backyard which has a pretty large garden space with lots of 
    flowers and trees. I'm thinking maybe we could do something during sunset, like around 
    6 PM when the lighting is really beautiful. I have about 25 people coming, mostly close 
    friends from college and some coworkers she really likes.
    
    My budget is around $800 to $1000, and I want to focus on making it feel intimate and 
    personal rather than fancy or expensive. She's not into loud music or anything too 
    flashy, so I'm thinking more of a cozy garden gathering vibe with good food, warm 
    conversations, and maybe some thoughtful touches that show how much we all care about her.
    
    Could you help me brainstorm some ideas for decorations, activities, food options, and 
    maybe a special moment or surprise element that would make her feel really loved? Also, 
    any tips on how to coordinate everything without her finding out would be super helpful 
    because she's pretty observant and usually figures things out!
    """
    
    print("=" * 70)
    print("LONG CONVERSATIONAL PROMPT DEMO")
    print("=" * 70)
    print()
    print("📝 Prompt length:", len(long_prompt.split()), "words")
    print()
    
    # Process with optimization
    print("🚀 Processing with optimization...")
    print()
    
    response = optimizer.optimize_request(
        prompt=long_prompt,
        max_tokens=800
    )
    
    # Display results
    print()
    print("=" * 70)
    print("RESPONSE")
    print("=" * 70)
    print(response.content[:500] + "..." if len(response.content) > 500 else response.content)
    print()
    
    print("=" * 70)
    print("OPTIMIZATION METRICS")
    print("=" * 70)
    print()
    
    metrics = response.metrics
    
    # Token analysis
    print("📊 TOKEN USAGE:")
    print(f"  Original tokens:    {metrics.original_tokens}")
    print(f"  Optimized tokens:   {metrics.optimized_tokens}")
    print(f"  Tokens saved:       {metrics.tokens_saved}")
    print(f"  Reduction:          {metrics.token_reduction_percent:.1f}%")
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
    print(f"  Translation time:  {metrics.translation_time:.2f}s")
    print(f"  LLM time:          {metrics.llm_time:.2f}s")
    print(f"  Total time:        {metrics.total_time:.2f}s")
    print()
    
    # Optimization status
    if metrics.used_optimization:
        if metrics.tokens_saved > 0:
            print("✅ Optimization SUCCESSFUL! Japanese was more efficient.")
        else:
            print("⚠️  Optimization used but no savings (Japanese was similar to English)")
    else:
        print("ℹ️  Direct English used (would have been more efficient)")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    print("Using Ollama with Gemma2 (multilingual with Japanese support!)")
    print()
    main()
