from typing import List, Dict
from statistics import mean


# ----------------------------
# Heuristic Thresholds
# ----------------------------
NECK_THRESHOLD = 20
SPINE_THRESHOLD = 10
SCORE_THRESHOLD = 65

SCORE_SIMILARITY = 3
ANGLE_SIMILARITY = 2
TIME_WINDOW = 1.0  # seconds


def determine_primary_issue(metrics: Dict) -> str:
    """
    Determine dominant posture issue for a frame.
    """

    neck = metrics["neck_angle"]
    spine = metrics["spine_vertical_deviation"]
    shoulder = metrics["shoulder_alignment_difference"]
    hip = metrics["hip_alignment_difference"]

    max_value = max(neck, spine, shoulder, hip)

    if max_value == neck:
        return "Forward head posture"
    elif max_value == spine:
        return "Spinal deviation"
    elif max_value == shoulder:
        return "Shoulder asymmetry"
    else:
        return "Pelvic imbalance"


def extract_flagged_events(frame_results: List[Dict]) -> Dict:
    """
    Extract flagged posture events and cluster similar frames.
    """

    flagged = []

    # Step 1 — Identify problematic frames
    for frame in frame_results:

        metrics = frame["metrics"]
        score = frame["score"]

        if (
            score < SCORE_THRESHOLD or
            metrics["neck_angle"] > NECK_THRESHOLD or
            metrics["spine_vertical_deviation"] > SPINE_THRESHOLD
        ):
            flagged.append({
                "frame_index": frame["frame_index"],   # <-- ADD THIS
                "timestamp": frame["timestamp"],
                "score": score,
                "metrics": metrics,
                "issue": determine_primary_issue(metrics)
            })

    if not flagged:
        return {
            "percent_time_bad": 0,
            "events": []
        }

    # Step 2 — Cluster similar frames
    clustered = []
    current_cluster = [flagged[0]]

    for frame in flagged[1:]:

        last = current_cluster[-1]

        if (
            abs(frame["score"] - last["score"]) < SCORE_SIMILARITY and
            abs(frame["metrics"]["neck_angle"] - last["metrics"]["neck_angle"]) < ANGLE_SIMILARITY and
            abs(frame["timestamp"] - last["timestamp"]) < TIME_WINDOW
        ):
            current_cluster.append(frame)
        else:
            clustered.append(current_cluster)
            current_cluster = [frame]

    clustered.append(current_cluster)

    # Step 3 — Pick representative frame per cluster
    events = []

    for cluster in clustered:
        worst_frame = min(cluster, key=lambda x: x["score"])

        events.append({
        "frame_index": worst_frame["frame_index"],
        "timestamp": worst_frame["timestamp"],
        "score": worst_frame["score"],
        "primary_issue": worst_frame["issue"]
    })

    # Step 4 — Compute % time in bad posture
    total_frames = len(frame_results)
    bad_frames = len(flagged)

    percent_time_bad = round((bad_frames / total_frames) * 100, 2)

    return {
        "percent_time_bad": percent_time_bad,
        "events": events
    }