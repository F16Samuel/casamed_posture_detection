import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings

router = APIRouter()


@router.get("/image/{report_id}")
def get_overlay_image(report_id: str):
    """
    Returns the annotated skeleton overlay image.
    """

    image_path = os.path.join(settings.IMAGE_FOLDER, f"{report_id}.png")

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Overlay image not found.")

    return FileResponse(
        path=image_path,
        media_type="image/png",
        filename=f"{report_id}.png"
    )