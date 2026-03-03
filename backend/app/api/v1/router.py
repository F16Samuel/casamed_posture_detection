from fastapi import APIRouter

from app.api.v1.endpoints import posture, health, image, report


api_router = APIRouter()

# ----------------------------
# Endpoint Registrations
# ----------------------------

api_router.include_router(
    health.router,
    tags=["Health"]
)

api_router.include_router(
    posture.router,
    tags=["Posture Analysis"]
)

api_router.include_router(
    image.router,
    tags=["Artifacts"]
)

api_router.include_router(
    report.router,
    tags=["Artifacts"]
)