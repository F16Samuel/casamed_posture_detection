from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    # -----------------------------
    # Application Metadata
    # -----------------------------
    APP_NAME: str = "AI Posture Analysis Service"
    VERSION: str = "1.0.0"

    # -----------------------------
    # CORS Configuration
    # -----------------------------
    ALLOWED_ORIGINS: List[str] = ["*"]

    # -----------------------------
    # Video Constraints (seconds)
    # -----------------------------
    MIN_VIDEO_DURATION: int = 10
    MAX_VIDEO_DURATION: int = 15

    # -----------------------------
    # Supported Video Formats
    # -----------------------------
    SUPPORTED_FORMATS: List[str] = ["mp4", "mov", "avi"]

    # -----------------------------
    # Storage Paths
    # -----------------------------
    STORAGE_ROOT: str = "storage"
    TEMP_FOLDER: str = "storage/temp"
    IMAGE_FOLDER: str = "storage/images"
    REPORT_FOLDER: str = "storage/reports"

    # -----------------------------
    # Performance
    # -----------------------------
    FRAME_SAMPLING_RATE: int = 5  # process every 5th frame

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()