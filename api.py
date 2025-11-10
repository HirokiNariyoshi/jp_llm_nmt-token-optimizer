"""
FastAPI server for TokenOptimizer.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging

from token_optimizer import TokenOptimizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TokenOptimizer API",
    description="Optimize Japanese LLM queries by reducing token usage through neural machine translation",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

optimizer: Optional[TokenOptimizer] = None


def get_optimizer() -> TokenOptimizer:
    """Get or create TokenOptimizer instance."""
    global optimizer
    if optimizer is None:
        logger.info("Initializing TokenOptimizer...")
        optimizer = TokenOptimizer(
            llm_model="llama3.2:3b",
            optimization_threshold=50
        )
        logger.info("TokenOptimizer initialized successfully")
    return optimizer


class OptimizeRequest(BaseModel):
    """Request model for optimization endpoint."""
    prompt: str = Field(..., description="Japanese prompt text to optimize")
    max_tokens: int = Field(1000, description="Maximum tokens for LLM response", ge=1, le=4000)
    system_prompt: Optional[str] = Field(None, description="Optional Japanese system prompt")
    force_optimization: Optional[bool] = Field(None, description="Force enable/disable optimization (None=auto)")

    class Config:
        schema_extra = {
            "example": {
                "prompt": "Pythonで機械学習モデルを作る方法を教えてください。",
                "max_tokens": 500,
                "force_optimization": True
            }
        }


class MetricsResponse(BaseModel):
    """Metrics from optimization process."""
    original_tokens: int
    optimized_tokens: int
    tokens_saved: int
    token_reduction_percent: float
    original_cost: float
    optimized_cost: float
    cost_saved: float
    cost_reduction_percent: float
    translation_time: float
    time_overhead_percent: float
    llm_time: float
    total_time: float
    used_optimization: bool


class OptimizeResponse(BaseModel):
    """Response model for optimization endpoint."""
    content: str = Field(..., description="LLM generated content in Japanese")
    metrics: MetricsResponse = Field(..., description="Performance and optimization metrics")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    optimizer_ready: bool
    ollama_connected: bool


# API Endpoints
@app.get("/", response_model=dict)
async def root():
    """API root endpoint with basic information."""
    return {
        "name": "TokenOptimizer API",
        "version": "0.1.0",
        "description": "Optimize Japanese LLM queries through neural machine translation",
        "endpoints": {
            "POST /optimize": "Optimize a Japanese query",
            "GET /health": "Health check",
            "GET /docs": "Interactive API documentation"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    optimizer_ready = optimizer is not None
    
    ollama_connected = False
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        ollama_connected = response.status_code == 200
    except Exception:
        pass
    
    status = "healthy" if ollama_connected else "degraded"
    
    return {
        "status": status,
        "optimizer_ready": optimizer_ready,
        "ollama_connected": ollama_connected
    }


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_query(request: OptimizeRequest):
    """Optimize a Japanese query for LLM processing."""
    try:
        opt = get_optimizer()
        
        logger.info(f"Processing optimization request: {len(request.prompt)} chars")
        
        response = opt.optimize_request(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            system_prompt=request.system_prompt,
            force_optimization=request.force_optimization
        )
        
        logger.info(
            f"Optimization complete: {response.metrics.token_reduction_percent:.1f}% "
            f"token reduction, {response.metrics.total_time:.2f}s total time"
        )
        
        return OptimizeResponse(
            content=response.content,
            metrics=MetricsResponse(**response.to_dict()["metrics"])
        )
        
    except Exception as e:
        logger.error(f"Optimization failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}"
        )


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("TokenOptimizer API starting up...")
    logger.info("Optimizer will be initialized on first request")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("TokenOptimizer API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
