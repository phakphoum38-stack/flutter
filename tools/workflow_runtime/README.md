# Workflow Runtime

Implementation foundation for the workflow runtime defined by the upstream
`ENTERPRISE_API_ARCHITECTURE_LOGIC_TH` contracts.

## Boundary

```text
Architecture Contract
        |
        v
WorkflowEngine -> Queue -> StatelessRunner -> Handler
       |                         |
       +---- lifecycle ----------+
```

The engine owns lifecycle state. The runner only executes a leased job and
reports the result. Durable state must live behind the engine/storage boundary;
the runner must remain disposable and horizontally scalable.

## Current implementation

- Typed job/state/event models
- In-memory queue adapter for deterministic tests
- Lifecycle-owning workflow engine
- Stateless runner
- Per-job timeout
- At-least-once retry scheduling
- Duplicate submission protection
- Unit tests for success, retry/failure, and duplicate submission

## Production adapter requirements

A durable queue adapter must provide:

1. publish
2. lease/consume with visibility timeout
3. acknowledgement after durable result persistence
4. negative acknowledgement / retry
5. dead-letter support
6. idempotency support
7. observability for queue depth and age

The in-memory queue is intentionally not a production queue.
