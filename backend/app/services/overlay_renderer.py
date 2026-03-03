import os
import cv2
import logging
from typing import Dict

import mediapipe as mp

from app.core.config import settings
from app.schemas.posture_response import Metrics

logger = logging.getLogger(__name__)

mp_pose = mp.solutions.pose


# -----------------------------
# Color Utility
# -----------------------------
def _get_color(value: float, good_threshold: float, moderate_threshold: float):
    """
    Returns BGR color based on severity.
    Green = Good
    Yellow = Moderate
    Red = Poor
    """
    if value <= good_threshold:
        return (0, 200, 0)  # Green
    elif value <= moderate_threshold:
        return (0, 215, 255)  # Yellow
    else:
        return (0, 0, 255)  # Red


def render_overlay(report_id: str, representative_frame, metrics: Metrics) -> str:
    """
    Renders annotated skeleton overlay and saves image.
    """

    image = representative_frame.copy()
    height, width, _ = image.shape

    # Convert BGR to RGB for mediapipe drawing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(rgb_image)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

    # -----------------------------
    # Extract Important Points
    # -----------------------------
    landmarks = results.pose_landmarks.landmark

    def get_point(index):
        return (
            int(landmarks[index].x * width),
            int(landmarks[index].y * height)
        )

    nose = get_point(0)
    left_shoulder = get_point(11)
    right_shoulder = get_point(12)
    left_hip = get_point(23)
    right_hip = get_point(24)

    shoulder_mid = (
        (left_shoulder[0] + right_shoulder[0]) // 2,
        (left_shoulder[1] + right_shoulder[1]) // 2
    )

    hip_mid = (
        (left_hip[0] + right_hip[0]) // 2,
        (left_hip[1] + right_hip[1]) // 2
    )

    # -----------------------------
    # Draw Spine Line
    # -----------------------------
    spine_color = _get_color(metrics.spine_vertical_deviation, 5, 10)
    cv2.line(image, hip_mid, shoulder_mid, spine_color, 3)

    # -----------------------------
    # Draw Shoulder Line
    # -----------------------------
    shoulder_color = _get_color(metrics.shoulder_alignment_difference, 2, 5)
    cv2.line(image, left_shoulder, right_shoulder, shoulder_color, 3)

    # -----------------------------
    # Draw Hip Line
    # -----------------------------
    hip_color = _get_color(metrics.hip_alignment_difference, 2, 5)
    cv2.line(image, left_hip, right_hip, hip_color, 3)

    # -----------------------------
    # Draw Neck Line
    # -----------------------------
    neck_color = _get_color(metrics.neck_angle, 10, 20)
    cv2.line(image, shoulder_mid, nose, neck_color, 3)

    # -----------------------------
    # Annotate Metrics
    # -----------------------------
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(image, f"Neck: {metrics.neck_angle}°",
                (nose[0], nose[1] - 20),
                font, 0.6, neck_color, 2)

    cv2.putText(image, f"Spine: {metrics.spine_vertical_deviation}°",
                (shoulder_mid[0], shoulder_mid[1] - 20),
                font, 0.6, spine_color, 2)

    cv2.putText(image, f"Shoulder diff: {metrics.shoulder_alignment_difference}%",
                (left_shoulder[0], left_shoulder[1] - 20),
                font, 0.6, shoulder_color, 2)

    cv2.putText(image, f"Hip diff: {metrics.hip_alignment_difference}%",
                (left_hip[0], left_hip[1] - 20),
                font, 0.6, hip_color, 2)

    # -----------------------------
    # Save Image
    # -----------------------------
    image_path = os.path.join(settings.IMAGE_FOLDER, f"{report_id}.png")
    cv2.imwrite(image_path, image)

    logger.info(f"Overlay image saved at {image_path}")

    return image_path