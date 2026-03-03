import logging
import os
from typing import List, Dict

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from app.core.exceptions import NoPersonDetected

logger = logging.getLogger(__name__)


# -------------------------------
# Load Pose Landmarker Model
# -------------------------------

MODEL_PATH = os.path.join("models", "pose_landmarker_full.task")

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_poses=1
)

pose_landmarker = vision.PoseLandmarker.create_from_options(options)


def extract_landmarks(frames: List) -> List[Dict]:
    """
    Extract pose landmarks using MediaPipe Tasks API.
    """

    all_landmarks = []

    for idx, frame in enumerate(frames):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = pose_landmarker.detect(mp_image)

        if not result.pose_landmarks:
            logger.warning(f"No person detected in frame {idx}")
            continue

        landmarks = {}

        for i, landmark in enumerate(result.pose_landmarks[0]):
            landmarks[i] = {
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            }

        all_landmarks.append(landmarks)

    if len(all_landmarks) == 0:
        raise NoPersonDetected()

    logger.info(f"Pose extracted for {len(all_landmarks)} frames.")

    return all_landmarks