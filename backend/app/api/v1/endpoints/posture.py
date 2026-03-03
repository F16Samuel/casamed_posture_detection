import os
import uuid
import time
import logging

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.schemas.posture_response import PostureResponse
from app.core.config import settings
from app.core.exceptions import InvalidVideoFormat
from app.services.video_processor import process_video
from app.services.pose_estimator import extract_landmarks
from app.services.metrics_calculator import compute_aggregate_metrics
from app.services.scoring_engine import compute_posture_score
from app.services.feedback_engine import generate_feedback
from app.services.overlay_renderer import render_overlay
from app.services.report_generator import generate_pdf_report

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze-posture", response_model=PostureResponse)
async def analyze_posture(file: UploadFile = File(...)):
    """
    Accepts a posture video and returns posture analysis results.
    """

    start_time = time.time()

    # ----------------------------------
    # Validate File Extension
    # ----------------------------------
    filename = file.filename
    extension = filename.split(".")[-1].lower()

    if extension not in settings.SUPPORTED_FORMATS:
        raise InvalidVideoFormat()

    # ----------------------------------
    # Save Temporary File
    # ----------------------------------
    report_id = str(uuid.uuid4())[:8]
    temp_path = os.path.join(settings.TEMP_FOLDER, f"{report_id}.{extension}")

    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    logger.info(f"Saved uploaded file to {temp_path}")

    # ----------------------------------
    # Process Video (Frame Extraction)
    # ----------------------------------
    frames = process_video(temp_path)

    # ----------------------------------
    # Pose Estimation
    # ----------------------------------
    landmarks_per_frame = extract_landmarks(frames)

    # ----------------------------------
    # Compute Metrics
    # ----------------------------------
    metrics = compute_aggregate_metrics(landmarks_per_frame)

    # ----------------------------------
    # Compute Score & Classification
    # ----------------------------------
    posture_score, classification = compute_posture_score(metrics)

    # ----------------------------------
    # Generate Feedback
    # ----------------------------------
    feedback = generate_feedback(metrics)

    # ----------------------------------
    # Render Skeleton Overlay
    # ----------------------------------
    representative_frame = frames[0]
    representative_landmarks = landmarks_per_frame[0]

    image_path = render_overlay(
        report_id=report_id,
        representative_frame=representative_frame,
        representative_landmarks=representative_landmarks,
        metrics=metrics
    )

    # ----------------------------------
    # Generate PDF Report
    # ----------------------------------
    pdf_path = generate_pdf_report(
        report_id=report_id,
        posture_score=posture_score,
        classification=classification,
        metrics=metrics,
        feedback=feedback,
        image_path=image_path
    )

    # ----------------------------------
    # Cleanup Temp File
    # ----------------------------------
    os.remove(temp_path)

    processing_time = round(time.time() - start_time, 2)

    logger.info(f"Posture analysis completed in {processing_time}s")

    return PostureResponse(
        status="success",
        report_id=report_id,
        posture_score=posture_score,
        classification=classification,
        metrics=metrics,
        feedback=feedback,
        artifacts={
            "skeleton_image_url": f"/api/v1/image/{report_id}",
            "pdf_report_url": f"/api/v1/report/{report_id}"
        },
        processing_time_seconds=processing_time
    )