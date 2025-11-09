# API Client Examples

## Python Client

```python
import requests

API_URL = "http://localhost:8000"

def optimize_query(prompt: str, max_tokens: int = 1000):
    """Optimize a Japanese query using the TokenOptimizer API."""
    response = requests.post(
        f"{API_URL}/optimize",
        json={
            "prompt": prompt,
            "max_tokens": max_tokens,
            "force_optimization": True
        }
    )
    response.raise_for_status()
    return response.json()

# Example usage
if __name__ == "__main__":
    result = optimize_query(
        prompt="Pythonで機械学習モデルを作る方法を教えてください。",
        max_tokens=500
    )

    print("Response:", result["content"])
    print(f"Token reduction: {result['metrics']['token_reduction_percent']:.1f}%")
    print(f"Tokens saved: {result['metrics']['tokens_saved']}")
```

## JavaScript/Node.js Client

```javascript
const axios = require("axios");

const API_URL = "http://localhost:8000";

async function optimizeQuery(prompt, maxTokens = 1000) {
  try {
    const response = await axios.post(`${API_URL}/optimize`, {
      prompt: prompt,
      max_tokens: maxTokens,
      force_optimization: true,
    });

    return response.data;
  } catch (error) {
    console.error(
      "Optimization failed:",
      error.response?.data || error.message
    );
    throw error;
  }
}

// Example usage
(async () => {
  const result = await optimizeQuery(
    "Pythonで機械学習モデルを作る方法を教えてください。",
    500
  );

  console.log("Response:", result.content);
  console.log(
    `Token reduction: ${result.metrics.token_reduction_percent.toFixed(1)}%`
  );
  console.log(`Tokens saved: ${result.metrics.tokens_saved}`);
})();
```

## cURL Examples

### Optimize a query

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Pythonで機械学習モデルを作る方法を教えてください。",
    "max_tokens": 500,
    "force_optimization": true
  }'
```

### Health check

```bash
curl http://localhost:8000/health
```

### Get API info

```bash
curl http://localhost:8000/
```

## Response Format

```json
{
  "content": "機械学習モデルを構築するには...",
  "metrics": {
    "original_tokens": 86,
    "optimized_tokens": 39,
    "tokens_saved": 47,
    "token_reduction_percent": 54.7,
    "original_cost": 0.0,
    "optimized_cost": 0.0,
    "cost_saved": 0.0,
    "cost_reduction_percent": 0.0,
    "translation_time": 3.2,
    "time_overhead_percent": 25.2,
    "llm_time": 9.5,
    "total_time": 12.7,
    "used_optimization": true
  }
}
```

## Error Handling

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/optimize",
        json={"prompt": "日本語のクエリ"},
        timeout=60
    )
    response.raise_for_status()
    result = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
    print(f"Detail: {e.response.json()}")
except Exception as e:
    print(f"Error: {str(e)}")
```
