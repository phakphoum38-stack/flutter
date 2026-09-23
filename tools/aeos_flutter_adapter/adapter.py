"""AEOS -> FlutterFixCode repair boundary.

This module only validates and normalizes repair requests. It does not run
FlutterFixCode and it never decides which files may be edited on its own.
AEOS supplies the exact scope and lineage evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import PurePosixPath
from typing import Any


REPAIRABLE_CODES = frozenset(
    {
        "AEOS-CODE-FAIL",
        "AEOS-TEST-FAIL",
        "AEOS-STATIC-ANALYSIS",
        "AEOS-FLUTTER-ANALYZE",
        "AEOS-FLUTTER-TEST",
    }
)

BLOCKED_CODES = frozenset(
    {
        "AEOS-LINEAGE-ORPHAN",
        "AEOS-SHA-MISMATCH",
        "AEOS-MISSING-EVIDENCE",
        "AEOS-IDENTITY-CONFLICT",
        "AEOS-WORKFLOW-LINEAGE",
    }
)


class RepairRequestError(ValueError):
    """Raised when AEOS evidence is insufficient or unsafe for repair."""


@dataclass(frozen=True)
class RepairRequest:
    repair_request_id: str
    lineage_id: str
    base_sha: str
    head_sha: str
    file_path: str
    fail_code: str
    failure_evidence: str
    allowed_files: tuple[str, ...]
    repair_scope: str
    required_checks: tuple[str, ...]
    symbol: str | None = None
    line: int | None = None
    column: int | None = None

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "RepairRequest":
        required = (
            "repair_request_id",
            "lineage_id",
            "base_sha",
            "head_sha",
            "file_path",
            "fail_code",
            "failure_evidence",
            "allowed_files",
            "repair_scope",
            "required_checks",
        )
        missing = [key for key in required if key not in raw]
        if missing:
            raise RepairRequestError(
                "AEOS-MISSING-FIELD: " + ", ".join(sorted(missing))
            )

        return cls(
            repair_request_id=str(raw["repair_request_id"]),
            lineage_id=str(raw["lineage_id"]),
            base_sha=str(raw["base_sha"]),
            head_sha=str(raw["head_sha"]),
            file_path=str(raw["file_path"]),
            fail_code=str(raw["fail_code"]),
            failure_evidence=str(raw["failure_evidence"]),
            allowed_files=tuple(str(p) for p in raw["allowed_files"]),
            repair_scope=str(raw["repair_scope"]),
            required_checks=tuple(str(c) for c in raw["required_checks"]),
            symbol=raw.get("symbol"),
            line=_optional_int(raw.get("line")),
            column=_optional_int(raw.get("column")),
        )


@dataclass(frozen=True)
class AdapterResult:
    status: str
    repair_request_id: str
    lineage_id: str
    head_sha: str
    base_sha: str
    file_path: str
    fail_code: str
    adapter_version: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise RepairRequestError("AEOS-INVALID-LOCATION") from exc
    if result < 1:
        raise RepairRequestError("AEOS-INVALID-LOCATION")
    return result


def _sha(value: str) -> bool:
    return len(value) == 40 and all(c in "0123456789abcdef" for c in value.lower())


def _safe_repo_path(path: str) -> bool:
    if not path or path.startswith("/") or "\\" in path:
        return False
    pure = PurePosixPath(path)
    return ".." not in pure.parts and "." not in pure.parts and path == pure.as_posix()


def validate_repair_request(request: RepairRequest) -> None:
    """Fail closed before any request can reach FlutterFixCode."""

    if request.fail_code in BLOCKED_CODES:
        raise RepairRequestError(
            f"AEOS-NOT-REPAIRABLE: {request.fail_code}"
        )

    if request.fail_code not in REPAIRABLE_CODES:
        raise RepairRequestError(
            f"AEOS-UNKNOWN-FAILURE-CLASS: {request.fail_code}"
        )

    if not _sha(request.head_sha) or not _sha(request.base_sha):
        raise RepairRequestError("AEOS-SHA-MISSING-OR-INVALID")

    if request.head_sha == request.base_sha:
        raise RepairRequestError("AEOS-SHA-NOT-CHANGED")

    if not request.lineage_id.strip():
        raise RepairRequestError("AEOS-LINEAGE-MISSING")

    if not request.failure_evidence.strip():
        raise RepairRequestError("AEOS-MISSING-EVIDENCE")

    if not _safe_repo_path(request.file_path):
        raise RepairRequestError("AEOS-INVALID-FILE-PATH")

    if request.file_path not in set(request.allowed_files):
        raise RepairRequestError("AEOS-SCOPE-VIOLATION")

    if not request.repair_scope.strip():
        raise RepairRequestError("AEOS-REPAIR-SCOPE-MISSING")

    if not request.required_checks:
        raise RepairRequestError("AEOS-REQUIRED-CHECKS-MISSING")

    if any(not check.strip() for check in request.required_checks):
        raise RepairRequestError("AEOS-REQUIRED-CHECKS-INVALID")


def build_repair_envelope(raw: dict[str, Any]) -> dict[str, Any]:
    """Validate an AEOS request and return the immutable adapter envelope."""

    request = RepairRequest.from_dict(raw)
    validate_repair_request(request)

    payload = {
        "adapter": "aeos-flutter-repair",
        "adapter_version": "1",
        "status": "READY_FOR_FLUTTERFIXCODE",
        "request": asdict(request),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["request_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", help="Path to an AEOS repair-request JSON file")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    with open(args.request, encoding="utf-8") as handle:
        raw = json.load(handle)

    try:
        envelope = build_repair_envelope(raw)
    except RepairRequestError as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        return 2

    rendered = json.dumps(envelope, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
