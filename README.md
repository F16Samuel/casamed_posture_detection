# PostureAI — AI-Powered Temporal Posture Analysis Platform

PostureAI is a full-stack AI-powered posture assessment system that analyzes short posture videos (10–15 seconds) and generates:

- Temporal posture score (0–100)
- Annotated skeleton overlay video (60 FPS)
- Posture metrics (neck, spine, shoulder, hip alignment)
- Flagged posture events
- Downloadable PDF report

The system combines computer vision, temporal aggregation, and frontend visualization into a medical-grade web experience.

---

## 🚀 Tech Stack

### Backend
- FastAPI
- MediaPipe Pose
- OpenCV
- ReportLab
- Python 3.12

### Frontend
- React (Vite + TypeScript)
- Axios
- Framer Motion
- Tailwind CSS

---

# 🛠 Setup Instructions

---

## 1️⃣ Backend Setup

### Clone repository

```bash
git clone <repo-url>
cd backend
````

### Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will run at:

```
http://localhost:8000
```

---

## 2️⃣ Frontend Setup

```bash
cd frontend
npm install
```

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Run development server:

```bash
npm run dev
```

Frontend will run at:

```
http://localhost:8080
```

---

# 📡 API Usage

---

## Analyze Posture (Temporal v2)

**Endpoint**

```
POST /api/v2/analyze
```

**Request**

* Content-Type: `multipart/form-data`
* Field: `file`
* Accepted formats: `.mp4`, `.mov`, `.avi`
* Duration: 10–15 seconds

### Example (cURL)

```bash
curl -X POST http://localhost:8000/api/v2/analyze \
  -F "file=@posture_video.mp4"
```

### Response

```json
{
  "status": "success",
  "report_id": "a1b2c3d4",
  "overall_score": 82.34,
  "frames_analyzed": 142,
  "percent_time_bad": 18.4,
  "flagged_events": [
    {
      "timestamp": 4.2,
      "score": 58.3,
      "primary_issue": "Forward head posture"
    }
  ],
  "artifacts": {
    "annotated_video_url": "/api/v2/video/a1b2c3d4",
    "pdf_report_url": "/api/v2/report/a1b2c3d4"
  },
  "processing_time_seconds": 3.52
}
```

---

## Retrieve Annotated Video

```
GET /api/v2/video/{report_id}
```

Returns 60 FPS annotated MP4 video.

---

## Retrieve PDF Report

```
GET /api/v2/report/{report_id}
```

Returns downloadable PDF posture report.

---

## Health Check

```
GET /api/v2/health
```

---

# 🏗 Architecture Overview

```
                ┌──────────────┐
                │   Frontend   │
                │ React + Vite │
                └──────┬───────┘
                       │ REST API
                ┌──────▼───────┐
                │   FastAPI    │
                └──────┬───────┘
                       │
      ┌────────────────┼────────────────┐
      │                │                │
┌─────▼─────┐   ┌──────▼──────┐   ┌─────▼─────┐
│ Pose Est. │   │ Metrics Calc│   │ Aggregator│
│ MediaPipe │   │ Frame-Level │   │ Temporal  │
└─────┬─────┘   └──────┬──────┘   └─────┬─────┘
      │                │                │
      └────────────────▼────────────────┘
               JSON Analysis Storage
                       │
        ┌──────────────┼──────────────┐
        │              │              │
  Annotated Video   PDF Report   Event Thumbnails
