from fastapi import HTTPException, status

from app.services.model_service import ModelService
from app.core.rate_limiter import RateLimiter

model_service = ModelService()
rate_limiter = RateLimiter()

def get_model_service() -> ModelService:
    if model_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model service not initialized"
        )
    return model_service

def get_rate_limiter() -> RateLimiter:
    if rate_limiter is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Rate limiter not initialized"
        )
    return rate_limiter
