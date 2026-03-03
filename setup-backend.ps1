# ================================
# FastAPI Posture Analysis Backend Setup Script
# ================================

$root = "backend"

# Create root directory
New-Item -ItemType Directory -Path $root -Force

# -------------------------------
# Create Main App Structure
# -------------------------------

$folders = @(
    "$root/app",
    "$root/app/api/v1/endpoints",
    "$root/app/core",
    "$root/app/schemas",
    "$root/app/services",
    "$root/app/utils",
    "$root/app/dependencies",
    "$root/storage",
    "$root/storage/images",
    "$root/storage/reports",
    "$root/storage/temp",
    "$root/tests"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force
}

# -------------------------------
# Create Python Files
# -------------------------------

$files = @(
    "$root/app/main.py",
    "$root/app/api/v1/router.py",
    "$root/app/api/v1/endpoints/posture.py",
    "$root/app/api/v1/endpoints/health.py",
    "$root/app/api/v1/endpoints/image.py",
    "$root/app/api/v1/endpoints/report.py",
    "$root/app/core/config.py",
    "$root/app/core/logging.py",
    "$root/app/core/exceptions.py",
    "$root/app/schemas/posture_response.py",
    "$root/app/schemas/health_response.py",
    "$root/app/schemas/error_response.py",
    "$root/app/services/video_processor.py",
    "$root/app/services/pose_estimator.py",
    "$root/app/services/metrics_calculator.py",
    "$root/app/services/scoring_engine.py",
    "$root/app/services/feedback_engine.py",
    "$root/app/services/overlay_renderer.py",
    "$root/app/services/report_generator.py",
    "$root/app/utils/geometry.py",
    "$root/app/utils/file_validator.py",
    "$root/app/utils/frame_selector.py",
    "$root/app/dependencies/rate_limiter.py",
    "$root/tests/test_metrics.py",
    "$root/tests/test_scoring.py",
    "$root/tests/test_api.py",
    "$root/requirements.txt",
    "$root/Dockerfile",
    "$root/.env",
    "$root/.gitignore",
    "$root/README.md"
)

foreach ($file in $files) {
    New-Item -ItemType File -Path $file -Force
}

# -------------------------------
# Add __init__.py files
# -------------------------------

$initFolders = @(
    "$root/app",
    "$root/app/api",
    "$root/app/api/v1",
    "$root/app/api/v1/endpoints",
    "$root/app/core",
    "$root/app/schemas",
    "$root/app/services",
    "$root/app/utils",
    "$root/app/dependencies"
)

foreach ($folder in $initFolders) {
    New-Item -ItemType File -Path "$folder/__init__.py" -Force
}

Write-Host "Backend project structure created successfully!" -ForegroundColor Green