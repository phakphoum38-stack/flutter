# Architecture Source of Truth

This repository is a tooling, build, validation, and integration repository. It does not redefine the enterprise architecture.

## Source of Truth

`phakphoum38-stack/ENTERPRISE_API_ARCHITECTURE_LOGIC_TH`

## Integration Boundary

```text
ENTERPRISE_API_ARCHITECTURE_LOGIC_TH
            |
            | Source of Truth
            v
       Contract / Version
            |
            v
         flutter
            |
      +-----+-----+
      |     |     |
    Tools Build Workflows
      |     |     |
      +-----+-----+
            |
            v
        CI / Audit
            |
            v
         Release
```

## Rules

1. Architecture rules are read from the Architecture repository.
2. Flutter tooling must not redefine architecture, contracts, or version policy.
3. Workflows validate implementation against the architecture contract.
4. Version and execution fencing are authoritative constraints.
5. A rejected execution must stop, release resources, reconcile delivery, and emit audit evidence.
6. A newer version may branch according to the architecture contract; an execution must not overwrite another execution in the same version.
7. CI failures are blocking failures. No bypass is allowed.
8. Code Writer cannot modify protected workflow files or execute generated code as part of validation.

## Repository Relationship

- Architecture: `https://github.com/phakphoum38-stack/ENTERPRISE_API_ARCHITECTURE_LOGIC_TH`
- Tooling / Build / Validation: `https://github.com/phakphoum38-stack/flutter`

The two repositories remain physically separate. Integration is by explicit contracts, pinned versions, validation, and audit records—not by copying the architecture into Flutter.
