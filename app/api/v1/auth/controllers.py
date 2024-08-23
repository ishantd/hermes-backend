from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import constants
from app.api.v1.auth import services
from app.api.v1.auth.models import User
from app.api.v1.auth.schemas import (
    UserLoginSchema,
    UserResponseSchema,
    UserSignupSchema,
)
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

    response = services.create_success_auth_user_response(user, status.HTTP_201_CREATED)

    return response


@router.post("/login")
def login(
    payload: UserLoginSchema,
    session: Session = Depends(db),
) -> UserResponseSchema:
    """
    Log in a user.
    """

    logger.info(
        f"[User Login] Attempting to log in user: {payload.email}",
    )
    try:
        user: User = services.login(
            payload=payload,
            session=session,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[User Login] {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    response = services.create_success_auth_user_response(user, status.HTTP_200_OK)

    return response


@router.post("/logout")
def logout() -> JSONResponse:
    """
    Log out a user.
    """

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Logged out."},
    )

    response.delete_cookie(
        key=constants.AUTH_TOKEN_NAME,
    )

    return response


@router.get("/whoami")
def whoami(user: User = Depends(services.get_current_user)):
    """
    Get the current user.
    """
    return services.create_success_auth_user_response(user, status.HTTP_200_OK)
