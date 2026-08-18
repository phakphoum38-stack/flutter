from __future__ import annotations

from collections import deque
from threading import Lock
from typing import Deque

from .models import Job


class InMemoryQueue:
    """Small deterministic queue adapter for local tests.

    Production adapters should preserve the same at-least-once contract and
    provide a durable acknowledgement mechanism.
    """

    def __init__(self) -> None:
        self._items: Deque[Job] = deque()
        self._lock = Lock()

    def publish(self, job: Job) -> None:
        with self._lock:
            self._items.append(job)

    def consume(self) -> Job | None:
        with self._lock:
            return self._items.popleft() if self._items else None

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
