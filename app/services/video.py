import os
import uuid
import asyncio
import tempfile
import subprocess
import shutil
import random
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

    def _generate_realistic_scroll_pattern(self, total_scroll: int):
        """
        Generate a realistic scroll pattern mimicking human behavior.
        - Unequal scroll distances (some short, some long)
        - Varying pause durations
        - Occasional small backtracks
        - Scrolls down then back up
        Returns list of (scroll_position, is_pause) tuples.
        """
        pattern = []
        current_pos = 0

        # Generate random scroll segments going DOWN (4-7 segments)
        num_down_scrolls = random.randint(4, 7)
        remaining = total_scroll
        scroll_targets = []

        for i in range(num_down_scrolls):
            if i == num_down_scrolls - 1:
                # Last segment gets the rest
                scroll_targets.append(total_scroll)
            else:
                # Random portion of remaining distance (15-40%)
                portion = random.uniform(0.15, 0.40)
                target = current_pos + int(remaining * portion)
                scroll_targets.append(target)
                remaining = total_scroll - target
                current_pos = target

        current_pos = 0

        # Scroll DOWN with varying behaviors
        for i, target in enumerate(scroll_targets):
            scroll_distance = target - current_pos

            # Varying scroll speed (frames) - shorter scrolls are quicker
            scroll_frames = random.randint(8, 18) if scroll_distance > 200 else random.randint(5, 10)

            # Animate the scroll with easing
            for f in range(scroll_frames):
                t = f / scroll_frames
                ease = t * t * (3 - 2 * t)  # Smoothstep
                pos = current_pos + scroll_distance * ease
                pattern.append((int(pos), False))

            current_pos = target

            # Varying pause duration (longer pauses mid-page, shorter at edges)
            if i == 0:
                pause_frames = random.randint(12, 20)  # Quick first look
            elif i == len(scroll_targets) - 1:
                pause_frames = random.randint(15, 25)  # Pause at bottom
            else:
                pause_frames = random.randint(10, 30)  # Variable mid-page

            for _ in range(pause_frames):
                pattern.append((current_pos, True))

            # Occasional small backtrack (30% chance, not on first or last)
            if 0 < i < len(scroll_targets) - 1 and random.random() < 0.3:
                backtrack = random.randint(30, 80)
                back_pos = max(0, current_pos - backtrack)

                # Quick scroll up
                for f in range(6):
                    t = f / 6
                    ease = t * t * (3 - 2 * t)
                    pos = current_pos - (current_pos - back_pos) * ease
                    pattern.append((int(pos), False))

                # Brief pause
                for _ in range(random.randint(8, 15)):
                    pattern.append((back_pos, True))

                # Scroll back down
                for f in range(6):
                    t = f / 6
                    ease = t * t * (3 - 2 * t)
                    pos = back_pos + (current_pos - back_pos) * ease
                    pattern.append((int(pos), False))

        # Scroll back UP (fewer segments, more direct)
        num_up_scrolls = random.randint(3, 5)
        up_targets = []
        remaining = total_scroll

        for i in range(num_up_scrolls):
            if i == num_up_scrolls - 1:
                up_targets.append(0)
            else:
                portion = random.uniform(0.20, 0.45)
                target = current_pos - int(remaining * portion)
                up_targets.append(max(0, target))
                remaining = target
                current_pos = target

        current_pos = total_scroll

        # Scroll UP
        for i, target in enumerate(up_targets):
            scroll_distance = current_pos - target
            scroll_frames = random.randint(10, 16)

            for f in range(scroll_frames):
                t = f / scroll_frames
                ease = t * t * (3 - 2 * t)
                pos = current_pos - scroll_distance * ease
                pattern.append((int(max(0, pos)), False))

            current_pos = target

            # Shorter pauses on the way up (scanning, not reading)
            pause_frames = random.randint(8, 18)
            for _ in range(pause_frames):
                pattern.append((max(0, current_pos), True))

        return pattern

    async def capture_video(self, request: VideoRequest) -> VideoResponse:
        """Capture a scrolling video of the URL."""
        video_id = str(uuid.uuid4())
        filename = f"{video_id}.{request.format}"
        filepath = self.settings.output_dir / filename

        # Check for realistic scroll mode
        realistic_mode = getattr(request, 'realistic', False) or request.scroll_speed == "realistic"

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

                total_scroll = max(0, page_height - request.height)

                # Scroll to top
                driver.execute_script("window.scrollTo(0, 0)")
                await asyncio.sleep(0.1)

                frames_captured = 0

                if realistic_mode:
                    # Realistic human-like scrolling with varying speeds and pauses
                    logger.info(f"Using realistic scroll pattern (varying segments with backtracks)")
                    scroll_pattern = self._generate_realistic_scroll_pattern(total_scroll)

                    for scroll_pos, is_pause in scroll_pattern:
                        # Capture frame
                        screenshot = await asyncio.get_event_loop().run_in_executor(
                            None, driver.get_screenshot_as_png
                        )

                        frame_path = temp_dir / f"frame_{frames_captured:05d}.png"
                        image = Image.open(BytesIO(screenshot))

                        if image.size != (request.width, request.height):
                            image = image.crop((0, 0, request.width, request.height))

                        image.save(frame_path, "PNG")
                        frames_captured += 1

                        # Scroll to position
                        driver.execute_script(f"window.scrollTo(0, {scroll_pos})")

                        # Faster capture during scroll, slower during pause
                        delay = 0.05 if not is_pause else 0.033
                        await asyncio.sleep(delay)

                else:
                    # Original smooth scroll mode
                    scroll_per_frame = self._get_scroll_speed_pixels(request.scroll_speed, request.height)
                    frame_interval = 1000 / request.fps
                    total_frames = int((request.duration / 1000) * request.fps)

                    logger.info(f"Capturing {total_frames} frames at {request.fps} FPS")

                    current_scroll = 0

                    for frame_num in range(total_frames):
                        screenshot = await asyncio.get_event_loop().run_in_executor(
                            None, driver.get_screenshot_as_png
                        )

                        frame_path = temp_dir / f"frame_{frame_num:05d}.png"
                        image = Image.open(BytesIO(screenshot))

                        if image.size != (request.width, request.height):
                            image = image.crop((0, 0, request.width, request.height))

                        image.save(frame_path, "PNG")
                        frames_captured += 1

                        if current_scroll < total_scroll:
                            current_scroll = min(current_scroll + scroll_per_frame, total_scroll)
                            driver.execute_script(f"window.scrollTo(0, {current_scroll})")

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
