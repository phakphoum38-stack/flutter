from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Any, Callable

from .engine import WorkflowEngine
from .models import Job, JobResult


class StatelessRunner:
    """Executes one queue item and keeps no durable workflow state locally."""

    def __init__(self, engine: WorkflowEngine) -> None:
        self.engine = engine

    def run_once(self) -> JobResult | None:
        job = self.engine.queue.consume()
        if job is None:
            return None
        self.engine.mark_running(job)
        handler = self.engine.handler_for(job.task_type)
        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(handler, dict(job.payload))
                output = future.result(timeout=job.timeout_seconds)
        except (Exception, FutureTimeoutError) as exc:
            self.engine.fail(job, exc)
            result = self.engine.result(job.job_id)
            assert result is not None
            return result
        self.engine.complete(job, output)
        result = self.engine.result(job.job_id)
        assert result is not None
        return result

    def drain(self, max_jobs: int | None = None) -> list[JobResult]:
        results: list[JobResult] = []
        while max_jobs is None or len(results) < max_jobs:
            result = self.run_once()
            if result is None:
                break
            results.append(result)
        return results
