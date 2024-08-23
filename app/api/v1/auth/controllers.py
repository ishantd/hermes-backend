from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import constants
from app.api.v1.auth import services
from app.api.v1.auth.models import User
from app.api.v1.auth.schemas import UserResponseSchema, UserSignupSchema
from app.database import db

router = APIRouter()


@router.post("/signup")
def signup(
    payload: UserSignupSchema,
    session: Session = Depends(db),
) -> UserResponseSchema:
    """
    Create a new user.
    """

    logger.info(
        f"[User Signup] Attempting to sign up user: {payload.email}",
    )
    try:
        user: User = services.signup(
            payload=payload,
            session=session,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[User Signup] {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    user_response = UserResponseSchema(
        user_id=user.id,
        email=user.email,
        name=user.name,
    )

    response = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=user_response.model_dump(),
    )

    access_token = services.create_user_access_token(user)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=True,
        expires=(
            datetime.utcnow() + timedelta(days=constants.ACCESS_TOKEN_EXPIRY_DAYS)
        ).replace(tzinfo=timezone.utc),
    )

    return response
