import os
import cv2
from app.core.config import settings
from app.services.analysis_writer import load_analysis
from app.services.overlay_renderer import draw_analytical_overlay


def generate_event_thumbnails(report_id: str, events: list) -> list:
    """
    Generate annotated thumbnails for flagged posture events.
    Uses original frame indices for correct mapping.
    """

    os.makedirs(settings.IMAGE_FOLDER, exist_ok=True)

    analysis = load_analysis(report_id)
    frame_results = analysis["frame_results"]

    # Build fast lookup dictionary
    frame_lookup = {r["frame_index"]: r for r in frame_results}

    video_path = os.path.join(settings.TEMP_FOLDER, f"{report_id}.mp4")
    cap = cv2.VideoCapture(video_path)

    thumbnails = []

    for event in events:

        original_frame_index = event["frame_index"]

        # Jump directly to correct frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, original_frame_index)

        ret, frame = cap.read()
        if not ret:
            continue

        result = frame_lookup.get(original_frame_index)
        if result is None:
            continue

        landmarks = result["landmarks"]

        # Normalize JSON string keys
        if isinstance(landmarks, dict):
            landmarks = {int(k): v for k, v in landmarks.items()}

        annotated = draw_analytical_overlay(
            frame,
            landmarks,
            result["metrics"]
        )

        image_path = os.path.join(
            settings.IMAGE_FOLDER,
            f"{report_id}_frame_{original_frame_index}.png"
        )

        cv2.imwrite(image_path, annotated)

        thumbnails.append({
            "path": image_path,
            "timestamp": event["timestamp"],
            "score": event["score"],
            "issue": event["primary_issue"]
        })

    cap.release()

    return thumbnails