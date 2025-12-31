import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from ..utils.logger import logger
from ..config import get_settings

# Domains to block at network level (prevents popup scripts from loading)
BLOCKED_POPUP_DOMAINS = [
    # ESPs - Email Service Providers
    "*klaviyo.com*",
    "*static.klaviyo.com*",
    "*a.klaviyo.com*",
    "*chimpstatic.com*",
    "*list-manage.com*",
    "*mailchimp.com*",
    "*omnisend.com*",
    "*omnisrc.com*",
    "*privy.com*",
    "*privymktg.com*",
    "*cdn.attn.tv*",
    "*attn.tv*",
    "*sendlane.com*",
    "*activehosted.com*",
    "*activecampaign.com*",
    "*hsforms.com*",
    "*hs-scripts.com*",
    "*getresponse.com*",
    "*convertkit.com*",
    "*ck.page*",
    "*getdrip.com*",
    "*drip.com*",
    "*aweber.com*",
    "*constantcontact.com*",
    "*ctctcdn.com*",
    "*brevo.com*",
    "*sendinblue.com*",
    "*mailerlite.com*",
    "*moosend.com*",

    # Popup Tools
    "*optinmonster.com*",
    "*optmstr.com*",
    "*api.opmnstr.com*",
    "*justuno.com*",
    "*cdn.justuno.com*",
    "*sumo.com*",
    "*sumome.com*",
    "*load.sumo.com*",
    "*optimonk.com*",
    "*wisepops.com*",
    "*poptin.com*",
    "*sleeknote.com*",
    "*hellobar.com*",
    "*picreel.com*",
    "*plerdy.com*",
    "*claspo.io*",

    # Spin Wheel / Gamification
    "*wheelio.com*",
    "*wheelpop.com*",
    "*spinwheel.io*",

    # Social Proof / FOMO
    "*provesrc.com*",
    "*useproof.com*",
    "*fomo.com*",
    "*nudgify.com*",
    "*trustpulse.com*",

    # Chat Widgets (optional - can be toggled)
    # "*intercom.com*",
    # "*drift.com*",
    # "*crisp.chat*",
    # "*zendesk.com*",
    # "*tawk.to*",
]


class BrowserPool:
    def __init__(self):
        self.settings = get_settings()
        self._drivers: list[webdriver.Chrome] = []
        self._available: asyncio.Queue[webdriver.Chrome] = asyncio.Queue()
        self._lock = asyncio.Lock()
        self._initialized = False
        self._active_count = 0

    def _create_chrome_options(self) -> Options:
        """Create Chrome options matching snapsht configuration."""
        options = Options()

        if self.settings.browser_headless:
            options.add_argument("--headless=new")

        # Core options from snapsht
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")

        # Additional stability options
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--mute-audio")
        options.add_argument("--no-first-run")
        options.add_argument("--safebrowsing-disable-auto-update")

        # Hide automation indicators
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Set window size
        options.add_argument(
            f"--window-size={self.settings.default_width},{self.settings.default_height}"
        )

        return options

    def _create_driver(self) -> webdriver.Chrome:
        """Create a new Chrome WebDriver instance."""
        options = self._create_chrome_options()

        # Try known chromedriver paths, fallback to webdriver-manager
        import os
        chromedriver_paths = [
            "/opt/homebrew/bin/chromedriver",  # macOS Homebrew
            "/usr/local/bin/chromedriver",      # Linux system
            "/usr/bin/chromedriver",            # Linux alt
        ]

        service = None
        for path in chromedriver_paths:
            if os.path.exists(path):
                service = Service(path)
                break

        if service is None:
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)

        # Hide webdriver property
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """
            },
        )

        return driver

    async def initialize(self):
        """Initialize the browser pool with configured number of drivers."""
        if self._initialized:
            return

        async with self._lock:
            if self._initialized:
                return

            logger.info(f"Initializing browser pool with {self.settings.max_concurrent} drivers")

            for i in range(self.settings.max_concurrent):
                try:
                    # Create driver synchronously with delay to avoid race conditions
                    driver = self._create_driver()
                    self._drivers.append(driver)
                    await self._available.put(driver)
                    logger.info(f"Created browser instance {i + 1}/{self.settings.max_concurrent}")
                    # Small delay between driver creations to avoid port conflicts
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"Failed to create browser instance: {e}")

            self._initialized = True
            logger.info("Browser pool initialized")

    async def shutdown(self):
        """Shutdown all browser instances."""
        logger.info("Shutting down browser pool")

        for driver in self._drivers:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")

        self._drivers.clear()
        self._initialized = False

    def _enable_network_blocking(self, driver: webdriver.Chrome, block_popups: bool = True):
        """Enable network-level blocking of popup/ESP domains."""
        if not block_popups:
            # Clear any existing blocks
            try:
                driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': []})
            except Exception:
                pass
            return

        try:
            # Enable network domain
            driver.execute_cdp_cmd('Network.enable', {})

            # Block popup domains at network level
            driver.execute_cdp_cmd('Network.setBlockedURLs', {
                'urls': BLOCKED_POPUP_DOMAINS
            })

            logger.debug(f"Network blocking enabled for {len(BLOCKED_POPUP_DOMAINS)} domains")
        except Exception as e:
            logger.warning(f"Failed to enable network blocking: {e}")

    @asynccontextmanager
    async def get_driver(self, block_popups: bool = True) -> AsyncGenerator[webdriver.Chrome, None]:
        """Get a driver from the pool.

        Args:
            block_popups: If True, blocks popup/ESP domains at network level
        """
        if not self._initialized:
            await self.initialize()

        driver = await self._available.get()
        self._active_count += 1

        try:
            # Enable network blocking for popup domains
            self._enable_network_blocking(driver, block_popups)
            yield driver
        finally:
            self._active_count -= 1
            # Reset driver state
            try:
                driver.delete_all_cookies()
                # Clear network blocks
                driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': []})
            except Exception:
                pass
            await self._available.put(driver)

    @property
    def status(self) -> dict:
        """Get pool status."""
        return {
            "initialized": self._initialized,
            "total_drivers": len(self._drivers),
            "active_drivers": self._active_count,
            "available_drivers": self._available.qsize() if self._initialized else 0,
        }


# Global browser pool instance
browser_pool = BrowserPool()
