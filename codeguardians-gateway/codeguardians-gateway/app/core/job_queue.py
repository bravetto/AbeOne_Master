"""
Background Job Queue System

A Redis-based job queue system for processing background tasks asynchronously.
Provides persistent job processing that survives application restarts.
"""

import json
import uuid
import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable, Awaitable
from datetime import datetime, timedelta
from enum import Enum

import redis.asyncio as redis
from pydantic import BaseModel, Field

from app.core.centralized_redis import get_centralized_redis
from app.utils.logging import get_logger

logger = get_logger(__name__)


class JobStatus(str, Enum):
    """Job status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"
    CANCELLED = "cancelled"


class JobPriority(str, Enum):
    """Job priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class Job(BaseModel):
    """Job model for background processing."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    priority: JobPriority = JobPriority.NORMAL
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    queue_name: str = "default"


class JobQueue:
    """Redis-based job queue for background processing."""

    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis = redis_client
        self.job_handlers: Dict[str, Callable[[Job], Awaitable[None]]] = {}
        self._running = False
        self._workers: List[asyncio.Task] = []

    async def initialize(self):
        """Initialize the job queue with Redis connection."""
        if self.redis is None:
            centralized_redis = get_centralized_redis()
            await centralized_redis.initialize()
            self.redis = centralized_redis.redis_client

        if self.redis is None:
            logger.warning("Redis not available. Job queue will use in-memory fallback.")
            # Could implement in-memory fallback here if needed

    async def enqueue_job(
        self,
        name: str,
        payload: Dict[str, Any] = None,
        priority: JobPriority = JobPriority.NORMAL,
        queue_name: str = "default",
        max_retries: int = 3
    ) -> str:
        """
        Enqueue a job for background processing.

        Args:
            name: Job handler name
            payload: Job data payload
            priority: Job priority level
            queue_name: Queue to add job to
            max_retries: Maximum retry attempts

        Returns:
            Job ID
        """
        job = Job(
            name=name,
            payload=payload or {},
            priority=priority,
            queue_name=queue_name,
            max_retries=max_retries
        )

        if self.redis:
            # Store job in Redis
            job_key = f"job:{job.id}"
            queue_key = f"queue:{queue_name}:{priority.value}"

            await self.redis.set(job_key, job.model_dump_json())
            await self.redis.zadd(queue_key, {job.id: self._get_priority_score(priority)})

            logger.info(f"Job {job.id} ({name}) enqueued in {queue_name}:{priority.value}")
        else:
            logger.warning(f"Job {job.id} ({name}) queued but Redis not available")

        return job.id

    async def register_handler(self, job_name: str, handler: Callable[[Job], Awaitable[None]]):
        """
        Register a job handler function.

        Args:
            job_name: Name of the job to handle
            handler: Async function that takes a Job and processes it
        """
        self.job_handlers[job_name] = handler
        logger.info(f"Registered job handler for: {job_name}")

    async def start_workers(self, num_workers: int = 2, queues: List[str] = None):
        """
        Start background workers to process jobs.

        Args:
            num_workers: Number of worker tasks to start
            queues: List of queue names to process (default: all)
        """
        if queues is None:
            queues = ["default"]

        self._running = True

        for i in range(num_workers):
            worker = asyncio.create_task(self._worker_loop(i, queues))
            self._workers.append(worker)
            logger.info(f"Started job worker {i}")

    async def stop_workers(self):
        """Stop all background workers."""
        self._running = False

        # Cancel all worker tasks
        for worker in self._workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()

        logger.info("All job workers stopped")

    async def _worker_loop(self, worker_id: int, queues: List[str]):
        """Main worker loop that processes jobs."""
        logger.info(f"Worker {worker_id} started processing queues: {queues}")

        while self._running:
            try:
                job = await self._dequeue_job(queues)
                if job:
                    await self._process_job(job)
                else:
                    # No jobs available, wait before checking again
                    await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                await asyncio.sleep(5)  # Back off on errors

    async def _dequeue_job(self, queues: List[str]) -> Optional[Job]:
        """Dequeue the highest priority job from available queues."""
        if not self.redis:
            return None

        # Check queues in priority order
        priority_order = [JobPriority.CRITICAL, JobPriority.HIGH, JobPriority.NORMAL, JobPriority.LOW]

        for priority in priority_order:
            for queue_name in queues:
                queue_key = f"queue:{queue_name}:{priority.value}"

                # Get the job with highest score (lowest score = highest priority)
                result = await self.redis.zpopmin(queue_key, 1)

                if result:
                    job_id = result[0][0]
                    job_data = await self.redis.get(f"job:{job_id}")

                    if job_data:
                        job_dict = json.loads(job_data)
                        job = Job(**job_dict)

                        # Mark job as running
                        job.status = JobStatus.RUNNING
                        job.started_at = datetime.utcnow()
                        await self.redis.set(f"job:{job.id}", job.model_dump_json())

                        logger.info(f"Dequeued job {job.id} ({job.name})")
                        return job

        return None

    async def _process_job(self, job: Job):
        """Process a single job."""
        try:
            # Find handler
            handler = self.job_handlers.get(job.name)
            if not handler:
                raise ValueError(f"No handler registered for job: {job.name}")

            # Execute job
            logger.info(f"Processing job {job.id} ({job.name})")
            await handler(job)

            # Mark as completed
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()

            logger.info(f"Job {job.id} completed successfully")

        except Exception as e:
            logger.error(f"Job {job.id} failed: {e}")

            job.retry_count += 1
            job.error_message = str(e)

            if job.retry_count < job.max_retries:
                # Re-queue for retry
                job.status = JobStatus.RETRY
                await self._requeue_job(job)
                logger.info(f"Job {job.id} re-queued for retry ({job.retry_count}/{job.max_retries})")
            else:
                # Mark as failed
                job.status = JobStatus.FAILED
                logger.error(f"Job {job.id} failed permanently after {job.max_retries} retries")

        # Update job status in Redis
        if self.redis:
            await self.redis.set(f"job:{job.id}", job.model_dump_json())

    async def _requeue_job(self, job: Job):
        """Re-queue a job for retry."""
        if not self.redis:
            return

        # Add delay for retry (exponential backoff)
        delay_seconds = 2 ** job.retry_count
        retry_at = datetime.utcnow() + timedelta(seconds=delay_seconds)

        queue_key = f"queue:{job.queue_name}:{job.priority.value}"
        await self.redis.zadd(queue_key, {job.id: retry_at.timestamp()})

    def _get_priority_score(self, priority: JobPriority) -> float:
        """Get priority score for Redis sorted set."""
        priority_scores = {
            JobPriority.CRITICAL: 0,
            JobPriority.HIGH: 1,
            JobPriority.NORMAL: 2,
            JobPriority.LOW: 3
        }
        return priority_scores.get(priority, 2)

    async def get_job_status(self, job_id: str) -> Optional[Job]:
        """Get the status of a job."""
        if not self.redis:
            return None

        job_data = await self.redis.get(f"job:{job_id}")
        if job_data:
            job_dict = json.loads(job_data)
            return Job(**job_dict)
        return None

    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending job."""
        if not self.redis:
            return False

        job_data = await self.redis.get(f"job:{job_id}")
        if job_data:
            job_dict = json.loads(job_data)
            job = Job(**job_dict)

            if job.status == JobStatus.PENDING:
                job.status = JobStatus.CANCELLED
                await self.redis.set(f"job:{job_id}", job.model_dump_json())

                # Remove from queue
                queue_key = f"queue:{job.queue_name}:{job.priority.value}"
                await self.redis.zrem(queue_key, job_id)

                logger.info(f"Job {job_id} cancelled")
                return True

        return False


# Global job queue instance
_job_queue: Optional[JobQueue] = None


def get_job_queue() -> JobQueue:
    """Get the global job queue instance."""
    global _job_queue
    if _job_queue is None:
        _job_queue = JobQueue()
    return _job_queue


async def initialize_job_queue():
    """Initialize the global job queue."""
    queue = get_job_queue()
    await queue.initialize()
    return queue


async def enqueue_background_job(
    name: str,
    payload: Dict[str, Any] = None,
    priority: JobPriority = JobPriority.NORMAL
) -> str:
    """
    Convenience function to enqueue a background job.

    Args:
        name: Job handler name
        payload: Job data payload
        priority: Job priority level

    Returns:
        Job ID
    """
    queue = get_job_queue()
    return await queue.enqueue_job(name, payload, priority)


def register_job_handler(job_name: str, handler: Callable[[Job], Awaitable[None]]):
    """
    Convenience function to register a job handler.

    Args:
        job_name: Name of the job to handle
        handler: Async function that takes a Job and processes it
    """
    queue = get_job_queue()
    asyncio.create_task(queue.register_handler(job_name, handler))

