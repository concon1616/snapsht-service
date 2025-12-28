from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from ..models.schemas import VideoRequest, VideoResponse
from ..services.video import video_service
from ..utils.logger import logger

router = APIRouter(prefix="/api/video", tags=["video"])


@router.post("", response_model=VideoResponse)
async def create_video(request: VideoRequest):
    """Capture a scrolling video of the specified URL."""
    try:
        result = await video_service.capture_video(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Video capture failed: {e}")
        raise HTTPException(status_code=500, detail="Video capture failed")


@router.get("/{video_id}")
async def get_video(video_id: str):
    """Download a video by ID."""
    filepath = await video_service.get_video(video_id)

    if not filepath:
        raise HTTPException(status_code=404, detail="Video not found")

    # Determine media type from extension
    ext = filepath.suffix.lower()
    media_types = {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".gif": "image/gif",
    }

    return FileResponse(
        filepath,
        media_type=media_types.get(ext, "application/octet-stream"),
        filename=filepath.name,
    )


@router.delete("/{video_id}")
async def delete_video(video_id: str):
    """Delete a video by ID."""
    deleted = await video_service.delete_video(video_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found")

    return {"success": True, "message": "Video deleted"}
