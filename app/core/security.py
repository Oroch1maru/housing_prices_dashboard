from typing import Optional, Any
import datetime
from datetime import datetime, timezone,timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
import jwt
import logging
import sys
from passlib.context import CryptContext

from app.core.config import settings



logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
security = HTTPBearer()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict,expires_delta: timedelta) -> str:
    logging.info('Create token...')
    to_encode = data.copy()
    exp_time = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": exp_time})


    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    logging.info(f'The token has been successfully generated and will be valid until {exp_time}')

    return encoded_jwt

def decode_token(token: str) -> dict:
    logging.info('Decode token...')

    decoded_data=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    logging.info(f'The token has been successfully decoded')

    return decoded_data


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            logging.warning('Username not found in payload')

        return payload

    except jwt.ExpiredSignatureError:
        logging.warning('Token is expired!')