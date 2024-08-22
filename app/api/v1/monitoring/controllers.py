from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import db

router = APIRouter()


@router.get("/health")
def health_check(request: Request, session: Session = Depends(db)) -> str:
    """
    Checks the health of hermes - lol.

    It returns 200 if hermes is healthy. hermes is always healthy.
    """
    session.execute(text("SELECT 1"))

    return "OK"
