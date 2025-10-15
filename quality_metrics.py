"""
Automated Quality Metrics for Translation Optimization

Uses semantic similarity to quantify quality degradation from translation.
Requires: sentence-transformers for embedding-based comparison
"""

from typing import Dict, Any, Optional
import json


class QualityMetrics:
    """
    Automated quality assessment for translated LLM responses.
    
    Methods:
    1. Semantic Similarity - Compare embeddings of responses
    2. Length Ratio - Check if response length is preserved
    3. BLEU Score - Machine translation metric (optional)
    4. Back-Translation Check - Translate optimized response back and compare
    """
    
    def __init__(self):
        self._embedding_model = None
        
    def get_embedding_model(self):
        """Lazy load sentence transformer model."""
        if self._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                # Multilingual model that works with Japanese and English
                self._embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
                print("✅ Loaded multilingual embedding model")
            except ImportError:
                print("⚠️  sentence-transformers not installed.")
                print("Install with: pip install sentence-transformers")
                return None
        return self._embedding_model
    
    def semantic_similarity(self, text1: str, text2: str) -> Optional[float]:
        """
        Calculate semantic similarity between two texts using embeddings.
        
        Returns:
            Similarity score 0.0-1.0 (higher = more similar)
            Returns None if model not available
        """
        model = self.get_embedding_model()
        if model is None:
            return None
        
        # Generate embeddings
        embeddings = model.encode([text1, text2])
        
        # Calculate cosine similarity
        from numpy import dot
        from numpy.linalg import norm
        
        similarity = dot(embeddings[0], embeddings[1]) / (norm(embeddings[0]) * norm(embeddings[1]))
        
        return float(similarity)
    
    def length_ratio(self, text1: str, text2: str) -> float:
        """
        Compare lengths of two texts.
        
        Returns:
            Ratio of lengths (1.0 = same length, <1.0 = text2 shorter)
        """
        len1 = len(text1)
        len2 = len(text2)
        
        if len1 == 0:
            return 0.0
        
        return min(len1, len2) / max(len1, len2)
    
    def assess_quality(
        self,
        direct_response: str,
        optimized_response: str,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Full quality assessment comparing direct vs optimized responses.
        
        Args:
            direct_response: Response from direct Japanese path (baseline)
            optimized_response: Response from optimized translation path
            verbose: Print detailed results
            
        Returns:
            Dictionary with quality metrics
        """
        results = {
            "semantic_similarity": None,
            "length_ratio": self.length_ratio(direct_response, optimized_response),
            "assessment": "Unknown"
        }
        
        # Semantic similarity (if available)
        similarity = self.semantic_similarity(direct_response, optimized_response)
        if similarity is not None:
            results["semantic_similarity"] = similarity
            
            # Quality assessment based on similarity
            if similarity >= 0.90:
                results["assessment"] = "Excellent - Minimal quality loss"
            elif similarity >= 0.80:
                results["assessment"] = "Good - Minor differences"
            elif similarity >= 0.70:
                results["assessment"] = "Acceptable - Some quality loss"
            else:
                results["assessment"] = "Poor - Significant quality degradation"
        
        if verbose:
            print("\n" + "=" * 70)
            print("📊 AUTOMATED QUALITY METRICS")
            print("=" * 70)
            
            if results["semantic_similarity"] is not None:
                print(f"\n🔍 Semantic Similarity: {results['semantic_similarity']:.3f}")
                print(f"   (1.0 = identical meaning, 0.0 = completely different)")
            else:
                print("\n⚠️  Semantic similarity unavailable (install sentence-transformers)")
            
            print(f"\n📏 Length Ratio: {results['length_ratio']:.3f}")
            print(f"   (1.0 = same length, lower = more difference)")
            
            print(f"\n✅ Assessment: {results['assessment']}")
            
            # Recommendations
            print("\n💡 Recommendations:")
            if results["semantic_similarity"] and results["semantic_similarity"] >= 0.85:
                print("   ✅ Quality is good - translation optimization is safe to use")
            elif results["semantic_similarity"] and results["semantic_similarity"] >= 0.75:
                print("   ⚠️  Minor quality differences - review for critical use cases")
            else:
                print("   ❌ Quality concerns - manual review recommended")
        
        return results


# Example usage
if __name__ == "__main__":
    print("📊 Automated Quality Assessment Tool")
    print("=" * 70)
    print("\nThis tool uses semantic embeddings to measure quality differences.")
    print("First, install required package:")
    print("  pip install sentence-transformers\n")
    
    # Example comparison
    direct = "量子コンピューティングは、量子力学の原理を利用して計算を行う新しいタイプのコンピューターです。"
    optimized = "量子コンピューティングとは、量子力学の法則を使って計算する新型コンピューターのことです。"
    
    metrics = QualityMetrics()
    results = metrics.assess_quality(direct, optimized, verbose=True)
    
    print("\n" + "=" * 70)
    print("📝 INTERPRETING RESULTS")
    print("=" * 70)
    print("""
Semantic Similarity Score Interpretation:
  0.95-1.00: Nearly identical - translation has minimal impact
  0.90-0.95: Excellent - minor paraphrasing, same meaning
  0.85-0.90: Good - some differences but core meaning preserved
  0.80-0.85: Acceptable - noticeable differences, meaning mostly intact
  0.70-0.80: Concerning - significant meaning drift
  < 0.70:    Poor - substantial quality loss

For production use, aim for >0.85 similarity score.
Below 0.80 requires manual review.
    """)
