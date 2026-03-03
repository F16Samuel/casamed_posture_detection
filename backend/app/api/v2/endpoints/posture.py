import os
import uuid
import time
import logging

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import InvalidVideoFormat
from app.services.video_processor import extract_frames_from_video
from app.services.pose_estimator import extract_landmarks_with_index
from app.services.metrics_calculator import compute_frame_metrics
from app.services.scoring_engine import compute_posture_score
from app.services.analysis_writer import save_analysis
from app.services.temporal_aggregator import weighted_overall_score
from app.services.temporal_flagger import extract_flagged_events
from app.services.video_renderer import generate_annotated_video
from app.services.temporal_report_generator import generate_temporal_pdf
from app.services.event_thumbnail_generator import generate_event_thumbnails

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze")
async def analyze_posture_v2(file: UploadFile = File(...)):
    """
    Full-frame temporal posture analysis.
    Stores per-frame metrics, scores, and landmarks.
    Applies 75-25 weighted aggregation favoring bad posture.
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
    os.makedirs(settings.TEMP_FOLDER, exist_ok=True)

    temp_path = os.path.join(settings.TEMP_FOLDER, f"{report_id}.{extension}")

    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    logger.info(f"[v2] Saved uploaded file to {temp_path}")

    # ----------------------------------
    # Extract ALL Frames
    # ----------------------------------
    frames, sampled_indices, fps, total_frames, duration = extract_frames_from_video(temp_path)



    # ----------------------------------
    # Pose Estimation (Full-frame)
    # ----------------------------------
    landmarks_per_frame = extract_landmarks_with_index(
        frames,
        sampled_indices
    )
    frame_results = []

    # ----------------------------------
    # Per-frame Metrics + Scoring
    # ----------------------------------
    for frame_data in landmarks_per_frame:

        frame_index = frame_data["frame_index"]
        landmarks = frame_data["landmarks"]

        metrics_obj = compute_frame_metrics(landmarks)

        score, classification = compute_posture_score(metrics_obj)

        frame_results.append({
            "frame_index": frame_index,
            "timestamp": round(frame_index / fps, 3),
            "metrics": metrics_obj.dict(),   # store as dict
            "score": score,
            "classification": classification,
            "landmarks": landmarks
        })

    if not frame_results:
        os.remove(temp_path)
        return JSONResponse(
            status_code=422,
            content={"status": "error", "message": "No valid posture frames detected."}
        )

    # ----------------------------------
    # Weighted Overall Score (75-25)
    # ----------------------------------
    overall_score = weighted_overall_score(frame_results)
    
    # ----------------------------------
    # Extract Flagged Temporal Events
    # ----------------------------------
    flagging_result = extract_flagged_events(frame_results)

    

    # ----------------------------------
    # Save Full Analysis JSON
    # ----------------------------------
    metadata = {
        "fps": fps,
        "total_frames": total_frames,
        "duration_seconds": duration
    }

    analysis_path = save_analysis(
        report_id=report_id,
        metadata=metadata,
        frame_results=frame_results
    )

    logger.info(f"[v2] Analysis saved at {analysis_path}")
    
    # ----------------------------------
    # Generate 60 FPS Annotated Video
    # ----------------------------------
    annotated_video_path = generate_annotated_video(
        report_id=report_id,
        original_video_path=temp_path
    )

    # ----------------------------------
    # Generate Event Thumbnails
    # ----------------------------------
    thumbnails = generate_event_thumbnails(
        report_id=report_id,
        events=flagging_result["events"]
    )

    # ----------------------------------
    # Cleanup Temp File
    # ----------------------------------
    os.remove(temp_path)

    processing_time = round(time.time() - start_time, 2)

    logger.info(f"[v2] Full temporal posture analysis completed in {processing_time}s")

    # ----------------------------------
    # Generate Temporal PDF
    # ----------------------------------
    pdf_path = generate_temporal_pdf(
        report_id=report_id,
        overall_score=overall_score,
        flagging_result=flagging_result,
        processing_time=processing_time,
        thumbnails=thumbnails
    )

    return {
        "status": "success",
        "report_id": report_id,
        "overall_score": overall_score,
        "frames_analyzed": len(frame_results),
        "percent_time_bad": flagging_result["percent_time_bad"],
        "flagged_events": flagging_result["events"],
        "artifacts": {
            "annotated_video_url": f"/api/v2/video/{report_id}",
            "pdf_report_url": f"/api/v2/report/{report_id}"
        },
        "processing_time_seconds": processing_time
    }