# Snapsht Service

A Python/FastAPI screenshot and video capture service using Selenium (snapsht-style approach). Self-hosted alternative to screenshot APIs.

## Features

- **Screenshot Capture**: Full-page or viewport screenshots
- **Video Recording**: Smooth scrolling videos (MP4, WebM, GIF)
- **Realistic Scrolling**: Human-like scroll patterns with variable speeds, pauses, and backtracks
- **Batch Processing**: Process multiple URLs concurrently
- **React Frontend**: Web UI for easy capture
- **API Documentation**: Auto-generated Swagger docs

## Deployment

### Production (monk.godigitalpigeon.com)

Running as a systemd service on port 8001:

```bash
# Service management
systemctl status snapsht
systemctl restart snapsht
journalctl -u snapsht -f  # View logs

# Update deployment
cd /opt/snapsht-service
git pull
systemctl restart snapsht
```

**API URL**: `http://monk.godigitalpigeon.com:8001`

### Local Development

```bash
cd ~/Projects/snapsht-service

# Create virtual environment (first time)
python3.12 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd client
npm install
npm run dev
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/screenshot` | POST | Capture screenshot |
| `/api/screenshot/{id}` | GET | Download screenshot |
| `/api/video` | POST | Capture scrolling video |
| `/api/video/{id}` | GET | Download video |
| `/api/batch` | POST | Start batch job |
| `/api/batch/{id}` | GET | Get batch status |
| `/health` | GET | Service health |
| `/docs` | GET | Swagger API docs |

## Screenshot Request

```json
{
  "url": "https://example.com",
  "width": 1280,
  "height": 720,
  "full_page": true,
  "format": "png",
  "quality": 80,
  "wait_for": 2000,
  "dismiss_popups": true
}
```

## Video Request

```json
{
  "url": "https://example.com",
  "width": 1280,
  "height": 720,
  "duration": 5000,
  "fps": 24,
  "format": "mp4",
  "scroll_speed": "realistic",
  "scroll_depth": 0.5,
  "max_scroll_px": 2000,
  "pause_multiplier": 1.5
}
```

### Video Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | URL to capture |
| `width` | int | 1280 | Viewport width (100-1920) |
| `height` | int | 720 | Viewport height (100-1080) |
| `duration` | int | 5000 | Max duration in ms (1000-30000) |
| `fps` | int | 24 | Frames per second (10-60) |
| `format` | string | "mp4" | Output format: mp4, webm, gif |
| `scroll_speed` | string | "medium" | slow, medium, fast, **realistic** |
| `scroll_depth` | float | 1.0 | How much of page to scroll (0.1-1.0) |
| `max_scroll_px` | int | null | Hard pixel limit (overrides depth) |
| `pause_multiplier` | float | 1.0 | Pause duration multiplier (0.5-3.0) |

### Realistic Scroll Mode

When `scroll_speed: "realistic"`, the video mimics human browsing behavior:

- **Unequal scroll distances**: Some short, some long (not uniform segments)
- **Variable pause durations**: Longer mid-page, shorter at edges
- **Occasional backtracks**: 30% chance to scroll back up briefly mid-page
- **Scroll down then up**: Scrolls to bottom, then back to top
- **Adaptive segments**: Fewer segments for shorter pages

## Batch Request

```json
{
  "urls": [
    "https://example.com",
    "https://google.com"
  ],
  "options": {
    "full_page": true
  }
}
```

## Configuration

Environment variables (`.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 8000 | Server port |
| `MAX_CONCURRENT` | 3 | Browser pool size |
| `BROWSER_HEADLESS` | true | Headless Chrome |

## Requirements

- Python 3.12+
- Chrome/Chromium browser
- ChromeDriver (macOS: `brew install chromedriver`, Linux: `/usr/local/bin/chromedriver`)
- FFmpeg (for video encoding)
- Node.js 18+ (for frontend)

## Project Structure

```
snapsht-service/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration
│   ├── routes/
│   │   ├── screenshot.py    # Screenshot endpoints
│   │   ├── video.py         # Video endpoints
│   │   ├── batch.py         # Batch endpoints
│   │   └── health.py        # Health checks
│   ├── services/
│   │   ├── browser_pool.py  # Selenium driver pool
│   │   ├── capture.py       # Screenshot capture
│   │   ├── video.py         # Video recording
│   │   └── job_queue.py     # Batch job management
│   └── models/
│       └── schemas.py       # Pydantic models
├── client/                  # React frontend
├── docs/
│   └── breadcrumbs/         # Development session notes
├── tests/
│   └── test_domains.py      # Domain testing script
├── requirements.txt
└── README.md
```

## License

MIT
