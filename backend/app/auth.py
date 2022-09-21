from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import SessionLocal

from app import schemas, crud, security

import datetime

# Dependency is remade since an import would create circular dependencies


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JSON Web Token (JWT) Functions


def generic_token_creation(data: dict, expires_delta: datetime.timedelta, token_type: str):
    """
    Creates a JWT
    """
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    if token_type == "access":
        encoded_jwt = jwt.encode(
            to_encode, security.SECRET_KEY, algorithm=security.ALGORITHM)
    else:
        encoded_jwt = jwt.encode(
            to_encode, security.JWT_REFRESH_SECRET_KEY, algorithm=security.ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str):
    """
    Checks if a user exists with credentials provided
    """
    user = crud.get_user_by_username(db, username=username)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(security.reuseable_oauth)):
    """
    Gets the current logged in user entity based on the JWT (token) passed in
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user
