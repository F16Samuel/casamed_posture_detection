import os
import cv2
import logging
from typing import Dict

from app.core.config import settings
from app.schemas.posture_response import Metrics

logger = logging.getLogger(__name__)


# -----------------------------
# Landmark Connections (Manual)
# -----------------------------
POSE_CONNECTIONS = [
    (11, 12),  # shoulders
    (11, 23),  # left torso
    (12, 24),  # right torso
    (23, 24),  # hips
    (0, 11),   # nose to left shoulder
    (0, 12)    # nose to right shoulder
]


# -----------------------------
# Color Utility
# -----------------------------
def _get_color(value: float, good_threshold: float, moderate_threshold: float):
    if value <= good_threshold:
        return (0, 200, 0)  # Green
    elif value <= moderate_threshold:
        return (0, 215, 255)  # Yellow
    else:
        return (0, 0, 255)  # Red


def render_overlay(
    report_id: str,
    representative_frame,
    representative_landmarks: Dict,
    metrics: Metrics
) -> str:
    """
    Render annotated overlay using precomputed landmarks.
    """

    image = representative_frame.copy()
    height, width, _ = image.shape

    def get_point(index):
        lm = representative_landmarks[index]
        return (
            int(lm["x"] * width),
            int(lm["y"] * height)
        )

    # -----------------------------
    # Draw Skeleton Connections
    # -----------------------------
    for start, end in POSE_CONNECTIONS:
        p1 = get_point(start)
        p2 = get_point(end)
        cv2.line(image, p1, p2, (255, 255, 255), 2)

    # Extract important points
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
    # Draw Analytical Lines
    # -----------------------------
    spine_color = _get_color(metrics.spine_vertical_deviation, 5, 10)
    shoulder_color = _get_color(metrics.shoulder_alignment_difference, 2, 5)
    hip_color = _get_color(metrics.hip_alignment_difference, 2, 5)
    neck_color = _get_color(metrics.neck_angle, 10, 20)

    cv2.line(image, hip_mid, shoulder_mid, spine_color, 3)
    cv2.line(image, left_shoulder, right_shoulder, shoulder_color, 3)
    cv2.line(image, left_hip, right_hip, hip_color, 3)
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