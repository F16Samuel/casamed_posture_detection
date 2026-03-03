from fastapi import APIRouter

from app.api.v2.endpoints import posture, health, image, report, video


api_router_v2 = APIRouter()

# ----------------------------
# Endpoint Registrations
# ----------------------------

api_router_v2.include_router(
    health.router,
    tags=["Health V2"]
)

api_router_v2.include_router(
    posture.router,
    tags=["Posture Analysis V2"]
)

api_router_v2.include_router(
    image.router,
    tags=["Artifacts V2"]
)

api_router_v2.include_router(
    report.router,
    tags=["Reports V2"]
)

api_router_v2.include_router(video.router, tags=["Video V2"])