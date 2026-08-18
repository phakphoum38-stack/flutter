# Code Writer

Safe, deterministic repository code-writing tool.

## Usage

Preview changes first:

```bash
python tools/code_writer/main.py . --spec tools/code_writer/example.json --plan
```

Apply only after review:

```bash
python tools/code_writer/main.py . --spec tools/code_writer/example.json --apply
```

The tool:

- accepts a reviewed JSON generation spec;
- creates or updates files inside the repository only;
- blocks absolute paths, `..`, `.git`, and `.github/workflows`;
- limits generated files to 256 KiB each;
- supports plan/apply modes;
- never executes generated code.

## Architecture

```text
Request / AI Generator
        |
        v
Generation Spec (JSON)
        |
        v
Code Writer --plan
        |
        v
Review / Policy Gate
        |
        v
Code Writer --apply
        |
        v
Tests / Flutter / Inspector / Contract Gates
```

This is intentionally the **write layer**, not the AI model itself. An AI provider can produce the generation spec later without giving the provider direct filesystem write access.
