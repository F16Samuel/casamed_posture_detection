import os
import subprocess
import cv2
from app.core.config import settings
from app.services.analysis_writer import load_analysis
from app.services.overlay_renderer import draw_analytical_overlay


def generate_annotated_video(report_id: str, original_video_path: str) -> str:
    """
    Generate smooth 60 FPS annotated video.
    Uses last-known-pose hold strategy to prevent flickering.
    """

    os.makedirs(settings.VIDEO_FOLDER, exist_ok=True)
    output_path = os.path.join(settings.VIDEO_FOLDER, f"{report_id}.mp4")

    analysis = load_analysis(report_id)
    frame_results = analysis["frame_results"]

    # Build fast lookup dictionary by ORIGINAL frame index
    frame_lookup = {r["frame_index"]: r for r in frame_results}

    cap = cv2.VideoCapture(original_video_path)

    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps <= 0:
        original_fps = 30  # fallback safety

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    target_fps = 60
    frame_multiplier = target_fps / original_fps

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, target_fps, (width, height), True)

    frame_index = 0
    frame_accumulator = 0.0
    current_result = None  # Holds last valid analyzed frame

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # If this frame was analyzed, update current_result
        if frame_index in frame_lookup:
            current_result = frame_lookup[frame_index]

        # If we have a valid pose result, keep drawing it
        if current_result is not None:
            landmarks = current_result["landmarks"]

            # Normalize JSON string keys to int
            if isinstance(landmarks, dict):
                landmarks = {int(k): v for k, v in landmarks.items()}

            frame = draw_analytical_overlay(
                frame,
                landmarks,
                current_result["metrics"]
            )

        # --- Proper FPS resampling ---
        frame_accumulator += frame_multiplier

        while frame_accumulator >= 1.0:
            out.write(frame)
            frame_accumulator -= 1.0

        frame_index += 1

    cap.release()
    out.release()

    temp_path = output_path.replace(".mp4", "_temp.mp4")
    os.rename(output_path, temp_path)

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", temp_path,
        "-vcodec", "libx264",
        "-preset", "fast",
        "-profile:v", "baseline",
        "-level", "3.0",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path
    ])

    os.remove(temp_path)
    cv2.destroyAllWindows()

    return output_path