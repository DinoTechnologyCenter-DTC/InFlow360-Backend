import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Union
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from sqlmodel import Session, select

from src.models.tables import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


bearer_scheme = HTTPBearer(
    auto_error=False,
    description="Bearer token authentication for Nairi API",
)


# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def create_access_token(
    *,
    user_id: UUID,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token."""
    to_encode = {
        "sub": str(user_id),
        "iss": "nairi",
    }
    expire = (
        datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if not expires_delta
        else datetime.now(tz=timezone.utc) + expires_delta
    )

    to_encode.update(
        {
            "exp": expire,
        },
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    cred: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """Get the current user from the token."""
    # Check if credentials were provided
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the token
    payload = verify_access_token(cred.credentials)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch the user from the database
    return True
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def decode_access_token(token: str) -> Optional[dict]:
    """Decode JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> dict:
    """Verify and decode the JWT access token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
