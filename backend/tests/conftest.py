import os
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.core.config import settings


@pytest.fixture(scope="session")
def temp_storage():
    """
    Create temporary folders for storage during tests.
    Prevents polluting real storage.
    """
    temp_dir = tempfile.mkdtemp()

    settings.TEMP_FOLDER = os.path.join(temp_dir, "temp")
    settings.VIDEO_FOLDER = os.path.join(temp_dir, "videos")
    settings.REPORT_FOLDER = os.path.join(temp_dir, "reports")
    settings.IMAGE_FOLDER = os.path.join(temp_dir, "images")
    settings.ANALYSIS_FOLDER = os.path.join(temp_dir, "analysis")

    os.makedirs(settings.TEMP_FOLDER, exist_ok=True)
    os.makedirs(settings.VIDEO_FOLDER, exist_ok=True)
    os.makedirs(settings.REPORT_FOLDER, exist_ok=True)
    os.makedirs(settings.IMAGE_FOLDER, exist_ok=True)
    os.makedirs(settings.ANALYSIS_FOLDER, exist_ok=True)

    yield temp_dir

    shutil.rmtree(temp_dir)


@pytest.fixture
def client(temp_storage):
    """
    Provides FastAPI TestClient.
    """
    return TestClient(app)