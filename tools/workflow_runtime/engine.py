from __future__ import annotations

from dataclasses import replace
from threading import Lock
from typing import Any, Callable
from uuid import uuid4

from .models import Event, Job, JobResult, JobState
from .queue import InMemoryQueue


class WorkflowEngine:
    """Owns lifecycle transitions; runners never mutate lifecycle state directly."""

    def __init__(self, queue: InMemoryQueue) -> None:
        self.queue = queue
        self._states: dict[str, JobState] = {}
        self._results: dict[str, JobResult] = {}
        self._handlers: dict[str, Callable[[dict[str, Any]], Any]] = {}
        self._lock = Lock()

    def register_handler(self, task_type: str, handler: Callable[[dict[str, Any]], Any]) -> None:
        self._handlers[task_type] = handler

    def submit(self, job: Job) -> Event:
        with self._lock:
            if job.job_id in self._states:
                raise ValueError(f"job already exists: {job.job_id}")
            self._states[job.job_id] = JobState.QUEUED
        self.queue.publish(job)
        return self._event("job.queued", job)

    def handler_for(self, task_type: str) -> Callable[[dict[str, Any]], Any]:
        try:
            return self._handlers[task_type]
        except KeyError as exc:
            raise KeyError(f"no handler registered for task_type={task_type}") from exc

    def mark_running(self, job: Job) -> Event:
        with self._lock:
            self._transition(job.job_id, JobState.RUNNING, {JobState.QUEUED, JobState.RETRY_WAIT})
        return self._event("job.running", job)

    def complete(self, job: Job, output: Any) -> Event:
        result = JobResult(job.job_id, JobState.SUCCEEDED, job.attempt, output=output)
        with self._lock:
            self._states[job.job_id] = JobState.SUCCEEDED
            self._results[job.job_id] = result
        return self._event("job.succeeded", job, {"output": output})

    def fail(self, job: Job, error: Exception) -> Event:
        next_attempt = job.attempt + 1
        retry = next_attempt < job.max_attempts
        state = JobState.RETRY_WAIT if retry else JobState.FAILED
        with self._lock:
            self._states[job.job_id] = state
            self._results[job.job_id] = JobResult(job.job_id, state, next_attempt, error=str(error))
        if retry:
            self.queue.publish(replace(job, attempt=next_attempt))
            return self._event("job.retry_scheduled", job, {"error": str(error), "next_attempt": next_attempt})
        return self._event("job.failed", job, {"error": str(error), "attempt": next_attempt})

    def state(self, job_id: str) -> JobState | None:
        with self._lock:
            return self._states.get(job_id)

    def result(self, job_id: str) -> JobResult | None:
        with self._lock:
            return self._results.get(job_id)

    def _transition(self, job_id: str, target: JobState, allowed: set[JobState]) -> None:
        current = self._states.get(job_id)
        if current not in allowed:
            raise ValueError(f"invalid transition {current} -> {target} for {job_id}")
        self._states[job_id] = target

    @staticmethod
    def _event(event_type: str, job: Job, payload: dict[str, Any] | None = None) -> Event:
        return Event(str(uuid4()), event_type, job.job_id, job.workflow_id, job.attempt, payload or {})
