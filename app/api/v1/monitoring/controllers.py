from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
def health_check(request: Request) -> str:
    """
    Checks the health of hermes - lol.

    It returns 200 if hermes is healthy. hermes is always healthy.
    """

    return "OK"
