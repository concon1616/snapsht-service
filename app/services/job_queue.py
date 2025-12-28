import asyncio
import uuid
from datetime import datetime
from typing import Callable, Any
from dataclasses import dataclass, field

from ..utils.logger import logger


@dataclass
class Job:
    id: str
    url: str
    status: str = "pending"
    result: Any = None
    error: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: datetime | None = None
    completed_at: datetime | None = None


@dataclass
class Batch:
    id: str
    jobs: list[Job]
    options: dict
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)


class JobQueue:
    def __init__(self):
        self._batches: dict[str, Batch] = {}
        self._lock = asyncio.Lock()

    async def create_batch(self, urls: list[str], options: dict) -> Batch:
        """Create a new batch of jobs."""
        batch_id = str(uuid.uuid4())

        jobs = [
            Job(id=str(uuid.uuid4()), url=str(url))
            for url in urls
        ]

        batch = Batch(id=batch_id, jobs=jobs, options=options)
        self._batches[batch_id] = batch

        logger.info(f"Created batch {batch_id} with {len(jobs)} jobs")
        return batch

    async def get_batch(self, batch_id: str) -> Batch | None:
        """Get batch by ID."""
        return self._batches.get(batch_id)

    async def process_batch(
        self,
        batch_id: str,
        processor: Callable,
        max_concurrent: int = 3,
    ):
        """Process all jobs in a batch."""
        batch = self._batches.get(batch_id)
        if not batch:
            return

        batch.status = "processing"
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_job(job: Job):
            async with semaphore:
                job.status = "processing"
                job.started_at = datetime.utcnow()

                try:
                    result = await processor(job.url, batch.options)
                    job.result = result
                    job.status = "completed"
                except Exception as e:
                    job.error = str(e)
                    job.status = "failed"
                    logger.error(f"Job {job.id} failed: {e}")
                finally:
                    job.completed_at = datetime.utcnow()

        # Process all jobs concurrently (with semaphore limiting)
        await asyncio.gather(*[process_job(job) for job in batch.jobs])

        # Update batch status
        failed_count = sum(1 for j in batch.jobs if j.status == "failed")
        batch.status = "failed" if failed_count == len(batch.jobs) else "completed"

        logger.info(f"Batch {batch_id} completed: {len(batch.jobs) - failed_count}/{len(batch.jobs)} successful")

    def get_batch_status(self, batch_id: str) -> dict | None:
        """Get detailed batch status."""
        batch = self._batches.get(batch_id)
        if not batch:
            return None

        jobs = batch.jobs
        completed = sum(1 for j in jobs if j.status == "completed")
        failed = sum(1 for j in jobs if j.status == "failed")
        processing = sum(1 for j in jobs if j.status == "processing")
        pending = sum(1 for j in jobs if j.status == "pending")

        return {
            "batch_id": batch.id,
            "total_jobs": len(jobs),
            "completed": completed,
            "failed": failed,
            "processing": processing,
            "pending": pending,
            "status": batch.status,
            "progress": round((completed + failed) / len(jobs) * 100, 1) if jobs else 0,
            "jobs": [
                {
                    "id": j.id,
                    "url": j.url,
                    "status": j.status,
                    "result": j.result,
                    "error": j.error,
                }
                for j in jobs
            ],
        }

    async def cleanup_old_batches(self, max_age_hours: int = 24):
        """Remove batches older than max_age_hours."""
        now = datetime.utcnow()
        to_remove = []

        for batch_id, batch in self._batches.items():
            age = (now - batch.created_at).total_seconds() / 3600
            if age > max_age_hours and batch.status in ["completed", "failed"]:
                to_remove.append(batch_id)

        for batch_id in to_remove:
            del self._batches[batch_id]

        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} old batches")


# Global job queue instance
job_queue = JobQueue()
