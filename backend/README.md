# AI Posture Analysis Microservice

A modular FastAPI-based backend microservice that analyzes 10–15 second posture videos and generates:

- Posture score (0–100)
- Classification (Good / Fair / Poor)
- Biomechanical metrics
- Annotated skeleton overlay image
- Downloadable PDF posture report

---

## 📌 Features

- MediaPipe Pose-based landmark extraction
- Geometry-based posture metric computation
- Weighted scoring engine
- Rule-based feedback generation
- Annotated skeleton visualization
- Structured PDF report generation
- Modular, production-ready architecture
- REST API (versioned)
- Docker-ready structure

---

## 🏗 Architecture Overview

```

backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── storage/
├── tests/
├── requirements.txt
├── Dockerfile
└── README.md

````

### Processing Pipeline

1. Upload video
2. Extract frames
3. Extract pose landmarks
4. Compute posture metrics
5. Compute posture score
6. Generate feedback
7. Render annotated overlay
8. Generate PDF report
9. Return structured JSON response

---

## 📡 API Endpoints

### 1️⃣ POST `/api/v1/analyze-posture`

**Input:**  
Multipart form-data  
Field: `file` (.mp4, .mov, .avi)  
Duration: 10–15 seconds  

**Response Example:**

```json
{
  "status": "success",
  "report_id": "a8f13b92",
  "posture_score": 82,
  "classification": "Fair",
  "metrics": {
    "neck_angle": 14.2,
    "shoulder_alignment_difference": 2.8,
    "hip_alignment_difference": 3.1,
    "spine_vertical_deviation": 5.9
  },
  "feedback": [
    "Mild forward head posture detected."
  ],
  "artifacts": {
    "skeleton_image_url": "/api/v1/image/a8f13b92",
    "pdf_report_url": "/api/v1/report/a8f13b92"
  },
  "processing_time_seconds": 2.14
}
````

---

### 2️⃣ GET `/api/v1/health`

Service health check.

---

### 3️⃣ GET `/api/v1/image/{report_id}`

Returns annotated skeleton overlay image (PNG).

---

### 4️⃣ GET `/api/v1/report/{report_id}`

Returns downloadable PDF report.

---

## 🧠 Posture Metrics

The system computes:

* **Neck Angle** (relative to vertical)
* **Spine Vertical Deviation**
* **Shoulder Alignment Difference (%)**
* **Hip Alignment Difference (%)**

Metrics are aggregated using median across sampled frames.

---

## 📊 Posture Score Calculation

Weighted penalty system:

* Neck Angle → 35%
* Spine Deviation → 30%
* Shoulder Alignment → 17.5%
* Hip Alignment → 17.5%

Score = 100 − weighted penalties (clamped 0–100)

Classification:

* ≥ 85 → Good
* 65–84 → Fair
* < 65 → Poor

---

## 🚀 Setup Instructions

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Server

```bash
uvicorn app.main:app --reload
```

Access Swagger docs at:

```
http://127.0.0.1:8000/docs
```

---

## ⚠ Limitations

* 2D landmark-based posture estimation
* Single-person detection only
* Not a medical diagnosis tool
* Lighting and camera angle may affect results

---

## 🔮 Future Improvements

* 3D landmark utilization
* Temporal smoothing
* Async processing
* Cloud storage integration
* Database-backed report tracking
* Enhanced visualization (angle arcs, vertical guides)

---

## 📄 Disclaimer

This AI-powered posture analysis system is intended for general wellness screening and informational purposes only. It does not replace professional medical advice.