# Engineering Tools

The `tools/` directory contains repository-level engineering tools used by local development and GitHub Actions.

## Principles

- Tools are not part of the Flutter runtime.
- Tools are versioned with the repository.
- Tools should use the Python standard library unless a dependency is explicitly justified.
- Every tool should be deterministic and safe to run in CI.
- Tools report findings; they do not silently modify application source.

## Current tools

- `repo_inspector/` — inventories source, Markdown, workflows, TODO markers, and syntax issues.
- `workflow_validator/` — validates GitHub Actions workflow structure and required fields.
- `version_validator/` — validates Flutter/Dart semantic application versions.
- `contract_checker/` — checks required contract/documentation markers.
- `security_scanner/` — performs conservative secret-like pattern detection.

## CI rule

A tool may become a hard merge gate only after it has its own tests and its findings are reviewed for false positives.
