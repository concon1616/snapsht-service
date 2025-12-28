"""
Test script that:
1. Pulls .com domains from MySQL companies table
2. Checks which ones are online (HEAD request)
3. Takes screenshots of responsive domains
"""

import asyncio
import httpx
import mysql.connector
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.capture import capture_service
from app.services.browser_pool import browser_pool
from app.models.schemas import ScreenshotRequest


async def get_domains_from_mysql(limit: int = 20) -> list[str]:
    """Fetch .com domains from MySQL companies table."""
    print(f"\n[1/3] Fetching domains from MySQL...")

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="g#NFC1s%",
            database="Companies"
        )
        cursor = conn.cursor()

        query = """
            SELECT DISTINCT domain
            FROM Storeleads
            WHERE domain LIKE '%.com'
            AND domain IS NOT NULL
            AND domain != ''
            ORDER BY RAND()
            LIMIT %s
        """

        cursor.execute(query, (limit,))
        domains = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        print(f"   Found {len(domains)} .com domains")
        return domains

    except Exception as e:
        print(f"   Error: {e}")
        return []


async def check_uptime(domains: list[str], timeout: float = 5.0) -> list[str]:
    """Check which domains are online using HEAD requests."""
    print(f"\n[2/3] Checking uptime for {len(domains)} domains...")

    online_domains = []

    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        for i, domain in enumerate(domains, 1):
            url = f"https://{domain}" if not domain.startswith("http") else domain

            try:
                response = await client.head(url)
                if response.status_code < 400:
                    online_domains.append(url)
                    print(f"   [{i}/{len(domains)}] {domain}: {response.status_code}")
                else:
                    print(f"   [{i}/{len(domains)}] {domain}: {response.status_code} (skipped)")
            except Exception as e:
                # Try HTTP if HTTPS fails
                try:
                    http_url = f"http://{domain}"
                    response = await client.head(http_url)
                    if response.status_code < 400:
                        online_domains.append(http_url)
                        print(f"   [{i}/{len(domains)}] {domain}: {response.status_code} (HTTP)")
                    else:
                        print(f"   [{i}/{len(domains)}] {domain}: offline")
                except:
                    print(f"   [{i}/{len(domains)}] {domain}: offline")

    print(f"   {len(online_domains)} domains online")
    return online_domains


async def capture_screenshots(urls: list[str], max_captures: int = 5):
    """Capture screenshots of the URLs."""
    print(f"\n[3/3] Capturing screenshots (max {max_captures})...")

    # Initialize browser pool
    await browser_pool.initialize()

    results = {"success": [], "failed": []}

    for i, url in enumerate(urls[:max_captures], 1):
        print(f"\n   [{i}/{min(len(urls), max_captures)}] {url}")

        try:
            request = ScreenshotRequest(
                url=url,
                width=1280,
                height=720,
                full_page=True,
                format="png",
                wait_for=2000,
                dismiss_popups=True,
            )

            start = datetime.now()
            result = await capture_service.capture_screenshot(request)
            elapsed = (datetime.now() - start).total_seconds()

            print(f"       Saved: {result.filename}")
            print(f"       Size: {result.size:,} bytes")
            print(f"       Dimensions: {result.dimensions['width']}x{result.dimensions['height']}")
            print(f"       Time: {elapsed:.1f}s")

            results["success"].append({
                "url": url,
                "file": result.filename,
                "size": result.size,
                "time": elapsed,
            })

        except Exception as e:
            print(f"       Failed: {e}")
            results["failed"].append({"url": url, "error": str(e)})

    # Shutdown browser pool
    await browser_pool.shutdown()

    return results


async def main():
    print("=" * 60)
    print("Snapsht Service - Domain Test")
    print("=" * 60)

    # 1. Get domains from MySQL
    domains = await get_domains_from_mysql(limit=20)

    if not domains:
        print("\nNo domains found. Exiting.")
        return

    # 2. Check uptime
    online = await check_uptime(domains)

    if not online:
        print("\nNo online domains found. Exiting.")
        return

    # 3. Capture screenshots
    results = await capture_screenshots(online, max_captures=5)

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Domains checked: {len(domains)}")
    print(f"Online: {len(online)}")
    print(f"Screenshots captured: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")

    if results["success"]:
        print(f"\nScreenshots saved to: /tmp/snapsht-screenshots/")
        for r in results["success"]:
            print(f"  - {r['file']}")


if __name__ == "__main__":
    asyncio.run(main())
