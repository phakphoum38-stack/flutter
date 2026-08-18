#!/usr/bin/env python3
"""Safe deterministic code writer for repository automation.

The writer does not execute generated code and never writes outside the repository.
Use --plan to preview changes and --apply to write them.
Existing files require --allow-update so accidental overwrites are explicit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MAX_FILE_BYTES = 256 * 1024
PROTECTED_PREFIXES = (".git", ".github/workflows")


def load_spec(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("files"), list):
        raise ValueError("spec must contain a files array")
    return data


def safe_relative_path(raw: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("file path must be a non-empty string")
    p = Path(raw)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"unsafe path: {raw}")
    normalized = p.as_posix().lstrip("./")
    if normalized == "." or any(normalized == prefix or normalized.startswith(prefix + "/") for prefix in PROTECTED_PREFIXES):
        raise ValueError(f"protected path: {raw}")
    return p


def validate_file(item: dict) -> tuple[Path, str]:
    if not isinstance(item, dict):
        raise ValueError("each file entry must be an object")
    rel = safe_relative_path(item.get("path"))
    content = item.get("content")
    if not isinstance(content, str):
        raise ValueError(f"content must be text: {rel}")
    if len(content.encode("utf-8")) > MAX_FILE_BYTES:
        raise ValueError(f"file too large: {rel}")
    return rel, content


def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def render(root: Path, spec: dict) -> list[tuple[Path, str, bool, str | None]]:
    changes = []
    for item in spec["files"]:
        rel, content = validate_file(item)
        target = root / rel
        old = target.read_text(encoding="utf-8") if target.exists() else None
        if old != content:
            changes.append((rel, content, old is not None, sha256_text(old) if old is not None else None))
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely write generated repository code from a JSON spec")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-update", action="store_true", help="allow replacing existing files")
    args = parser.parse_args()

    if args.plan == args.apply:
        parser.error("choose exactly one of --plan or --apply")

    root = Path(args.root).resolve()
    spec = load_spec(Path(args.spec).resolve())
    changes = render(root, spec)

    print(f"Code Writer: {len(changes)} file(s) changed")
    for rel, content, existed, old_sha in changes:
        action = "UPDATE" if existed else "CREATE"
        suffix = f" old_sha256={old_sha}" if old_sha else ""
        print(f"[{action}] {rel} ({len(content.encode('utf-8'))} bytes, new_sha256={sha256_text(content)}{suffix})")

    if args.plan:
        return 0

    blocked = [str(rel) for rel, _, existed, _ in changes if existed and not args.allow_update]
    if blocked:
        print("Refusing to overwrite existing files without --allow-update:")
        for path in blocked:
            print(f"  {path}")
        return 2

    for rel, content, _, _ in changes:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    print("Applied safely. Generated code was not executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
