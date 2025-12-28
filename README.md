# Snapsht Service

A Python/FastAPI screenshot and video capture service using Selenium (snapsht-style approach). Self-hosted alternative to screenshot APIs.

## Features

- **Screenshot Capture**: Full-page or viewport screenshots
- **Video Recording**: Smooth scrolling videos (MP4, WebM, GIF)
- **Batch Processing**: Process multiple URLs concurrently
- **React Frontend**: Web UI for easy capture
- **API Documentation**: Auto-generated Swagger docs

## Quick Start

### Backend

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
  "scroll_speed": "medium"
}
```

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
- ChromeDriver (via Homebrew: `brew install chromedriver`)
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
├── tests/
│   └── test_domains.py      # Domain testing script
├── requirements.txt
└── README.md
```

## License

MIT
