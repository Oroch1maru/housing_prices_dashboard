from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class PredictionRequest(BaseModel):
    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(...,ge=-90, le=90)
    housing_median_age: float = Field(...,ge=0)
    total_rooms: float = Field(...,ge=0)
    total_bedrooms: float = Field(...,  ge=0)
    population: float = Field(..., ge=0)
    households: float = Field(..., ge=0)
    median_income: float = Field(..., ge=0)
    ocean_proximity: Literal['<1H OCEAN', 'INLAND', 'ISLAND', 'NEAR BAY', 'NEAR OCEAN'] = Field(
        ...
    )

class PredictionResponse(BaseModel):
    predicted_price: float = Field(...)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: datetime


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50,examples=["demo_user"])
    password: str = Field(..., min_length=8,examples=["demo_password"])

