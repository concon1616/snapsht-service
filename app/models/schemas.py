from pydantic import BaseModel, HttpUrl, Field
from typing import Literal
from datetime import datetime


class ScreenshotRequest(BaseModel):
    url: HttpUrl
    width: int = Field(default=1280, ge=100, le=3840)
    height: int = Field(default=720, ge=100, le=2160)
    full_page: bool = False
    format: Literal["png", "jpeg", "webp"] = "png"
    quality: int = Field(default=80, ge=1, le=100)
    wait_for: int = Field(default=1000, ge=0, le=30000)  # ms
    selector: str | None = None
    dismiss_popups: bool = True


class ScreenshotResponse(BaseModel):
    id: str
    filename: str
    size: int
    format: str
    dimensions: dict
    full_page: bool
    download_url: str
    created_at: datetime


class VideoRequest(BaseModel):
    url: HttpUrl
    width: int = Field(default=1280, ge=100, le=1920)
    height: int = Field(default=720, ge=100, le=1080)
    duration: int = Field(default=5000, ge=1000, le=30000)  # ms
    fps: int = Field(default=24, ge=10, le=60)
    format: Literal["mp4", "webm", "gif"] = "mp4"
    scroll_speed: Literal["slow", "medium", "fast", "realistic"] = "medium"
    scroll_depth: float = Field(default=1.0, ge=0.1, le=1.0)  # How much of page to scroll (0.1-1.0)
    max_scroll_px: int | None = Field(default=None, ge=100)  # Max pixels to scroll (overrides depth)
    pause_multiplier: float = Field(default=1.0, ge=0.5, le=3.0)  # Slow down pauses (1.0 = normal)
    dismiss_popups: bool = True  # Block popup/ESP domains and dismiss popups


class VideoResponse(BaseModel):
    id: str
    filename: str
    size: int
    format: str
    dimensions: dict
    duration: int
    fps: int
    download_url: str
    created_at: datetime


class BatchRequest(BaseModel):
    urls: list[HttpUrl] = Field(..., min_length=1, max_length=100)
    options: ScreenshotRequest | None = None


class JobStatus(BaseModel):
    id: str
    url: str
    status: Literal["pending", "processing", "completed", "failed"]
    result: ScreenshotResponse | None = None
    error: str | None = None


class BatchResponse(BaseModel):
    batch_id: str
    total_jobs: int
    completed: int
    failed: int
    processing: int
    pending: int
    status: Literal["pending", "processing", "completed", "failed"]
    progress: float
    jobs: list[JobStatus]


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    uptime: float
    browser: dict
