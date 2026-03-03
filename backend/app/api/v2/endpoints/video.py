import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.core.config import settings

router = APIRouter()


@router.get("/video/{report_id}")
def get_video(report_id: str):
    path = os.path.join(settings.VIDEO_FOLDER, f"{report_id}.mp4")

    if not os.path.exists(path):
        return {"error": "Video not found"}

    return FileResponse(
        path,
        media_type="video/mp4",
        filename=f"{report_id}.mp4"
)