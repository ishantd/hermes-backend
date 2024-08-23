import jwt
from fastapi import HTTPException, status
from fastapi.logger import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import constants
from app.api.v1.auth.models import User
from app.api.v1.auth.schemas import UserResponseSchema, UserSignupSchema
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
