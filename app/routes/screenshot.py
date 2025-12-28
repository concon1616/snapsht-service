from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..models.schemas import ScreenshotRequest, ScreenshotResponse
from ..services.capture import capture_service
from ..utils.logger import logger

router = APIRouter(prefix="/api/screenshot", tags=["screenshot"])


@router.post("", response_model=ScreenshotResponse)
async def create_screenshot(request: ScreenshotRequest):
    """Capture a screenshot of the specified URL."""
    try:
        result = await capture_service.capture_screenshot(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        raise HTTPException(status_code=500, detail="Screenshot capture failed")


@router.get("/{screenshot_id}")
async def get_screenshot(screenshot_id: str):
    """Download a screenshot by ID."""
    filepath = await capture_service.get_screenshot(screenshot_id)

    if not filepath:
        raise HTTPException(status_code=404, detail="Screenshot not found")

    # Determine media type from extension
    ext = filepath.suffix.lower()
    media_types = {
        ".png": "image/png",
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".webp": "image/webp",
    }

    return FileResponse(
        filepath,
        media_type=media_types.get(ext, "application/octet-stream"),
        filename=filepath.name,
    )


@router.delete("/{screenshot_id}")
async def delete_screenshot(screenshot_id: str):
    """Delete a screenshot by ID."""
    deleted = await capture_service.delete_screenshot(screenshot_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Screenshot not found")

    return {"success": True, "message": "Screenshot deleted"}
