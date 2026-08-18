# Combined Structure Lock

Status: ENABLED

This lock enables the complete project structure while preserving the repository boundary.

## Combined Structure

```text
ENTERPRISE_API_ARCHITECTURE_LOGIC_TH
        |
        | Source of Truth
        v
Architecture / Contract / Version Policy
        |
        v
flutter
        |
   +----+----+----+
   |    |    |    |
 Tools Build Workflows Audit
   |    |    |    |
   +----+----+----+
        |
        v
       CI
        |
        v
     Release
```

## Locked Boundaries

- Architecture repository remains the Source of Truth.
- Flutter remains the tooling, build, validation, and integration repository.
- Contracts and versions are referenced, not redefined.
- Workflow gates validate implementation against the authoritative contract.
- Execution fencing prevents overwrite between executions in the same version.
- A rejected execution must stop, release resources, reconcile delivery, and emit audit evidence.
- A newer version may branch according to policy.
- CI failures are blocking; bypass is prohibited.

## Build/Test Completion Gate

```text
Architecture Contract
  -> Contract Validation
  -> Version/Fencing Validation
  -> Tool Tests
  -> Flutter Analyze
  -> Flutter Test
  -> Web Build
  -> Android Build
  -> Final Gate
  -> Audit
  -> Release
```

No release is considered successful without an actual CI Workflow Run proving the final gate passed.

## Repository Separation

The repositories remain physically separate. The combined structure is a logical integration boundary only.