```

---

# 📊 How the Posture Score is Computed

PostureAI uses a hybrid frame-level + temporal aggregation approach.

---

## 1️⃣ Frame-Level Metrics

For each frame:

* Neck angle (head forward deviation)
* Spine vertical deviation
* Shoulder alignment difference
* Hip alignment difference

Each metric is computed using landmark geometry.

---

## 2️⃣ Frame Score Calculation (Detailed Formulation)

Each frame receives a posture score between **0–100** using a weighted penalty-based scoring model.

The frame score is computed as:

Score = 100 − (P_neck + P_spine + P_shoulder + P_hip)

Each penalty term reflects the severity of deviation from clinically reasonable posture thresholds. The total possible penalty is capped at 100.

---

### 📐 Metric Definitions

Let:

- N  = Neck angle (degrees)
- S  = Spine vertical deviation (degrees)
- Sh = Shoulder alignment difference (%)
- H  = Hip alignment difference (%)

---

## 🔹 1️⃣ Neck Penalty (Weight: 35%)

Forward head posture carries the highest weight due to its strong association with musculoskeletal strain.

Threshold Zones:

- Good: N ≤ 10°
- Moderate: 10° < N ≤ 20°
- Poor: N > 20°

Penalty Function:

If N ≤ 10:
    P_neck = 0

If 10 < N ≤ 20:
    P_neck = 1.75 × (N − 10)

If N > 20:
    P_neck = 17.5 + 2.5 × (N − 20)

Maximum contribution: 35 points

---

## 🔹 2️⃣ Spine Penalty (Weight: 30%)

Spinal deviation is critical for long-term postural integrity.

Threshold Zones:

- Good: S ≤ 5°
- Moderate: 5° < S ≤ 10°
- Poor: S > 10°

Penalty Function:

If S ≤ 5:
    P_spine = 0

If 5 < S ≤ 10:
    P_spine = 3 × (S − 5)

If S > 10:
    P_spine = 15 + 3 × (S − 10)

Maximum contribution: 30 points

---

## 🔹 3️⃣ Shoulder Penalty (Weight: 20%)

Shoulder asymmetry reflects muscular imbalance and compensation.

Threshold Zones:

- Good: Sh ≤ 2%
- Moderate: 2% < Sh ≤ 5%
- Poor: Sh > 5%

Penalty Function:

If Sh ≤ 2:
    P_shoulder = 0

If 2 < Sh ≤ 5:
    P_shoulder = 2 × (Sh − 2)

If Sh > 5:
    P_shoulder = 6 + 2 × (Sh − 5)

Maximum contribution: 20 points

---

## 🔹 4️⃣ Hip Penalty (Weight: 15%)

Pelvic imbalance affects spinal alignment and kinetic chain stability.

Threshold Zones:

- Good: H ≤ 2%
- Moderate: 2% < H ≤ 5%
- Poor: H > 5%

Penalty Function:

If H ≤ 2:
    P_hip = 0

If 2 < H ≤ 5:
    P_hip = 1.5 × (H − 2)

If H > 5:
    P_hip = 4.5 + 1.5 × (H − 5)

Maximum contribution: 15 points

---

## ⚖️ Weight Distribution Summary

| Metric    | Maximum Penalty | Weight Contribution |
|-----------|-----------------|--------------------|
| Neck      | 35              | 35%                |
| Spine     | 30              | 30%                |
| Shoulder  | 20              | 20%                |
| Hip       | 15              | 15%                |
| **Total** | **100**         | **100%**           |

---

## 🎯 Final Frame Score

Frame Score = 100 − Total_Penalty

The score is clipped to:

0 ≤ Score ≤ 100

Higher scores indicate better postural alignment.

---

## 🧠 Design Rationale

- Neck and spine deviations are weighted higher due to stronger clinical relevance.
- Progressive penalty scaling ensures mild deviations are not over-penalized.
- Severe deviations increase penalty sharply to reflect biomechanical risk.
- The scoring model is deterministic and interpretable.
- No black-box machine learning scoring is used in v2.
---

## 3️⃣ Temporal Weighted Aggregation

Rather than simple averaging:

* Bad posture frames are weighted 75%
* Good posture frames are weighted 25%

This prevents brief corrections from hiding sustained poor posture.

```
Overall Score = 0.75 * BadFrameMean + 0.25 * GoodFrameMean
```

---

## 4️⃣ Event Detection

Frames are flagged if:

* Score < threshold
* Neck angle > threshold
* Spine deviation > threshold

Similar frames are clustered using:

* Time proximity
* Score similarity
* Angle similarity

Each cluster produces one representative flagged event.

---

# ⚠️ Limitations

1. Single-person assumption
   Only one subject is supported per frame.

2. 2D landmark limitation
   Depth estimation is limited; no full 3D biomechanical modeling.

3. Camera positioning sensitivity
   Extreme angles can reduce accuracy.

4. Lighting dependence
   Poor lighting reduces landmark precision.

5. Short duration
   Designed for 10–15 second posture snapshots.

6. Heuristic thresholds
   Current penalty model is rule-based, not learned from medical datasets.

# 🧪 Backend Testing Architecture

The backend includes a structured test suite using **pytest** with isolated storage and full API validation.

---

## 📂 Test Structure

backend/
├── tests/
│   ├── conftest.py
│   ├── test_scoring_engine.py
│   ├── test_metrics_calculator.py
│   ├── test_temporal_aggregator.py
│   ├── test_flagger.py
│   ├── test_api_v2.py
│   └── test_video_pipeline.py

---

## 🧱 Test Categories

### 1️⃣ Unit Tests

Validate core computational logic:

- Frame scoring engine
- Metric calculations
- Temporal weighted aggregation
- Event clustering and flagging

These tests ensure mathematical correctness and deterministic behavior.

---

### 2️⃣ API Integration Tests

Validate:

- `/api/v2/health`
- File validation logic
- Error handling (400 / 422)
- Successful JSON structure

Uses FastAPI `TestClient`.

---

### 3️⃣ End-to-End Video Pipeline Test

Validates:

- Video upload
- Frame extraction
- Landmark processing
- Score computation
- Annotated video generation
- PDF generation
- JSON analysis persistence

This ensures the complete system works cohesively.

---

## 🔒 Storage Isolation via `conftest.py`

All tests run in a **temporary isolated directory**.

`conftest.py`:

- Overrides storage paths
- Creates temporary folders
- Cleans up automatically after test session

This prevents test runs from polluting production storage.

---

## ▶️ Running Tests

From backend root:

```bash
pytest -v
````

