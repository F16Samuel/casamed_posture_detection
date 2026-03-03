import logging
from typing import Tuple

from app.schemas.posture_response import Metrics

logger = logging.getLogger(__name__)


# -------------------------------
# Weight Distribution
# -------------------------------
WEIGHTS = {
    "neck": 0.35,
    "spine": 0.30,
    "shoulder": 0.175,
    "hip": 0.175
}


# -------------------------------
# Penalty Thresholds
# -------------------------------

def _neck_penalty(angle: float) -> float:
    """
    Penalize neck angle progressively.
    """
    if angle <= 10:
        return 0
    elif angle <= 20:
        return (angle - 10) * 2
    else:
        return 20 + (angle - 20) * 3


def _spine_penalty(angle: float) -> float:
    """
    Penalize spine deviation progressively.
    """
    if angle <= 5:
        return 0
    elif angle <= 10:
        return (angle - 5) * 2
    else:
        return 10 + (angle - 10) * 3


def _alignment_penalty(diff: float) -> float:
    """
    Penalize shoulder/hip alignment difference.
    diff is already in percentage scale.
    """
    if diff <= 2:
        return 0
    elif diff <= 5:
        return (diff - 2) * 3
    else:
        return 9 + (diff - 5) * 4


def compute_posture_score(metrics: Metrics) -> Tuple[float, str]:
    """
    Computes final posture score (0–100)
    and classification (Good / Fair / Poor).
    """

    neck_pen = _neck_penalty(metrics.neck_angle)
    spine_pen = _spine_penalty(metrics.spine_vertical_deviation)
    shoulder_pen = _alignment_penalty(metrics.shoulder_alignment_difference)
    hip_pen = _alignment_penalty(metrics.hip_alignment_difference)

    total_penalty = (
        neck_pen * WEIGHTS["neck"] +
        spine_pen * WEIGHTS["spine"] +
        shoulder_pen * WEIGHTS["shoulder"] +
        hip_pen * WEIGHTS["hip"]
    )

    score = max(0, round(100 - total_penalty, 2))

    # -------------------------------
    # Classification
    # -------------------------------
    if score >= 85:
        classification = "Good"
    elif score >= 65:
        classification = "Fair"
    else:
        classification = "Poor"

    logger.info(f"Computed Posture Score: {score} ({classification})")

    return score, classification