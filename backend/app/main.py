import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.exceptions import (
    InvalidVideoFormat,
    InvalidVideoDuration,
    NoPersonDetected,
    MultiplePersonsDetected
)

# Initialize logging
configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


# ---------------------------
# Global Exception Handlers
# ---------------------------

@app.exception_handler(InvalidVideoFormat)
async def invalid_format_handler(request: Request, exc: InvalidVideoFormat):
    return JSONResponse(
        status_code=400,
        content={"status": "error", "message": str(exc)}
    )


@app.exception_handler(InvalidVideoDuration)
async def invalid_duration_handler(request: Request, exc: InvalidVideoDuration):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "message": str(exc)}
    )


@app.exception_handler(NoPersonDetected)
async def no_person_handler(request: Request, exc: NoPersonDetected):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "message": str(exc)}
    )


@app.exception_handler(MultiplePersonsDetected)
async def multiple_person_handler(request: Request, exc: MultiplePersonsDetected):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "message": str(exc)}
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running"
    }