Expected output:

```
5 passed in XX.XXs
```

---

## ⚠️ Current Warning

Pydantic v2 deprecation warning:

```
metrics_obj.dict() → should be replaced with model_dump()
```

Planned update:

```python
metrics_obj.model_dump()
```

This does not affect functionality.
---

# 🐳 Dockerized Deployment

The project is fully containerized using Docker and Docker Compose.

This enables:

- Isolated backend execution (FastAPI + ML stack)
- Production-grade frontend build served via Nginx
- Networked service communication
- Persistent storage volumes
- Portable deployment across environments

---

## 🏗 Architecture Overview

```

Browser → Nginx (Frontend Container) → FastAPI (Backend Container)
→ ML Processing (MediaPipe / TensorFlow Lite)
→ Video Rendering + PDF Generation
→ Persistent Storage Volume

```

---

## 📂 Project Structure

```

casamed_posture_detection/
│
├── backend/
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/
│   ├── Dockerfile
│   └── .dockerignore
│
└── docker-compose.yml

```

---

## 🧱 Backend Container

- Base: python:3.11-slim
- Includes:
  - OpenCV
  - FFmpeg
  - TensorFlow Lite
  - MediaPipe
  - FastAPI
- Runs via:
```

uvicorn app.main:app --host 0.0.0.0 --port 8000

```

---

## 🌐 Frontend Container

- Multi-stage build:
- Stage 1: Node build (Vite)
- Stage 2: Nginx static serving
- Serves optimized production build
- Exposed on port 3000

---

## 🔗 Container Networking

Inside Docker network:

- Backend reachable at:
```

[http://backend:8000](http://backend:8000)

```

Frontend environment variable:

```

VITE_API_BASE_URL=[http://backend:8000/api/v2](http://backend:8000/api/v2)

````

---

## 📦 Running the Application

From project root:

```bash
docker compose build
docker compose up
````

Access:

Frontend → [http://localhost:3000](http://localhost:3000)
Backend → [http://localhost:8000](http://localhost:8000)

Health check:

```
http://localhost:8000/api/v2/health
```

---

## 💾 Persistent Storage

The backend mounts a volume:

```
./backend/storage:/app/storage
```

This ensures:

* Annotated videos persist
* PDF reports persist
* Analysis JSON persists
* Data survives container restarts

---

## 🛑 Stopping Services

```bash
docker compose down
```

---

## 🔧 Production Notes

For production environments:

* Increase Uvicorn workers:

  ```
  --workers 4
  ```
* Add reverse proxy (Nginx gateway)
* Enable HTTPS (Certbot / Cloudflare)
* Use environment-based configs
* Add resource limits in docker-compose

---

## 🎯 Coverage Scope

The test suite validates:

* Scoring logic integrity
* Penalty weighting
* Temporal aggregation behavior
* Flagging thresholds
* API contract compliance
* Artifact generation
* Video rendering synchronization

---

# 🔮 Future Improvements

1. Replace heuristic scoring with ML-trained posture model
2. Add 3D pose reconstruction
3. Add real-time posture monitoring
4. Multi-user tracking
5. Posture history dashboard per user
6. Clinician analytics dashboard
7. Kalman filtering for smoother landmark tracking
8. Long-duration posture session analysis
9. Mobile device optimization
10. Deploy as SaaS with authentication + database persistence

---

# 🎯 Project Vision

PostureAI aims to bridge computer vision and digital health by delivering accessible posture analytics through a web-based AI platform.

---
