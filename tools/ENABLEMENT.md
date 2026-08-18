# Toolchain Activation Guide

This document defines the supported way to enable the engineering toolchain in this repository.

## 1. Local prerequisites

- Git
- Flutter 3.24.3
- Python 3.12+

Verify:

```bash
flutter --version
python --version
git --version
```

## 2. Read-only audit first

Run the repository inspector before changing files:

```bash
python tools/repo_inspector/main.py .
```

The audit is read-only and produces repository inventory/report output.

## 3. Code Writer safe mode

Always preview generated changes first:

```bash
python tools/code_writer/main.py . \
  --spec tools/code_writer/example.json \
  --plan
```

`--plan` does not modify the repository.

Apply only after the plan has been reviewed:

```bash
python tools/code_writer/main.py . \
  --spec tools/code_writer/example.json \
  --apply
```

Existing files require explicit `--allow-update`.

## 4. Validation after generated changes

```bash
flutter pub get
flutter analyze
flutter test
python -m unittest discover -s tools/repo_inspector/tests -v
python tools/repo_inspector/main.py .
```

Generated code is never executed by Code Writer itself.

## 5. GitHub Actions

Pull requests and pushes to `main` run the repository gates. CI is the authoritative merge gate; local success alone is not sufficient.

The current pipeline separates validation from Android build:

```text
Flutter validation + Python inspection
                |
                +---- Web build
                |
                v
          Android build
                |
                v
           Final Gate
```

## 6. Security boundary

Code Writer must not:

- write outside the repository;
- use absolute or parent-traversal paths;
- modify `.git`;
- modify `.github/workflows` directly;
- execute generated code;
- bypass CI or release gates.

Workflow changes must go through normal review and CI.

## 7. Release rule

Do not treat a successful local generation as a release. A release requires the applicable GitHub workflow gates to pass.

Versioning remains deterministic: application version and build number are separate values, and an execution remains pinned to its selected version.
