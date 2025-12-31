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
from .popup_blocker import (
    ALL_POPUP_SELECTORS,
    generate_hiding_css,
    get_enhanced_popup_dismiss_script,
)
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

        async with browser_pool.get_driver(block_popups=request.dismiss_popups) as driver:
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
        """
        Aggressively dismiss popups, modals, cookie banners, and ESP signup forms.

        Uses comprehensive selectors for:
        - ESP popups: Klaviyo, Mailchimp, Omnisend, Sendlane, Privy, Justuno, OptinMonster, etc.
        - E-commerce modals: Square, Shopify, BigCommerce, WooCommerce
        - Cookie/consent banners
        - Chat widgets
        - Newsletter signup forms
        - Generic modal/popup patterns
        """
        # First, inject CSS to immediately hide known popup selectors
        hiding_css = generate_hiding_css(ALL_POPUP_SELECTORS)
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                driver.execute_script,
                f"""
                var style = document.createElement('style');
                style.textContent = `{hiding_css}`;
                document.head.appendChild(style);
                """
            )
        except Exception as e:
            logger.warning(f"Failed to inject hiding CSS: {e}")

        # Then run the comprehensive dismiss script
        dismiss_script = get_enhanced_popup_dismiss_script()
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, driver.execute_script, dismiss_script
            )
        except Exception as e:
            logger.warning(f"Failed to run dismiss script: {e}")

        # Wait for any animations to complete
        await asyncio.sleep(0.5)

        # Run a second pass to catch any delayed popups
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, driver.execute_script, dismiss_script
            )
        except Exception as e:
            logger.warning(f"Second dismiss pass failed: {e}")

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
