from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.schemas import  PredictionRequest,PredictionResponse
from app.services.database_service import get_db, User
from app.core.security import verify_token
from app.core.config import settings
from app.services.model_service import ModelService
from app.core.rate_limiter import RateLimiter
from app.dependencies import get_model_service, get_rate_limiter


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest,token_data: dict = Depends(verify_token),model_service: ModelService = Depends(get_model_service),rate_limiter: RateLimiter = Depends(get_rate_limiter))->PredictionResponse:
    """
    Price prediction based on house data.
    """

    try:
        username = token_data.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str("Token is expired!")
        )
    rate_limiter.check_rate_limit(username)

    try:
        result_prediction=model_service.predict(request.model_dump())
        return PredictionResponse(predicted_price=result_prediction)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=str(e)
        )