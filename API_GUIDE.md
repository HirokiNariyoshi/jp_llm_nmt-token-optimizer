# TokenOptimizer API Guide

## Quick Start

### Using Docker (Recommended)

```bash
docker-compose up
```

### Using Python directly

```bash
# Make sure Ollama is running
ollama serve

# Start the API
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Root Endpoint

```http
GET /
```

Returns API information and available endpoints.

**Response:**

```json
{
  "name": "TokenOptimizer API",
  "version": "0.1.0",
  "description": "Optimize Japanese LLM queries through neural machine translation",
  "endpoints": {
    "POST /optimize": "Optimize a Japanese query",
    "GET /health": "Health check",
    "GET /docs": "Interactive API documentation"
  }
}
```

### Health Check

```http
GET /health
```

Check API health and dependency status.

**Response:**

```json
{
  "status": "healthy",
  "optimizer_ready": true,
  "ollama_connected": true
}
```

### Optimize Query

```http
POST /optimize
```

Optimize a Japanese query for LLM processing.

**Request Body:**

```json
{
  "prompt": "Pythonで機械学習モデルを作る方法を教えてください。",
  "max_tokens": 500,
  "system_prompt": null,
  "force_optimization": null
}
```

**Parameters:**

- `prompt` (required): Japanese text to optimize
- `max_tokens` (optional): Maximum tokens for LLM response (default: 1000, max: 4000)
- `system_prompt` (optional): Japanese system prompt
- `force_optimization` (optional): Force enable/disable optimization (null = auto)

**Response:**

```json
{
  "content": "機械学習モデルを作成する方法は...",
  "metrics": {
    "original_tokens": 86,
    "optimized_tokens": 39,
    "tokens_saved": 47,
    "token_reduction_percent": 54.7,
    "original_cost": 0.0,
    "optimized_cost": 0.0,
    "cost_saved": 0.0,
    "cost_reduction_percent": 0.0,
    "translation_time": 2.5,
    "time_overhead_percent": 25.0,
    "llm_time": 7.5,
    "total_time": 10.0,
    "used_optimization": true
  }
}
```

## Usage Examples

### cURL

**Basic optimization:**

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Pythonで機械学習を始める方法を教えてください。",
    "max_tokens": 300
  }'
```

**Force optimization:**

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "短いプロンプト",
    "force_optimization": true
  }'
```

**Health check:**

```bash
curl http://localhost:8000/health
```

### Python

Using requests library:

```python
import requests

API_URL = "http://localhost:8000"

response = requests.post(
    f"{API_URL}/optimize",
    json={
        "prompt": "Pythonで機械学習モデルを作る方法を教えてください。",
        "max_tokens": 500
    }
)

result = response.json()
print("Response:", result["content"])
print(f"Token reduction: {result['metrics']['token_reduction_percent']:.1f}%")
print(f"Total time: {result['metrics']['total_time']:.2f}s")
```

Async client:

```python
import httpx
import asyncio

async def optimize_query(prompt: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/optimize",
            json={"prompt": prompt, "max_tokens": 500}
        )
        return response.json()

result = asyncio.run(optimize_query("Pythonで..."))
```

### JavaScript/Node.js

Using fetch:

```javascript
const response = await fetch("http://localhost:8000/optimize", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    prompt: "Pythonで機械学習モデルを作る方法を教えてください。",
    max_tokens: 500,
  }),
});

const result = await response.json();
console.log("Response:", result.content);
console.log(`Token reduction: ${result.metrics.token_reduction_percent}%`);
```

Using axios:

```javascript
const axios = require("axios");

const result = await axios.post("http://localhost:8000/optimize", {
  prompt: "Pythonで機械学習モデルを作る方法を教えてください。",
  max_tokens: 500,
});

console.log("Response:", result.data.content);
console.log(`Tokens saved: ${result.data.metrics.tokens_saved}`);
```

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Docker Deployment

### Build and Run

Development:

```bash
docker-compose up
```

Production:

```bash
docker-compose -f docker-compose.yml up -d
```

### Configuration

Environment variables (set in `docker-compose.yml`):

- `LLM_MODEL`: Ollama model to use (default: "llama3.2:3b")
- `OPTIMIZATION_THRESHOLD`: Minimum tokens for optimization (default: 50)
- `PORT`: API port (default: 8000)

### Scaling

```bash
docker-compose up --scale api=3
```

## Error Handling

### Common Errors

**503 Service Unavailable**

```json
{
  "detail": "Optimizer not initialized"
}
```

Solution: Wait for NLLB model to load (first request only)

**500 Internal Server Error**

```json
{
  "detail": "Optimization failed: Could not connect to Ollama..."
}
```

Solution: Ensure Ollama is running (`ollama serve`)

**422 Validation Error**

```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

Solution: Check request parameters match the schema

## Performance Tips

1. **First Request Latency**: NLLB model loads on first optimization (~10-20s)
2. **Subsequent Requests**: Model stays in memory, much faster
3. **Caching**: Consider implementing Redis cache for repeated prompts
4. **Batch Processing**: For multiple prompts, send requests in parallel
5. **Timeout**: Set appropriate timeouts (recommend 30s minimum)

## Monitoring

### Logs

Docker logs:

```bash
docker-compose logs -f api
```

Application logs:

```bash
tail -f logs/api.log  # if configured
```

### Metrics

Monitor these metrics from the `/optimize` response:

- `token_reduction_percent`: Optimization effectiveness
- `translation_time`: NLLB processing time
- `llm_time`: LLM generation time
- `total_time`: End-to-end latency

## Security Considerations

For production deployment:

1. **Authentication**: Add API key or OAuth2
2. **Rate Limiting**: Implement request throttling
3. **HTTPS**: Use reverse proxy (nginx) with SSL
4. **CORS**: Restrict allowed origins
5. **Input Validation**: Already implemented via Pydantic
6. **Resource Limits**: Set max_tokens limits (currently 4000)

Example nginx config:

```nginx
server {
    listen 443 ssl;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Support

For issues or questions:

- GitHub Issues: https://github.com/HirokiNariyoshi/llm_nmt-token-optimizer/issues
- Documentation: See README.md
