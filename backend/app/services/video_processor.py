import cv2
import os
import logging

from typing import List
from app.core.config import settings
from app.core.exceptions import InvalidVideoDuration

logger = logging.getLogger(__name__)


def process_video(video_path: str) -> List:
    """
    Processes the uploaded video:
    - Validates duration
    - Extracts frames
    - Applies frame sampling
    Returns a list of sampled frames (BGR format).
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError("Uploaded video file not found.")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Unable to open video file.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = frame_count / fps if fps > 0 else 0

    logger.info(f"Video FPS: {fps}")
    logger.info(f"Total Frames: {frame_count}")
    logger.info(f"Video Duration: {duration:.2f} seconds")

    # ----------------------------------------
    # Validate Duration
    # ----------------------------------------
    if duration < settings.MIN_VIDEO_DURATION or duration > settings.MAX_VIDEO_DURATION:
        cap.release()
        raise InvalidVideoDuration()

    frames = []
    frame_index = 0
    sampling_rate = settings.FRAME_SAMPLING_RATE

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % sampling_rate == 0:
            frames.append(frame)

        frame_index += 1

    cap.release()

    logger.info(f"Extracted {len(frames)} sampled frames.")

    if len(frames) == 0:
        raise ValueError("No frames extracted from video.")

    return frames

def extract_frames_from_video(video_path: str) -> List:
    """
    Processes the uploaded video:
    - Validates duration
    - Extracts frames
    - Applies frame sampling
    Returns a list of sampled frames (BGR format).
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError("Uploaded video file not found.")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Unable to open video file.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = frame_count / fps if fps > 0 else 0

    logger.info(f"Video FPS: {fps}")
    logger.info(f"Total Frames: {frame_count}")
    logger.info(f"Video Duration: {duration:.2f} seconds")

    # ----------------------------------------
    # Validate Duration
    # ----------------------------------------
    if duration < settings.MIN_VIDEO_DURATION or duration > settings.MAX_VIDEO_DURATION:
        cap.release()
        raise InvalidVideoDuration()

    

    frames = []
    sampling_rate = settings.FRAME_SAMPLING_RATE
    sampled_indices = []
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % sampling_rate == 0:
            frames.append(frame)
            sampled_indices.append(frame_index)

        frame_index += 1

    cap.release()

    logger.info(f"Extracted {len(frames)} sampled frames.")

    if len(frames) == 0:
        raise ValueError("No frames extracted from video.")

    return frames, sampled_indices, fps, frame_count, duration