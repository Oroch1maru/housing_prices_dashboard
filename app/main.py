from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routers import auth,prediction
from app.core.config import settings
from app.dependencies import model_service, rate_limiter


logger = logging.getLogger(__name__)




@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    model_service.load_model()
    logger.info("Application started successfully")

    yield

    logger.info("Shutting down application...")
    logger.info("Application shutdown complete")


app = FastAPI(
    title="House Price Prediction API",
    description="REST API for predicting house prices using ML model",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(prediction.router, prefix="/api", tags=["predictions"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_service.is_loaded() if model_service else False
    }


