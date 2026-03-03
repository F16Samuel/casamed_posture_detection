import os
from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.core.config import settings

router = APIRouter()


@router.get("/report/{report_id}")
def get_temporal_report(report_id: str):

    path = os.path.join(settings.REPORT_FOLDER, f"{report_id}_v2.pdf")

    if not os.path.exists(path):
        return {"error": "Report not found"}

    return FileResponse(path, media_type="application/pdf")