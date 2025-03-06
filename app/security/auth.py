from typing import Optional
from datetime import datetime,timedelta
from jose import JWTError,jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

from ..config.settings import settings

oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data:dict, expires_delta:Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encode_jwt

def verify_token(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=settings.JWT_ALGORITHM
        )
        return payload
    except JWTError :
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate" : "Bearer"}
        )



