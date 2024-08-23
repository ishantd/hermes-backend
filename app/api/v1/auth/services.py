from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import constants
from app.api.v1.auth.models import User
from app.api.v1.auth.schemas import (
    UserLoginSchema,
    UserResponseSchema,
    UserSignupSchema,
)
from app.database import db
from app.settings import settings

ALGORITHM = "HS256"


def signup(
    payload: UserSignupSchema,
    session: Session,
) -> User:
    """
    Create a new user.
    """
    log_prefix = "[User Signup]"
    logger.info(
        f"{log_prefix} Attempting to sign up user: {payload.email}",
    )

    if len(payload.password) < constants.MINIMUM_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password must be at least {constants.MINIMUM_PASSWORD_LENGTH} characters long.",
        )

    user = User(
        email=payload.email,
        password=payload.password,
        name=payload.name,
    )
    session.add(user)

    try:
        session.commit()
    except IntegrityError as e:
        logger.error(f"{log_prefix} {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        )
    except Exception as e:
        logger.error(f"{log_prefix} {e}")
        session.rollback()
        raise e

    return user


def login(
    payload: UserLoginSchema,
    session: Session,
) -> User:
    """
    Log in a user.
    """

    log_prefix = "[User Login]"
    logger.info(
        f"{log_prefix} Attempting to log in user: {payload.email}",
    )

    user: Optional[User] = (
        session.query(User).filter(User.email == payload.email).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if not user.check_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
        )

    return user


def create_jwt_with_expiry(
    data: dict,
) -> str:
    """Generate a JWT with given data and expiry.

    Args:
        data (dict): Data to encode in the JWT
        expires_delta (timedelta, optional): Timedelta defining JWT expiry.
        Defaults to 48 hours.

    Returns:
        str: JWT string
    """

    return jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)


def create_user_access_token(
    user: User,
) -> str:
    """Create an Access Token for the given user.

    JWT payload contains user's id, email, and name.

    Args:
        user (User): User to make an access token for.

    Returns:
        str: JWT string
    """

    jwt_payload = UserResponseSchema(
        user_id=user.id,
        email=user.email,
        name=user.name,
    )

    return create_jwt_with_expiry(jwt_payload.model_dump())


def create_success_auth_user_response(user: User, status_code: int) -> JSONResponse:
    user_response = UserResponseSchema(
        user_id=user.id,
        email=user.email,
        name=user.name,
    )
    response = JSONResponse(
        status_code=status_code,
        content=user_response.model_dump(),
    )
    access_token = create_user_access_token(user)
    response.set_cookie(
        key=constants.AUTH_TOKEN_NAME,
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,
        expires=(
            datetime.utcnow() + timedelta(days=constants.ACCESS_TOKEN_EXPIRY_DAYS)
        ).replace(tzinfo=timezone.utc),
    )
    return response


def decode_auth_token(token: str) -> Optional[UserResponseSchema]:
    """Decode the JWT token to get user details."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

    return UserResponseSchema(**payload)


def get_auth_token_data(request: Request) -> UserResponseSchema:
    """Get authentication token data from the request."""
    token = request.cookies.get(constants.AUTH_TOKEN_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )
    token_data = decode_auth_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication token or token has expired",
        )
    return token_data


def get_current_user(request: Request, session: Session = Depends(db)) -> User:
    """Get the current authenticated user or raise an HTTP exception."""
    token_data = get_auth_token_data(request)
    user = None
    if token_data and token_data.user_id:
        user = User.get(session, token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="We couldn't find the user associated with this token, we have logged you out.",
        )
    return user
