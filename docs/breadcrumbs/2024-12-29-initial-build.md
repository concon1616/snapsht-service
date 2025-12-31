# Snapsht Service - Initial Build Session

**Date**: December 28-29, 2024
**Session**: Initial build, realistic scrolling, production deployment

---

## Summary

Built a complete screenshot/video capture service from scratch using Selenium (inspired by the `snapsht` Python tool). Deployed to production on monk.godigitalpigeon.com.

---

## What Was Built

### Core Service
- FastAPI backend with async Selenium browser pool
- Screenshot capture (full-page, viewport, element selection)
- Video capture with smooth scrolling
- Batch processing for multiple URLs
- React + Vite + Tailwind frontend

### Realistic Scrolling Feature
Implemented human-like scroll behavior for video captures:
- Unequal scroll distances (random 15-40% portions)
- Variable pause durations (longer mid-page, shorter at edges)
- Occasional small backtracks (30% chance)
- Scroll down then back up
- Adaptive segment count based on page height

### Scroll Control Parameters
Added fine-grained control:
- `scroll_depth`: 0.1-1.0 (percentage of page to scroll)
- `max_scroll_px`: Hard pixel limit
- `pause_multiplier`: 0.5-3.0 (slow down pauses)

---

## Key Decisions

### Why Direct Port Hosting (not cPanel)?
Running uvicorn directly on port 8001 as a systemd service:
- No proxy overhead for API services
- Simpler for Python async apps
- Direct WebSocket support if needed
- systemd handles restart/logging

Trade-off: No SSL by default (would need nginx reverse proxy for HTTPS)

### ChromeDriver Path Handling
Updated to check multiple paths for cross-platform support:
```python
chromedriver_paths = [
    "/opt/homebrew/bin/chromedriver",  # macOS Homebrew
    "/usr/local/bin/chromedriver",      # Linux system
    "/usr/bin/chromedriver",            # Linux alt
]
```

---

## Production Deployment

### Server: monk.godigitalpigeon.com

**Location**: `/opt/snapsht-service`
**Port**: 8001
**Service**: systemd (`snapsht.service`)

### Systemd Service File
```ini
[Unit]
Description=Snapsht Screenshot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/snapsht-service
ExecStart=/opt/snapsht-service/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=3
Environment=DISPLAY=:99

[Install]
WantedBy=multi-user.target
```

### Update Process
```bash
ssh root@monk.godigitalpigeon.com
cd /opt/snapsht-service
git pull
systemctl restart snapsht
```

---

## Tested Sites

Successfully captured with realistic scrolling:
- radiococottes.com
- bubblybarsoaps.com
- nike.com
- target.com
- bulletproofbodyguard.com
- myselfdefensetraining.com
- beacn.com
- odinparker.com
- thirdlove.com
- fashionnova.com

**Failed**: apartments.com (Cloudflare bot protection)

---

## Capture Times (on monk)

Typical video capture: 50 seconds - 2 minutes depending on page complexity

---

## Example API Calls

### Basic Realistic Video
```bash
curl -X POST http://monk.godigitalpigeon.com:8001/api/video \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "scroll_speed": "realistic"}'
```

### Limited Scroll with Slower Pauses
```bash
curl -X POST http://monk.godigitalpigeon.com:8001/api/video \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://example.com",
    "scroll_speed": "realistic",
    "scroll_depth": 0.5,
    "pause_multiplier": 1.5
  }'
```

### Download Video
```bash
curl "http://monk.godigitalpigeon.com:8001/api/video/{video_id}" -o output.mp4
```

---

## Git History

```
c748a30 Add scroll depth/speed controls for video capture
3f1ec05 Support multiple chromedriver paths for cross-platform
7e48198 Improve realistic scroll to mimic human behavior
163241b Add scroll back up to realistic video mode
55efdeb Add realistic scroll mode for videos
db378e1 Initial commit - Snapsht Service v1.0.0
```

---

## Files Modified This Session

- `app/services/video.py` - Realistic scroll pattern generation
- `app/models/schemas.py` - Added scroll_depth, max_scroll_px, pause_multiplier
- `app/services/browser_pool.py` - Cross-platform chromedriver paths
- `README.md` - Updated documentation

---

## Future Ideas

- Add SSL via nginx reverse proxy
- Webhook notifications on capture complete
- S3/cloud storage for outputs
- Rate limiting
- API key authentication
