import os
import uuid
import time
import asyncio
from pathlib import Path
from datetime import datetime
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .browser_pool import browser_pool
from ..config import get_settings
from ..utils.logger import logger
from ..models.schemas import ScreenshotRequest, ScreenshotResponse


class CaptureService:
    def __init__(self):
        self.settings = get_settings()
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        self.settings.output_dir.mkdir(parents=True, exist_ok=True)

    async def capture_screenshot(self, request: ScreenshotRequest) -> ScreenshotResponse:
        """Capture a screenshot using snapsht-style approach."""
        capture_id = str(uuid.uuid4())
        filename = f"{capture_id}.{request.format}"
        filepath = self.settings.output_dir / filename

        async with browser_pool.get_driver() as driver:
            try:
                # Set viewport size
                driver.set_window_size(request.width, request.height)

                # Navigate to URL
                logger.info(f"Navigating to {request.url}")
                await asyncio.get_event_loop().run_in_executor(
                    None, driver.get, str(request.url)
                )

                # Wait for page load
                await asyncio.sleep(request.wait_for / 1000)

                # Dismiss popups if requested
                if request.dismiss_popups:
                    await self._dismiss_popups(driver)

                # Handle full page capture (snapsht approach)
                if request.full_page:
                    await self._prepare_full_page(driver)

                # Scroll to trigger lazy loading
                await self._trigger_lazy_load(driver)

                # Scroll back to top
                driver.execute_script("window.scrollTo(0, 0)")
                await asyncio.sleep(0.2)

                # Capture screenshot
                if request.selector:
                    screenshot_data = await self._capture_element(driver, request.selector)
                else:
                    screenshot_data = await asyncio.get_event_loop().run_in_executor(
                        None, driver.get_screenshot_as_png
                    )

                # Process and save image
                image = Image.open(BytesIO(screenshot_data))
                dimensions = {"width": image.width, "height": image.height}

                # Save in requested format
                await self._save_image(image, filepath, request.format, request.quality)

                file_size = filepath.stat().st_size

                logger.info(f"Screenshot saved: {filename} ({file_size} bytes)")

                return ScreenshotResponse(
                    id=capture_id,
                    filename=filename,
                    size=file_size,
                    format=request.format,
                    dimensions=dimensions,
                    full_page=request.full_page,
                    download_url=f"/api/screenshot/{capture_id}",
                    created_at=datetime.utcnow(),
                )

            except Exception as e:
                logger.error(f"Screenshot capture failed: {e}")
                raise

    async def _prepare_full_page(self, driver):
        """Resize browser to capture full page (snapsht approach)."""
        # Get full page dimensions
        total_width = driver.execute_script("return document.body.parentNode.scrollWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

        # Cap at reasonable maximum
        max_height = 15000
        total_height = min(total_height, max_height)

        # Resize window to full page size
        driver.set_window_size(total_width, total_height)

        # Hide scrollbars
        driver.execute_script(
            "document.documentElement.style.overflow = 'hidden';"
            "document.body.style.overflow = 'hidden';"
        )

        await asyncio.sleep(0.3)

    async def _trigger_lazy_load(self, driver):
        """Scroll through page to trigger lazy-loaded images."""
        scroll_script = """
            return new Promise((resolve) => {
                const scrollStep = window.innerHeight;
                const maxScroll = Math.min(document.body.scrollHeight, 15000);
                let currentScroll = 0;

                const scroll = () => {
                    if (currentScroll < maxScroll) {
                        window.scrollTo(0, currentScroll);
                        currentScroll += scrollStep;
                        setTimeout(scroll, 100);
                    } else {
                        window.scrollTo(0, 0);
                        resolve(true);
                    }
                };
                scroll();
            });
        """

        await asyncio.get_event_loop().run_in_executor(
            None, driver.execute_script, scroll_script
        )
        await asyncio.sleep(0.5)

    async def _dismiss_popups(self, driver):
        """Dismiss common popups, modals, cookie banners."""
        dismiss_script = """
            // Common popup close selectors
            const selectors = [
                '[class*="close"]', '[class*="Close"]',
                '[aria-label*="close"]', '[aria-label*="Close"]',
                '[class*="dismiss"]', '[class*="Dismiss"]',
                '[class*="cookie"] button', '[class*="Cookie"] button',
                '[id*="cookie"] button', '[id*="Cookie"] button',
                '[class*="consent"] button', '[class*="Consent"] button',
                '[class*="gdpr"] button', '[class*="GDPR"] button',
                '.modal-close', '.popup-close', '.close-button',
                '[data-dismiss="modal"]', '[data-close]',
                'button[aria-label="Close"]',
                '[class*="newsletter"] [class*="close"]',
                '[class*="popup"] [class*="close"]',
                '[class*="modal"] [class*="close"]',
            ];

            for (const selector of selectors) {
                try {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                        if (el.offsetParent !== null) {
                            el.click();
                        }
                    });
                } catch (e) {}
            }

            // Hide overlays
            const overlaySelectors = [
                '[class*="overlay"]',
                '[class*="modal-backdrop"]',
                '[class*="popup-overlay"]',
            ];

            for (const selector of overlaySelectors) {
                try {
                    document.querySelectorAll(selector).forEach(el => {
                        el.style.display = 'none';
                    });
                } catch (e) {}
            }
        """

        await asyncio.get_event_loop().run_in_executor(
            None, driver.execute_script, dismiss_script
        )
        await asyncio.sleep(0.3)

    async def _capture_element(self, driver, selector: str) -> bytes:
        """Capture a specific element."""
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element.screenshot_as_png
        except TimeoutException:
            raise ValueError(f"Element not found: {selector}")

    async def _save_image(self, image: Image.Image, filepath: Path, format: str, quality: int):
        """Save image in the requested format."""
        save_kwargs = {}

        if format == "jpeg":
            # Convert RGBA to RGB for JPEG
            if image.mode == "RGBA":
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = True

        elif format == "webp":
            save_kwargs["quality"] = quality

        elif format == "png":
            save_kwargs["optimize"] = True

        await asyncio.get_event_loop().run_in_executor(
            None, lambda: image.save(filepath, format.upper(), **save_kwargs)
        )

    async def get_screenshot(self, screenshot_id: str) -> Path | None:
        """Get screenshot file path by ID."""
        for ext in ["png", "jpeg", "webp"]:
            filepath = self.settings.output_dir / f"{screenshot_id}.{ext}"
            if filepath.exists():
                return filepath
        return None

    async def delete_screenshot(self, screenshot_id: str) -> bool:
        """Delete a screenshot."""
        filepath = await self.get_screenshot(screenshot_id)
        if filepath:
            filepath.unlink()
            return True
        return False


# Global capture service instance
capture_service = CaptureService()
