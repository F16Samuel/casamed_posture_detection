import os
import json
from typing import Dict, List
from app.core.config import settings


def save_analysis(report_id: str, metadata: Dict, frame_results: List[Dict]) -> str:
    """
    Persist full per-frame posture analysis (including landmarks)
    into a structured JSON file.
    """

    os.makedirs(settings.ANALYSIS_FOLDER, exist_ok=True)

    path = os.path.join(settings.ANALYSIS_FOLDER, f"{report_id}.json")

    payload = {
        "video_metadata": metadata,
        "summary": {
            "total_frames_analyzed": len(frame_results)
        },
        "frame_results": frame_results
    }

    with open(path, "w") as f:
        json.dump(payload, f, indent=2)

    return path


def load_analysis(report_id: str) -> Dict:
    """
    Load stored temporal analysis JSON.
    """

    path = os.path.join(settings.ANALYSIS_FOLDER, f"{report_id}.json")

    if not os.path.exists(path):
        raise FileNotFoundError("Analysis file not found.")

    with open(path, "r") as f:
        return json.load(f)