import os
import uuid
import asyncio
import tempfile
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from PIL import Image
from io import BytesIO

from .browser_pool import browser_pool
from ..config import get_settings
from ..utils.logger import logger
from ..models.schemas import VideoRequest, VideoResponse


class VideoService:
    def __init__(self):
        self.settings = get_settings()
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        self.settings.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_scroll_speed_pixels(self, speed: str, height: int) -> int:
        """Get pixels per frame based on scroll speed."""
        speeds = {
            "slow": max(2, height // 100),
            "medium": max(5, height // 50),
            "fast": max(10, height // 25),
        }
        return speeds.get(speed, speeds["medium"])

    async def capture_video(self, request: VideoRequest) -> VideoResponse:
        """Capture a scrolling video of the URL."""
        video_id = str(uuid.uuid4())
        filename = f"{video_id}.{request.format}"
        filepath = self.settings.output_dir / filename

        async with browser_pool.get_driver() as driver:
            # Create temp directory for frames
            temp_dir = Path(tempfile.mkdtemp())

            try:
                # Set viewport size
                driver.set_window_size(request.width, request.height)

                # Navigate to URL
                logger.info(f"Navigating to {request.url}")
                await asyncio.get_event_loop().run_in_executor(
                    None, driver.get, str(request.url)
                )

                # Wait for page load
                await asyncio.sleep(2)

                # Get page height
                page_height = driver.execute_script(
                    "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
                )

                # Calculate scroll parameters
                scroll_per_frame = self._get_scroll_speed_pixels(request.scroll_speed, request.height)
                total_scroll = max(0, page_height - request.height)

                # Calculate frames needed
                frame_interval = 1000 / request.fps  # ms per frame
                total_frames = int((request.duration / 1000) * request.fps)

                logger.info(f"Capturing {total_frames} frames at {request.fps} FPS")

                # Scroll to top
                driver.execute_script("window.scrollTo(0, 0)")
                await asyncio.sleep(0.1)

                # Capture frames
                current_scroll = 0
                frames_captured = 0

                for frame_num in range(total_frames):
                    # Capture frame
                    screenshot = await asyncio.get_event_loop().run_in_executor(
                        None, driver.get_screenshot_as_png
                    )

                    # Save frame
                    frame_path = temp_dir / f"frame_{frame_num:05d}.png"
                    image = Image.open(BytesIO(screenshot))

                    # Resize if needed to ensure consistent dimensions
                    if image.size != (request.width, request.height):
                        image = image.crop((0, 0, request.width, request.height))

                    image.save(frame_path, "PNG")
                    frames_captured += 1

                    # Scroll down
                    if current_scroll < total_scroll:
                        current_scroll = min(current_scroll + scroll_per_frame, total_scroll)
                        driver.execute_script(f"window.scrollTo(0, {current_scroll})")

                    # Small delay for smooth capture
                    await asyncio.sleep(frame_interval / 1000 * 0.5)

                logger.info(f"Captured {frames_captured} frames, encoding video...")

                # Encode video with FFmpeg
                await self._encode_video(
                    temp_dir,
                    filepath,
                    request.fps,
                    request.format,
                    request.width,
                    request.height,
                )

                file_size = filepath.stat().st_size
                logger.info(f"Video saved: {filename} ({file_size} bytes)")

                return VideoResponse(
                    id=video_id,
                    filename=filename,
                    size=file_size,
                    format=request.format,
                    dimensions={"width": request.width, "height": request.height},
                    duration=request.duration,
                    fps=request.fps,
                    download_url=f"/api/video/{video_id}",
                    created_at=datetime.utcnow(),
                )

            finally:
                # Cleanup temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)

    async def _encode_video(
        self,
        frames_dir: Path,
        output_path: Path,
        fps: int,
        format: str,
        width: int,
        height: int,
    ):
        """Encode frames into video using FFmpeg."""
        frame_pattern = str(frames_dir / "frame_%05d.png")

        if format == "gif":
            # Create GIF with palette for better quality
            palette_path = frames_dir / "palette.png"

            # Generate palette
            palette_cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", frame_pattern,
                "-vf", f"fps={min(fps, 15)},scale={width}:-1:flags=lanczos,palettegen",
                str(palette_path),
            ]

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: subprocess.run(palette_cmd, capture_output=True, check=True),
            )

            # Create GIF using palette
            gif_cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", frame_pattern,
                "-i", str(palette_path),
                "-lavfi", f"fps={min(fps, 15)},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
                str(output_path),
            ]

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: subprocess.run(gif_cmd, capture_output=True, check=True),
            )

        else:
            # MP4 or WebM
            codec = "libx264" if format == "mp4" else "libvpx-vp9"
            pix_fmt = "yuv420p" if format == "mp4" else "yuva420p"

            cmd = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", frame_pattern,
                "-c:v", codec,
                "-pix_fmt", pix_fmt,
                "-preset", "fast",
                "-crf", "23",
                str(output_path),
            ]

            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: subprocess.run(cmd, capture_output=True, check=True),
            )

    async def get_video(self, video_id: str) -> Path | None:
        """Get video file path by ID."""
        for ext in ["mp4", "webm", "gif"]:
            filepath = self.settings.output_dir / f"{video_id}.{ext}"
            if filepath.exists():
                return filepath
        return None

    async def delete_video(self, video_id: str) -> bool:
        """Delete a video."""
        filepath = await self.get_video(video_id)
        if filepath:
            filepath.unlink()
            return True
        return False


# Global video service instance
video_service = VideoService()
