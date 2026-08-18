# CI Operations Standard

## Purpose

This document defines the operational gates for the tooling repository. A local success is never sufficient for merge; GitHub Actions must produce a real run and a passing Final Gate.

## Required sequence

1. CI Health Check
2. Flutter validation
3. Python tool tests
4. Repository inspection
5. Contract validation
6. Security validation
7. Web build
8. Android build
9. Final Gate

## Run history

Every CI run records repository, commit SHA, workflow, event, ref, run ID, and run number as an artifact. Keep these records when investigating regressions.

## Code Writer policy

- `--plan` is allowed in CI.
- `--apply` is not allowed in CI.
- Generated code must pass validation before integration.
- Existing files require explicit update permission.
- Workflow files are protected from direct Code Writer changes.
- Generated code is never executed by the Code Writer itself.

## Version and execution fencing

A running execution owns a versioned state. A stale execution must stop when its version/token is rejected. It must release resources and reconcile delivery according to policy. It must never overwrite a newer execution in the same version.

A new version may branch from an earlier version, but versions remain immutable after publication.

## Failure policy

`FAIL` means stop. Do not use `|| true`, skip steps, or fabricate a passing status to bypass a gate. Diagnose the failing layer, fix the root cause, and run CI again.
