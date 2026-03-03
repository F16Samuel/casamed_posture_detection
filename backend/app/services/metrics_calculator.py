import statistics
import logging
from typing import List, Dict

from app.schemas.posture_response import Metrics
from app.utils.geometry import (
    midpoint,
    vector,
    angle_between,
    vertical_reference
)

logger = logging.getLogger(__name__)

# MediaPipe Landmark Indices
NOSE = 0
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_HIP = 23
RIGHT_HIP = 24


def _extract_point(landmarks: Dict, index: int):
    """
    Extract normalized (x, y) from landmarks dictionary.
    """
    return (landmarks[index]["x"], landmarks[index]["y"])


def _compute_frame_metrics(landmarks: Dict):
    """
    Compute posture metrics for a single frame.
    """

    nose = _extract_point(landmarks, NOSE)
    left_shoulder = _extract_point(landmarks, LEFT_SHOULDER)
    right_shoulder = _extract_point(landmarks, RIGHT_SHOULDER)
    left_hip = _extract_point(landmarks, LEFT_HIP)
    right_hip = _extract_point(landmarks, RIGHT_HIP)

    # Midpoints
    shoulder_mid = midpoint(left_shoulder, right_shoulder)
    hip_mid = midpoint(left_hip, right_hip)

    # ------------------------------------------------
    # Neck Angle (nose to shoulder_mid vs vertical)
    # ------------------------------------------------
    neck_vec = vector(shoulder_mid, nose)
    neck_angle = angle_between(neck_vec, vertical_reference())

    # ------------------------------------------------
    # Spine Deviation (hip_mid to shoulder_mid vs vertical)
    # ------------------------------------------------
    spine_vec = vector(hip_mid, shoulder_mid)
    spine_deviation = angle_between(spine_vec, vertical_reference())

    # ------------------------------------------------
    # Shoulder Alignment Difference (% vertical diff)
    # ------------------------------------------------
    shoulder_diff = abs(left_shoulder[1] - right_shoulder[1]) * 100

    # ------------------------------------------------
    # Hip Alignment Difference (% vertical diff)
    # ------------------------------------------------
    hip_diff = abs(left_hip[1] - right_hip[1]) * 100

    return {
        "neck_angle": neck_angle,
        "spine_vertical_deviation": spine_deviation,
        "shoulder_alignment_difference": shoulder_diff,
        "hip_alignment_difference": hip_diff
    }


def compute_aggregate_metrics(landmarks_per_frame: List[Dict]) -> Metrics:
    """
    Compute median metrics across all frames.
    """

    neck_angles = []
    spine_devs = []
    shoulder_diffs = []
    hip_diffs = []

    for landmarks in landmarks_per_frame:
        frame_metrics = _compute_frame_metrics(landmarks)

        neck_angles.append(frame_metrics["neck_angle"])
        spine_devs.append(frame_metrics["spine_vertical_deviation"])
        shoulder_diffs.append(frame_metrics["shoulder_alignment_difference"])
        hip_diffs.append(frame_metrics["hip_alignment_difference"])

    if len(neck_angles) == 0:
        raise ValueError("No valid frames available for metric aggregation.")

    aggregated_metrics = Metrics(
        neck_angle=round(statistics.median(neck_angles), 2),
        spine_vertical_deviation=round(statistics.median(spine_devs), 2),
        shoulder_alignment_difference=round(statistics.median(shoulder_diffs), 2),
        hip_alignment_difference=round(statistics.median(hip_diffs), 2)
    )

    logger.info(f"Aggregated Metrics: {aggregated_metrics}")

    return aggregated_metrics