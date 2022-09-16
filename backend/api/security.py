from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from api import schemas, crud

import datetime

SECRET_KEY = "sW04AA2nYC8jXYHtXP4PBJ3YIzi+oyfbel137TkkpeGAGjUxhk6cFM32PdWKYZPL"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
JWT_REFRESH_SECRET_KEY = "MIIEpAIBAAKCAQEAzJPPU2jJBnK4MjynlfQbWQXa2p4OVPohx+7O84uSfXWLVUhH"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str):
    return pwd_context.hash(password)
