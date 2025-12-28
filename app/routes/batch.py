import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks

from ..models.schemas import BatchRequest, ScreenshotRequest
from ..services.job_queue import job_queue
from ..services.capture import capture_service
from ..utils.logger import logger

router = APIRouter(prefix="/api/batch", tags=["batch"])


async def process_url(url: str, options: dict):
    """Process a single URL from batch."""
    request = ScreenshotRequest(
        url=url,
        width=options.get("width", 1280),
        height=options.get("height", 720),
        full_page=options.get("full_page", True),
        format=options.get("format", "png"),
        quality=options.get("quality", 80),
        wait_for=options.get("wait_for", 2000),
        dismiss_popups=options.get("dismiss_popups", True),
    )

    result = await capture_service.capture_screenshot(request)

    return {
        "id": result.id,
        "filename": result.filename,
        "download_url": result.download_url,
        "size": result.size,
        "dimensions": result.dimensions,
    }


@router.post("")
async def create_batch(request: BatchRequest, background_tasks: BackgroundTasks):
    """Create and start processing a batch of screenshots."""
    urls = [str(url) for url in request.urls]
    options = request.options.model_dump() if request.options else {}

    # Create batch
    batch = await job_queue.create_batch(urls, options)

    # Process in background
    background_tasks.add_task(
        job_queue.process_batch,
        batch.id,
        process_url,
        max_concurrent=3,
    )

    return {
        "success": True,
        "batch_id": batch.id,
        "total_jobs": len(batch.jobs),
        "status_url": f"/api/batch/{batch.id}",
        "message": f"Batch submitted. {len(batch.jobs)} jobs queued for processing.",
    }


@router.get("/{batch_id}")
async def get_batch_status(batch_id: str):
    """Get batch status and job results."""
    status = job_queue.get_batch_status(batch_id)

    if not status:
        raise HTTPException(status_code=404, detail="Batch not found")

    return {"success": True, "batch": status}
