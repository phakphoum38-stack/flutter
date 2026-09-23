# AEOS to FlutterFixCode Adapter

## Purpose

This adapter is the explicit boundary between AEOS and the external flutter
tooling repository.

It does not decide which file should be repaired, bypass AEOS lineage
validation, declare a repair PASS, build the user installer, or execute
arbitrary FlutterFixCode work.

It only accepts a repair request that AEOS has already classified as
code-repairable, validates exact scope and identity, and produces a
deterministic envelope for the downstream repair tool.

## Required contract

A request must contain:

- repair_request_id
- lineage_id
- base_sha
- head_sha
- file_path
- fail_code
- failure_evidence
- allowed_files
- repair_scope
- required_checks

Optional location metadata:

- symbol
- line
- column

## Fail-closed rules

The adapter blocks when:

- the failure is a structural, lineage, identity, or evidence failure;
- the failure class is unknown;
- SHA values are missing or invalid;
- base and head are identical;
- lineage identity is missing;
- failure evidence is missing;
- the target path is unsafe;
- the file is outside AEOS allowed_files;
- repair scope is missing;
- required checks are missing.

WAITING and UNKNOWN are never converted into repair-ready requests.

## Repair loop

AEOS FAIL
  |
  +-- lineage / identity / evidence failure --> BLOCKED
  |
  +-- code-repairable
          |
          v
     Flutter Adapter
          |
          v
     READY_FOR_FLUTTERFIXCODE
          |
          v
     FlutterFixCode
          |
          v
        New SHA
          |
          v
      AEOS Recheck
          |
       PASS / FAIL

## Release boundary

This adapter is unrelated to installation and release packaging.

The release path remains:

repair -> new SHA -> AEOS recheck -> Final Gate -> release build -> installer

The external flutter repository remains tooling and integration only.
