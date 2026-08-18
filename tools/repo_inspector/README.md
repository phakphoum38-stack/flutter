# Repository Inspector

`repo_inspector` is a standard-library-only Python tool for reading and auditing repository text/code files.

It currently inspects:

- `.py` with Python AST parsing
- `.md` headings and line counts
- `.yml` / `.yaml` including GitHub Actions workflow detection
- `.json`, `.toml`, `.dart` as inventoryable text files
- TODO/FIXME markers
- secret-like literal patterns for CI review

## Local usage

```bash
python3 tools/repo_inspector/main.py .
python3 tools/repo_inspector/main.py . --fail-on-secret-like
python3 -m unittest discover -s tools/repo_inspector/tests -v
```

Reports are written to `reports/repo-inspector/` and are intentionally excluded from recursive scanning.

## CI role

The GitHub Actions workflow runs the inspector on pull requests, pushes to `main`, and manual dispatch. It uploads the JSON and Markdown reports as a workflow artifact.

The tool is **developer/CI tooling**, not the Workflow Engine runtime. It does not replace the Architecture Source of Truth at:

https://github.com/phakphoum38-stack/ENTERPRISE_API_ARCHITECTURE_LOGIC_TH
