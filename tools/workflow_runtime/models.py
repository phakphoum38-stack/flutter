from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class JobState(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    RETRY_WAIT = "RETRY_WAIT"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class Job:
    job_id: str
    workflow_id: str
    task_type: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    attempt: int = 0
    max_attempts: int = 3
    timeout_seconds: float = 300.0
    idempotency_key: str | None = None


@dataclass(frozen=True)
class JobResult:
    job_id: str
    state: JobState
    attempt: int
    output: Any = None
    error: str | None = None


@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: str
    job_id: str
    workflow_id: str
    attempt: int
    payload: Mapping[str, Any] = field(default_factory=dict)
