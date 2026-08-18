# Code Writer

Safe, deterministic repository code-writing tool.

## Usage

Preview changes first:

```bash
python tools/code_writer/main.py . --spec tools/code_writer/example.json --plan
```

Create new files:

```bash
python tools/code_writer/main.py . --spec tools/code_writer/example.json --apply
```

Update an existing file only when explicitly authorized:

```bash
python tools/code_writer/main.py . --spec tools/code_writer/example.json --apply --allow-update
```

The tool:

- accepts a reviewed JSON generation spec;
- creates or updates files inside the repository only;
- blocks absolute paths, `..`, `.git`, and `.github/workflows`;
- limits generated files to 256 KiB each;
- supports plan/apply modes;
- refuses existing-file overwrites unless `--allow-update` is explicit;
- prints SHA-256 fingerprints for planned content;
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
Code Writer --apply [--allow-update]
        |
        v
Tests / Flutter / Inspector / Contract Gates
```

This is intentionally the **write layer**, not the AI model itself. An AI provider can produce the generation spec later without giving the provider direct filesystem write access.
