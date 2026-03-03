import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings

router = APIRouter()


@router.get("/report/{report_id}")
def get_pdf_report(report_id: str):
    """
    Returns the generated PDF posture report.
    """

    pdf_path = os.path.join(settings.REPORT_FOLDER, f"{report_id}.pdf")

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF report not found.")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"{report_id}.pdf"
    )