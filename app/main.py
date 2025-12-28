from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .services.browser_pool import browser_pool
from .routes import screenshot, video, batch, health
from .utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    logger.info("Starting Snapsht Service...")
    await browser_pool.initialize()
    logger.info("Snapsht Service ready")

    yield

    # Shutdown
    logger.info("Shutting down Snapsht Service...")
    await browser_pool.shutdown()
    logger.info("Snapsht Service stopped")


settings = get_settings()

app = FastAPI(
    title="Snapsht Service",
    description="Screenshot capture service using Selenium/Chrome",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Include routers
app.include_router(health.router)
app.include_router(screenshot.router)
app.include_router(video.router)
app.include_router(batch.router)


@app.get("/")
async def root():
    """Service information."""
    return {
        "service": "Snapsht Service",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "screenshot": {
                "create": "POST /api/screenshot",
                "get": "GET /api/screenshot/{id}",
                "delete": "DELETE /api/screenshot/{id}",
            },
            "video": {
                "create": "POST /api/video",
                "get": "GET /api/video/{id}",
                "delete": "DELETE /api/video/{id}",
            },
            "batch": {
                "create": "POST /api/batch",
                "status": "GET /api/batch/{batch_id}",
            },
            "health": {
                "status": "GET /health",
                "ready": "GET /health/ready",
            },
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
