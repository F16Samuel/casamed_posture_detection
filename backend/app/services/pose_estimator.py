import logging
from typing import List, Dict

import cv2
import mediapipe as mp

from app.core.exceptions import NoPersonDetected

logger = logging.getLogger(__name__)

mp_pose = mp.solutions.pose


class PoseEstimator:
    """
    Singleton-style MediaPipe Pose estimator.
    """

    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def extract(self, frames: List) -> List[Dict]:
        """
        Extract pose landmarks for each frame.
        Returns a list of dictionaries (one per frame).
        """

        all_landmarks = []

        for idx, frame in enumerate(frames):
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)

            if not results.pose_landmarks:
                logger.warning(f"No person detected in frame {idx}")
                continue

            landmarks = {}

            for i, landmark in enumerate(results.pose_landmarks.landmark):
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


# Instantiate once (module-level singleton)
pose_estimator = PoseEstimator()


def extract_landmarks(frames: List) -> List[Dict]:
    """
    Public function used by endpoint.
    """
    return pose_estimator.extract(frames)