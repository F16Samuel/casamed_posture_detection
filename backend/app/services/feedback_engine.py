import logging
from typing import List

from app.schemas.posture_response import Metrics

logger = logging.getLogger(__name__)


def generate_feedback(metrics: Metrics) -> List[str]:
    """
    Generates human-readable feedback based on posture metrics.
    """

    feedback = []

    # -----------------------------
    # Neck Angle Feedback
    # -----------------------------
    if metrics.neck_angle > 20:
        feedback.append("Significant forward head posture detected.")
    elif metrics.neck_angle > 10:
        feedback.append("Mild forward head posture detected.")
    else:
        feedback.append("Neck alignment appears well maintained.")

    # -----------------------------
    # Spine Deviation Feedback
    # -----------------------------
    if metrics.spine_vertical_deviation > 10:
        feedback.append("Noticeable spinal deviation from vertical alignment.")
    elif metrics.spine_vertical_deviation > 5:
        feedback.append("Mild trunk deviation observed.")
    else:
        feedback.append("Spine alignment appears stable.")

    # -----------------------------
    # Shoulder Alignment Feedback
    # -----------------------------
    if metrics.shoulder_alignment_difference > 5:
        feedback.append("Significant shoulder asymmetry detected.")
    elif metrics.shoulder_alignment_difference > 2:
        feedback.append("Shoulders are slightly uneven.")
    else:
        feedback.append("Shoulder alignment appears balanced.")

    # -----------------------------
    # Hip Alignment Feedback
    # -----------------------------
    if metrics.hip_alignment_difference > 5:
        feedback.append("Pelvic tilt detected.")
    elif metrics.hip_alignment_difference > 2:
        feedback.append("Minor pelvic imbalance observed.")
    else:
        feedback.append("Hip alignment appears symmetrical.")

    logger.info("Feedback generated successfully.")

    return feedback