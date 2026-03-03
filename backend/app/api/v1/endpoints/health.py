from fastapi import APIRouter
from app.schemas.health_response import HealthResponse
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint to verify service availability.
    Used for monitoring and deployment readiness.
    """
    return HealthResponse(
        status="ok",
        service=settings.APP_NAME,
        version=settings.VERSION
    )