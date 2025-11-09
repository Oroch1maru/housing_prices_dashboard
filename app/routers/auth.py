from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import logging

from app.schemas import LoginRequest, Token
from app.services.database_service import get_db, User
from app.core.security import verify_password, create_token
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/token", response_model=Token)
async def login(login_data: LoginRequest,db: Session = Depends(get_db))->dict:
    """
    Authenticate user and return JWT token.
    """


    user = db.query(User).filter(User.username == login_data.username).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt for username: {login_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    print(f"Time: {datetime.now(timezone.utc)}")
    access_token = create_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    logger.info(f"Successful login for user: {user.username}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": datetime.now(timezone.utc)+access_token_expires
    }