from pydantic import BaseModel
from typing import List, Dict

class Metrics(BaseModel):
    neck_angle: float
    shoulder_alignment_difference: float
    hip_alignment_difference: float
    spine_vertical_deviation: float


class Artifacts(BaseModel):
    skeleton_image_url: str
    pdf_report_url: str


class PostureResponse(BaseModel):
    status: str
    report_id: str
    posture_score: float
    classification: str
    metrics: Metrics
    feedback: List[str]
    artifacts: Artifacts
    processing_time_seconds: float