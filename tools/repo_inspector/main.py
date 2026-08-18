#!/usr/bin/env python3
"""Repository inspector for code, Markdown, and GitHub Actions workflows.

Standard-library only. Intended for local use and CI.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_EXTENSIONS = {".py", ".md", ".yml", ".yaml", ".json", ".toml", ".dart"}
DEFAULT_EXCLUDES = {".git", ".dart_tool", "build", "reports", "__pycache__", ".venv", "venv"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]+['\"]"),
]
TODO_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WORKFLOW_RE = re.compile(r"^\.github/workflows/[^/]+\.(?:yml|yaml)$")

@dataclass
class FileRecord:
    path: str
    extension: str
    bytes: int
    lines: int
    kind: str
    headings: int = 0
    python_functions: int = 0
    python_classes: int = 0
    python_syntax_error: str | None = None
    todos: int = 0
    secret_like_matches: int = 0
    workflow_jobs: int = 0


def should_skip(path: Path) -> bool:
    return any(part in DEFAULT_EXCLUDES for part in path.parts)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def classify(path: Path) -> str:
    p = path.as_posix()
    if WORKFLOW_RE.match(p):
        return "github-workflow"
    if path.suffix == ".py":
        return "python"
    if path.suffix == ".md":
        return "markdown"
    return "text"


def inspect_file(root: Path, path: Path) -> FileRecord | None:
    if should_skip(path) or path.suffix.lower() not in DEFAULT_EXTENSIONS:
        return None
    text = read_text(path)
    rel = path.relative_to(root).as_posix()
    record = FileRecord(
        path=rel,
        extension=path.suffix.lower(),
        bytes=path.stat().st_size,
        lines=len(text.splitlines()),
        kind=classify(path),
        todos=len(TODO_RE.findall(text)),
        secret_like_matches=sum(len(p.findall(text)) for p in SECRET_PATTERNS),
    )
    record.headings = len(HEADING_RE.findall(text)) if path.suffix == ".md" else 0
    if path.suffix == ".py":
        try:
            tree = ast.parse(text, filename=rel)
            record.python_functions = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree))
            record.python_classes = sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
        except SyntaxError as exc:
            record.python_syntax_error = f"line {exc.lineno}: {exc.msg}"
    if record.kind == "github-workflow":
        # Deliberately lightweight YAML inspection: count top-level job keys under jobs:.
        in_jobs = False
        for line in text.splitlines():
            if re.match(r"^jobs:\s*$", line):
                in_jobs = True
                continue
            if in_jobs and line and not line.startswith((" ", "\t")):
                break
            if in_jobs and re.match(r"^  [A-Za-z0-9_.-]+:\s*$", line):
                record.workflow_jobs += 1
    return record


def scan(root: Path) -> list[FileRecord]:
    records = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            item = inspect_file(root, path)
            if item:
                records.append(item)
    return records


def build_summary(records: list[FileRecord]) -> dict:
    return {
        "files": len(records),
        "bytes": sum(r.bytes for r in records),
        "lines": sum(r.lines for r in records),
        "python_files": sum(r.kind == "python" for r in records),
        "markdown_files": sum(r.kind == "markdown" for r in records),
        "workflow_files": sum(r.kind == "github-workflow" for r in records),
        "python_functions": sum(r.python_functions for r in records),
        "python_classes": sum(r.python_classes for r in records),
        "todo_count": sum(r.todos for r in records),
        "secret_like_matches": sum(r.secret_like_matches for r in records),
        "python_syntax_errors": sum(r.python_syntax_error is not None for r in records),
    }


def markdown_report(root: Path, records: list[FileRecord]) -> str:
    summary = build_summary(records)
    lines = [
        "# Repository Inspector Report",
        "",
        f"Repository: `{root.resolve()}`",
        "",
        "## Summary",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- **{key}**: {value}")
    lines += ["", "## Files", "", "| Path | Kind | Lines | TODO | Secret-like |", "|---|---|---:|---:|---:|"]
    for r in records:
        lines.append(f"| `{r.path}` | {r.kind} | {r.lines} | {r.todos} | {r.secret_like_matches} |")
    errors = [r for r in records if r.python_syntax_error]
    lines += ["", "## Python Syntax Errors", ""]
    lines += [f"- `{r.path}`: {r.python_syntax_error}" for r in errors] or ["- None"]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect repository source, Markdown, and workflows")
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--report-dir", default="reports/repo-inspector")
    parser.add_argument("--fail-on-secret-like", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    records = scan(root)
    summary = build_summary(records)
    report_dir = root / args.report_dir
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "report.json").write_text(json.dumps({"summary": summary, "files": [asdict(r) for r in records]}, indent=2), encoding="utf-8")
    (report_dir / "report.md").write_text(markdown_report(root, records), encoding="utf-8")

    print("Repository Inspector")
    print(json.dumps(summary, indent=2))
    if summary["python_syntax_errors"]:
        return 1
    if args.fail_on_secret_like and summary["secret_like_matches"]:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
