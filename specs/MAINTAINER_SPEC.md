# copier-python-mlplatform — Project Specification

## Purpose

`copier-python-mlplatform` is a Copier template that provides a production-grade Python project foundation with opinionated tooling choices: **uv** for dependency management and **Taskfile** for automation.

It supports three project types:
- **base**: Minimal foundation for any Python project
- **package**: Python libraries with documentation-first conventions
- **pipeline-kfp**: Kubeflow Pipelines ML workflow projects

This template is intentionally **opinionated, consistent, and maintainable**.

---

## Core Design Principles
- **Single source of truth**: One template with project type selection, not multiple templates
- **Coarse-grained conditionals**: Whole files/directories toggle based on project type, not inline conditionals
- **Docs-first** (for package type): Documentation is a first-class artifact and documentation is done using Sphinx with Google docstrings.
- **Local-first**: Everything must build and run locally without external services
- **Low cognitive overhead**: Minimal configuration, clear defaults
- **Two core tools**: uv for dependency management, Taskfile for automation.

---

## Single Source of Truth Architecture

This template uses a **pragmatic hybrid approach** for CI/local parity where Taskfile is the single source of truth for project-specific checks, while pre-commit handles file utilities and provides automatic git hook integration.

### Responsibilities

| Concern | Owned By | Rationale |
|---------|----------|-----------|
| File hygiene (whitespace, EOF, YAML, secrets, large files) | Pre-commit (native hooks) | Battle-tested, staged-file optimized, cross-platform |
| Project checks (lint, format, md-check, test, build, compile) | Taskfile | Single definition, CI orchestration, full scope |
| Automatic local execution | Pre-commit (git hooks) | Native integration via `pre-commit install` |
| CI entry point | Taskfile (individual tasks) | CI runs `task pre-commit`, `task test`, etc. for visibility |
| Local full check | Taskfile (`task check`) | Convenience command to run all CI checks locally |

### How It Works

**Local commits:**
```
git commit → pre-commit hooks →
  ├── Native file utilities (fast, staged-files only)
  └── Delegated project checks: task lint, task format-check, task md-check
```

**CI pipeline (runs individual steps for visibility):**
```
CI →
  ├── task pre-commit (file utilities + lint + format-check + md-check via delegation)
  ├── task test
  ├── task docs (package and pipeline-kfp only)
  └── task build (package only)
```

**Local `task check` (same checks, single command):**
```
task check →
  ├── task pre-commit
  ├── task test
  ├── task docs (package and pipeline-kfp only)
  └── task build (package only)
```

### Design Rationale

| Requirement | How It's Met |
|-------------|--------------|
| Local-CI parity | Same `task lint`, `task format-check`, `task md-check` run locally (via pre-commit) and in CI (via `task pre-commit`) |
| Single source of truth | Taskfile defines all check logic; pre-commit is just the trigger |
| Automatic on commit | Pre-commit provides git hook integration |
| Bypassable | Standard `git commit --no-verify` works |
| Best practices | Each tool used for its strength |
| Full CI scope | Taskfile handles tests, builds, docs that pre-commit cannot |
| CI visibility | CI runs individual tasks so failures are easy to identify in GitHub Actions |

### What Runs Where

| Check | Local (on commit) | CI (on push) |
|-------|-------------------|--------------|
| File utilities (whitespace, secrets, YAML) | ✅ (pre-commit native) | ✅ (via `task pre-commit`) |
| `task lint` | ✅ (via pre-commit delegation) | ✅ (via `task pre-commit`) |
| `task format-check` | ✅ (via pre-commit delegation) | ✅ (via `task pre-commit`) |
| `task md-check` | ✅ (via pre-commit delegation) | ✅ (via `task pre-commit`) |
| `task test` | ❌ (too slow) | ✅ |
| `task docs` (package, pipeline-kfp) | ❌ | ✅ |
| `task build` (package only) | ❌ | ✅ |
| SQL formatting (pipeline-kfp) | ✅ (via pre-commit for queries/) | ✅ (via `task pre-commit`) |

**Note:** CI runs `task pre-commit` which handles file utilities, lint, format-check, and md-check via delegation. There are no separate `task lint`, `task format-check`, or `task md-check` steps in CI to avoid duplication.

---

## Explicit Non-Goals

The following are **out of scope** for this template and MUST NOT be implemented:

- Static typing enforcement (no `py.typed`, mypy, or pyright)
- ReadTheDocs or documentation publishing automation
- PyPI publishing or release automation
- Cloud provider configuration
- Template layering
- GitLab CI or other CI providers beyond those explicitly listed

---

## Template Root Structure

The template repository MUST have the following structure:

```text
copier-python-mlplatform/
├── copier.yml
├── project_spec.md
├── template/
│   ├── README.md.jinja
│   ├── pyproject.toml.jinja
│   ├── Taskfile.yml.jinja
│   ├── .pre-commit-config.yaml.jinja
│   ├── .python-version.jinja
│   ├── .gitignore.jinja
│   ├── {{ _copier_conf.answers_file }}.jinja
│   ├── src/
│   │   └── {{ package_name }}/
│   │       └── __init__.py
│   ├── tests/
│   │   ├── test_smoke.py.jinja
│   │   └── conftest.py
│   │
│   │   # package type only
│   ├── {% if project_type == 'package' %}docs{% endif %}/
│   │   ├── conf.py.jinja
│   │   ├── index.rst.jinja
│   │   └── overview.rst.jinja
│   │
│   │   # pipeline-kfp type only
│   ├── {% if project_type == 'pipeline-kfp' %}configs{% endif %}/
│   │   └── config.yaml.jinja
│   ├── {% if project_type == 'pipeline-kfp' %}notebooks{% endif %}/
│   │   └── .gitkeep
│   ├── {% if project_type == 'pipeline-kfp' %}Dockerfile{% endif %}.jinja
│   ├── {% if project_type == 'pipeline-kfp' %}notes{% endif %}/
│   │   └── project_design_doc.md
│   ├── {% if project_type == 'pipeline-kfp' %}queries{% endif %}/
│   │   ├── .gitkeep
│   │   └── example.sql
│   ├── {% if project_type == 'pipeline-kfp' %}.sqlfluff{% endif %}
│   ├── {% if project_type == 'pipeline-kfp' %}.sqlfluffignore{% endif %}
│   │
│   │   # pipeline-kfp type only (inside src/{{ package_name }}/)
│   │   # src/{{ package_name }}/config.py.jinja
│   │   # src/{{ package_name }}/run_pipeline.py.jinja
│   │   # src/{{ package_name }}/components/
│   │   # src/{{ package_name }}/core/
│   │   # src/{{ package_name }}/pipelines/
│   │
│   │   # github CI only
│   └── {% if ci_provider == 'github' %}.github{% endif %}/
│       └── workflows/
│           └── ci.yml.jinja
```

All files under `template/` are rendered into the target project.

---

## Copier Configuration (`copier.yml`)

### Required Questions

| Variable | Type | Default | Validation |
|----------|------|---------|------------|
| `project_name` | string | — | none |
| `package_name` | string | — | `^[a-z][a-z0-9_]*$` |
| `python_version` | string | `3.11.11` | none |
| `author_name` | string | — | none |
| `author_email` | string | — | none |
| `project_type` | choice | `base` | `[base, package, pipeline-kfp]` |
| `ci_provider` | choice | `none` | `[none, github]` |

Only `package_name` has validation. Trust user input on other fields.

No other Copier user prompts are allowed.

---

## Project Type: base

The base type provides the minimal foundation shared by all project types.

### Generated Structure

```text
my-project/
├── README.md
├── pyproject.toml
├── Taskfile.yml
├── .pre-commit-config.yaml
├── .python-version
├── .gitignore
├── src/
│   └── {{ package_name }}/
│       └── __init__.py
└── tests/
    ├── test_smoke.py
    └── conftest.py
```

### What's Included

- Python version managed via `.python-version`
- Dependency management via `uv`
- Build backend: `hatchling`
- `src/` layout
- Ruff for linting and formatting
- pytest for testing
- pre-commit hooks
- Taskfile automation
- Smoke test that verifies package is importable

---

## Project Type: package

The package type extends base with documentation-first conventions for Python libraries.

### Additional Generated Structure

```text
my-project/
├── ... (all files in project_type=base)
└── docs/
    ├── conf.py
    ├── index.rst
    └── overview.rst
```

### Additional Dependencies

- `sphinx`
- `furo`

### Additional Taskfile Commands

- `docs`: Build HTML documentation locally via `uv run sphinx-build -b html docs docs/_build/html`
- `docs-clean`: Remove built documentation via `rm -rf docs/_build`
- `build`: Build the package via `uv build`

### Documentation Requirements

- Sphinx with furo theme
- Google-style docstrings (napoleon extension)
- Narrative documentation structure with `index.rst` and `overview.rst`
- Local HTML build support
- No `_templates/` or `_static/` directories (add when needed)

---

## Project Type: kfp-pipeline

The pipeline-kfp type extends package structure with Kubeflow Pipelines ML workflow structure.

### Additional Generated Structure

```text
my-project/
├── ... (all base files)
├── configs/
│   └── config.yaml
├── notes/
│   └── project_design_doc.md
├── notebooks/
│   └── .gitkeep
├── queries/
│   ├── .gitkeep
│   └── example.sql
├── Dockerfile
├── .sqlfluff
├── .sqlfluffignore
├── docs/
    ├── conf.py
    ├── index.rst
    └── overview.rst
└── src/
    └── {{ package_name }}/
        ├── __init__.py
        ├── config.py
        ├── run_pipeline.py
        ├── components/
        │   └── __init__.py
        ├── core/
        │   └── __init__.py
        └── pipelines/
            └── __init__.py
```

### Additional Dependencies
These should be in dependencies =[...]
- `google-cloud-aiplatform>=1.127.0`
- `google-cloud-storage>=3.6.0`
- `kfp>=2.14.6`
- `pyarrow>=15.0.0`
- `pyyaml>=6.0.3`

### Additional Dev Dependencies
- `sqlfluff`

### Additional Taskfile Commands

- `compile`: Compile the pipeline to JSON
- `run-local`: Run pipeline components locally for testing
- `sql-fix`: Fix SQL formatting in queries/ via `uv run sqlfluff fix queries/`

### Directory Purposes

- `configs/`: YAML configuration files
- `notebooks/`: Jupyter notebooks for exploration and dataset IDs
- `queries/`: SQL query files (formatted with SQLFluff for BigQuery)
- `components/`: KFP component definitions
- `core/`: Core logic as plain python functions (data generation, training, prediction, model registration)
- `pipelines/`: Pipeline definitions
- `docs/`: Holds Sphinx documentation

### SQLFluff Configuration

The `.sqlfluff` config uses:
- Dialect: BigQuery
- Templater: Jinja
- Uppercase keywords, functions, literals, types
- 4-space indentation
- Trailing commas
- Max line length: 145
- Required AS for column and table aliases

The `.sqlfluffignore` file is empty by default (add SQL fragment files to ignore as needed).

---

## Python Tooling Requirements (All Project Types)

### pyproject.toml

The generated `pyproject.toml` MUST include:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{{ package_name }}"
version = "0.1.0"
description = ""
authors = [{ name = "{{ author_name }}", email = "{{ author_email }}" }]
readme = "README.md"
requires-python = ">={{ py_major_minor }}"
dependencies = []

[dependency-groups]
dev = [
    "ruff",
    "pytest",
    "pre-commit",
    "jupytext",
    "mdformat",
    "mdformat-gfm",
    # Additional deps based on project_type
]

[tool.hatch.build.targets.wheel]
packages = ["src/{{ package_name }}"]

[tool.ruff]
line-length = 88
target-version = "{{ py_target }}"
extend-exclude = ["*.md", ".venv"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

### .gitignore

The `.gitignore` MUST exclude:
- Data files: `*.csv`, `*.parquet`, `*.xlsx`
- IPython notebook checkpoints: `.ipynb_checkpoints/`
- Python artifacts: `*.pyc`, `__pycache__/`, `.venv/`, `dist/`, `*.egg-info/`
- Environment file: `.env`
- VS Code settings: `.vscode/settings.json` (but not `.settings-example.json`)
- Documentation build: `docs/_build/` (for package type)

---

## Code Quality Tooling (All Project Types)

### Ruff

- Used for linting and formatting
- Formatting via `ruff format`

### mdformat

- Used for Markdown formatting across all project types
- Plugins: `mdformat-gfm` for GitHub-Flavored Markdown support
- Wrapping: `--wrap keep` preserves existing line breaks
- Markdown files are excluded from `trailing-whitespace` hook (mdformat owns all markdown formatting)

---

## Pre-commit Hooks

Pre-commit handles two categories of hooks:

### File Utilities (Native Pre-commit)

These run natively in pre-commit with staged-file optimization:

| Hook | Source | All Types | Notes |
|------|--------|-----------|-------|
| `trailing-whitespace` | pre-commit-hooks v4.5.0 | ✅ | `exclude: '\.md$'` (markdown handled by mdformat) |
| `end-of-file-fixer` | pre-commit-hooks v4.5.0 | ✅ | |
| `check-yaml` | pre-commit-hooks v4.5.0 | ✅ | |
| `check-toml` | pre-commit-hooks v4.5.0 | ✅ | |
| `detect-private-key` | pre-commit-hooks v4.5.0 | ✅ | |
| `check-added-large-files` | pre-commit-hooks v4.5.0 | ✅ | `args: ["--maxkb=1000"]` |
| `sqlfluff-fix` | sqlfluff v3.4.2 | pipeline-kfp only | `files: ^queries/` |

### Project Checks (Delegated to Taskfile)

These delegate to Taskfile to maintain single source of truth:

```yaml
- repo: local
  hooks:
    - id: task-lint
      name: task lint
      entry: task lint
      language: system
      pass_filenames: false
      types: [python]

    - id: task-format-check
      name: task format-check
      entry: task format-check
      language: system
      pass_filenames: false
      types: [python]

    - id: task-md-check
      name: task md-check
      entry: task md-check
      language: system
      pass_filenames: false
      types: [markdown]
```

**Why delegation:** The same `task lint` definition runs both locally (via pre-commit) and in CI (directly). No duplication of tool version or configuration.

### Pre-commit Configuration Structure

The `.pre-commit-config.yaml` MUST follow this structure:

```yaml
# Pre-commit handles file utilities; Taskfile handles linting/formatting
# CI runs: task pre-commit (which invokes pre-commit run --all-files)

repos:
  # ============== File Utilities (native pre-commit) ==============
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
        exclude: '\.md$'
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: detect-private-key
      - id: check-added-large-files
        args: ["--maxkb=1000"]

  # ============== SQL Formatting (pipeline-kfp only) ==============
  {% if project_type == 'pipeline-kfp' %}
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.4.2
    hooks:
      - id: sqlfluff-fix
        files: ^queries/
  {% endif %}

  # ============== Project Checks (delegate to Taskfile) ==============
  - repo: local
    hooks:
      - id: task-lint
        name: task lint
        entry: task lint
        language: system
        pass_filenames: false
        types: [python]

      - id: task-format-check
        name: task format-check
        entry: task format-check
        language: system
        pass_filenames: false
        types: [python]

      - id: task-md-check
        name: task md-check
        entry: task md-check
        language: system
        pass_filenames: false
        types: [markdown]
```

Use pinned versions: pre-commit-hooks v4.5.0, sqlfluff 3.4.2

---

## Taskfile (All Project Types)

A `Taskfile.yml` MUST be generated using version: '3'.

Taskfile is the **single source of truth** for all project-specific check logic. CI calls Taskfile directly; pre-commit delegates to Taskfile for project checks.

### Base Tasks (all project types)

| Task | Command | Description | Local (via pre-commit) | CI |
|------|---------|-------------|------------------------|-----|
| `install` | `uv sync` | Install dependencies | ❌ (manual) | ✅ |
| `pre-commit` | `uv run pre-commit run --all-files` | Run file utilities + lint + format-check | ❌ (runs natively) | ✅ |
| `lint` | `uv run ruff check .` | Run ruff linter | ✅ (delegated) | ✅ (via pre-commit) |
| `lint-fix` | `uv run ruff check --fix .` | Auto-fix lint issues | ❌ (manual) | ❌ |
| `format` | `uv run ruff format .` | Format code | ❌ (manual) | ❌ |
| `format-check` | `uv run ruff format --check .` | Verify formatting | ✅ (delegated) | ✅ (via pre-commit) |
| `md-format` | `find . -name '*.md' -not -path './.venv*/*' -exec uv run mdformat --wrap keep {} +` | Format Markdown files | ❌ (manual) | ❌ |
| `md-check` | `find . -name '*.md' -not -path './.venv*/*' -exec uv run mdformat --wrap keep --check {} +` | Check Markdown formatting | ✅ (delegated) | ✅ (via pre-commit) |
| `test` | `uv run pytest` | Run tests | ❌ (too slow) | ✅ |
| `check` | pre-commit + test | Full CI checks (base) | ❌ (manual) | ✅ |

### Package Tasks (project_type == 'package')

Inherits all base tasks, plus:

| Task | Command | Description | Local | CI |
|------|---------|-------------|-------|-----|
| `docs` | `uv run sphinx-build -b html docs docs/_build/html` | Build documentation | ❌ (manual) | ✅ |
| `docs-clean` | `rm -rf docs/_build` | Clean docs | ❌ (manual) | ❌ |
| `build` | `uv build` | Build package | ❌ (manual) | ✅ |
| `check` | pre-commit + test + docs + build | Full CI checks (package) | ❌ (manual) | ✅ |

### Pipeline-KFP Tasks (project_type == 'pipeline-kfp')

Inherits all base tasks, plus:

| Task | Command | Description | Local | CI |
|------|---------|-------------|-------|-----|
| `docs` | `uv run sphinx-build -b html docs docs/_build/html` | Build documentation | ❌ (manual) | ✅ |
| `docs-clean` | `rm -rf docs/_build` | Clean docs | ❌ (manual) | ❌ |
| `sql-fix` | `uv run sqlfluff fix queries/` | Fix SQL formatting | ❌ (manual) | ❌ |
| `compile` | `echo 'TODO: implement compile'` | Compile pipeline to JSON (placeholder) | ❌ (manual) | ❌ |
| `run-local` | `echo 'TODO: implement run-local'` | Run pipeline locally (placeholder) | ❌ (manual) | ❌ |
| `check` | pre-commit + test + docs | Full CI checks (pipeline-kfp) | ❌ (manual) | ✅ |

### Taskfile Structure

The `Taskfile.yml` MUST follow this structure:

```yaml
version: '3'

tasks:
  # ===========================================
  # DEPENDENCIES
  # ===========================================
  install:
    desc: Install dependencies
    cmds:
      - uv sync

  # ===========================================
  # FILE UTILITIES (delegates to pre-commit)
  # ===========================================
  pre-commit:
    desc: Run pre-commit file utilities (whitespace, secrets, YAML, etc.)
    cmds:
      - uv run pre-commit run --all-files

  # ===========================================
  # PROJECT CHECKS (single source of truth)
  # ===========================================
  lint:
    desc: Run ruff linter
    cmds:
      - uv run ruff check .

  lint-fix:
    desc: Run ruff linter with auto-fix
    cmds:
      - uv run ruff check --fix .

  format:
    desc: Format code with ruff
    cmds:
      - uv run ruff format .

  format-check:
    desc: Check code formatting with ruff
    cmds:
      - uv run ruff format --check .

  md-format:
    desc: Format Markdown files with mdformat
    cmds:
      - find . -name '*.md' -not -path './.venv*/*' -exec uv run mdformat --wrap keep {} +

  md-check:
    desc: Check Markdown formatting with mdformat
    cmds:
      - find . -name '*.md' -not -path './.venv*/*' -exec uv run mdformat --wrap keep --check {} +

  test:
    desc: Run tests
    cmds:
      - uv run pytest

  # ===========================================
  # COMPOSITE TASKS
  # ===========================================
  check:
    desc: Run all CI checks
    cmds:
      - task: pre-commit  # Handles file utilities + lint + format-check + md-check via delegation
      - task: test
      # Package type adds: docs, build
      # Pipeline-kfp type adds: docs

  # ===========================================
  # PACKAGE TYPE ONLY (project_type == 'package')
  # ===========================================
  # docs:
  #   desc: Build documentation
  #   cmds:
  #     - uv run sphinx-build -b html docs docs/_build/html
  #
  # docs-clean:
  #   desc: Clean built documentation
  #   cmds:
  #     - rm -rf docs/_build
  #
  # build:
  #   desc: Build the package
  #   cmds:
  #     - uv build
  #
  # check (override for package):
  #   cmds:
  #     - task: pre-commit
  #     - task: test
  #     - task: docs
  #     - task: build

  # ===========================================
  # PIPELINE-KFP TYPE ONLY (project_type == 'pipeline-kfp')
  # ===========================================
  # docs, docs-clean: (same as package)
  #
  # sql-fix:
  #   desc: Fix SQL formatting
  #   cmds:
  #     - uv run sqlfluff fix queries/
  #
  # compile:
  #   desc: Compile pipeline to JSON (placeholder)
  #   cmds:
  #     - echo 'TODO: implement compile'
  #
  # run-local:
  #   desc: Run pipeline components locally (placeholder)
  #   cmds:
  #     - echo 'TODO: implement run-local'
  #
  # check (override for pipeline-kfp):
  #   cmds:
  #     - task: pre-commit
  #     - task: test
  #     - task: docs
```

CI providers MUST call individual tasks (`task pre-commit`, `task test`, etc.) for better visibility in CI logs, NOT `task check`. The `check` task exists for local convenience.

---

## CI Provider Support

### General Rules

- CI configuration files are thin wrappers that call Taskfile
- All check logic lives in `Taskfile.yml`
- CI MUST NOT duplicate logic defined in Taskfile
- CI runs individual tasks for better visibility in GitHub Actions UI
- `task pre-commit` handles file utilities + lint + format-check + md-check (no separate lint/format-check/md-check steps in CI)

### GitHub Actions

If `ci_provider == "github"`:
- Generate `.github/workflows/ci.yml` (content varies by project type)
- Use `.python-version`
- Install `uv` and `task`
- Run individual tasks: `task pre-commit`, `task test`, plus `task docs`/`task build` for applicable types

If `ci_provider == "none"`, no CI files are generated.

Use Copier's `_exclude` to ensure the GitHub Actions CI file is only created when `ci_provider == "github"`.

### CI Workflow Structure

The `.github/workflows/ci.yml` is generated differently based on project type for clearer CI visibility. CI runs individual tasks rather than `task check` so failures are easier to identify in the GitHub Actions UI.

**Base type (`project_type == 'base'`):**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install Task
        uses: arduino/setup-task@v2
        with:
          version: 3.x

      - name: Install dependencies
        run: uv sync

      - name: Run pre-commit (file utilities + lint + format-check + md-check)
        run: task pre-commit

      - name: Run tests
        run: task test
```

**Package type (`project_type == 'package'`):**

Same as base, plus:

```yaml
      - name: Build documentation
        run: task docs

      - name: Build package
        run: task build
```

**Pipeline-KFP type (`project_type == 'pipeline-kfp'`):**

Same as base, plus:

```yaml
      - name: Build documentation
        run: task docs
```

**Note:** CI does NOT run `task lint`, `task format-check`, or `task md-check` separately because `task pre-commit` already handles them via delegation. This avoids duplicate execution.

---

## README

A `README.md` MUST be generated with the following structure:

### Base Content (all project types)

```markdown
# {{ project_name }}

TODO — one sentence on what this project does.

A minimal, production-grade Python project scaffold.

This project was generated from a Copier template designed to standardize:
- Python packaging and project structure
- Local development and CI workflows
- Linting, formatting, and testing conventions

The goal is to provide a **reliable foundation** that scales from local development to CI without surprises.

---

## Requirements

- Python {{ python_version }}
- [uv](https://github.com/astral-sh/uv)
- [Task](https://taskfile.dev/)

Make sure these three tools are installed.

## Getting started

Install dependencies:

```bash
uv sync
```

Pre-commit hooks can be installed with:
```bash
pre-commit install
```

## Project structure

[Project structure tree — varies by project_type, see below]

* `src/` layout is used for correct packaging behavior
* Tooling configuration lives in `pyproject.toml`
* Automation is centralized in `Taskfile.yml`

## Development workflow

Common tasks:
```bash
task install        # Run uv sync
task lint           # Run linters
task lint-fix       # Run linters with automated fixes
task format         # Auto-format code
task format-check   # Check formatting without modifying
task md-format      # Auto-format Markdown files
task md-check       # Check Markdown formatting without modifying
task test           # Run tests
task check          # Run full CI suite (pre-commit + test + [docs] + [build])
task pre-commit     # Run pre-commit hooks on all files (includes lint + format-check + md-check)
```

## How checks are organized

This project uses a **hybrid approach** for code quality:

- **Pre-commit hooks** handle file utilities (whitespace, YAML validation, secrets detection) and delegate linting/formatting to Taskfile
- **Taskfile** is the single source of truth for all project-specific checks (lint, format, md-check, test)
- **CI** runs individual tasks (`task pre-commit`, `task test`, etc.) for better visibility in GitHub Actions

`task pre-commit` handles file utilities plus lint, format-check, and md-check via delegation, so CI does not need separate steps for these.

## Notes
* Tool versions are intentionally pinned where appropriate for reproducibility.
* CI (if enabled) mirrors local commands exactly via the Taskfile.
* This repository is intended to be adapted to your specific domain needs.
* Dependencies are handled by `uv` and `uv.lock` is where all dependencies are documented. As a result, `uv.lock` should be committed.
* For VSCode users, copy `.vscode/settings.example.json` to `.vscode/settings.json`
```

### Project Structure by Type

The "Project structure" section MUST show the correct tree for each project type.

**base:**
```text
.
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── pyproject.toml
├── README.md
├── src
│   └── {{ package_name }}
│       └── __init__.py
├── Taskfile.yml
└── tests
    └── test_smoke.py
```

**package:** (base + docs/)
```text
.
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── docs
│   ├── conf.py
│   ├── index.rst
│   └── overview.rst
├── pyproject.toml
├── README.md
├── src
│   └── {{ package_name }}
│       └── __init__.py
├── Taskfile.yml
└── tests
    └── test_smoke.py
```

**pipeline-kfp:** (package + configs/, notebooks/, notes/, queries/, Dockerfile, .sqlfluff, expanded src/)
```text
.
├── configs
│   └── config.yaml
├── Dockerfile
├── .gitignore
├── .sqlfluff
├── .sqlfluffignore
├── notebooks
│   └── .gitkeep
├── notes
│   └── project_design_doc.md
├── .pre-commit-config.yaml
├── .python-version
├── docs
│   ├── conf.py
│   ├── index.rst
│   └── overview.rst
├── pyproject.toml
├── queries
│   └── example.sql
├── README.md
├── src
│   └── {{ package_name }}
│       ├── __init__.py
│       ├── config.py
│       ├── run_pipeline.py
│       ├── components
│       │   └── __init__.py
│       ├── core
│       │   └── __init__.py
│       └── pipelines
│           └── __init__.py
├── Taskfile.yml
└── tests
    └── test_smoke.py
```

If `ci_provider == 'github'`, include `.github/workflows/ci.yml` in the tree.

### Additional Sections by Type

**package type** — Add after "Development workflow":

```markdown
## Documentation

Build documentation locally:
```bash
task docs
```

Then open `docs/_build/html/index.html` in your browser.

To clean built documentation:
```bash
task docs-clean
```

## Building the Package

Build the package:
```bash
task build
```
```

**pipeline-kfp type** — Add after "Development workflow":

```markdown
## Pipeline Development

Compile the pipeline:
```bash
task compile
```

Run pipeline components locally:
```bash
task run-local
```

### Directory Overview

- `configs/` — YAML configuration files
- `notebooks/` — Jupyter notebooks for exploration
- `notes/` — Project design specification
- `queries/` — SQL query files
- `src/{{ package_name }}/components/` — KFP component definitions
- `src/{{ package_name }}/core/` — Core business logic
- `src/{{ package_name }}/pipelines/` — Pipeline definitions

### SQL Formatting

Fix SQL formatting in queries/:
```bash
task sql-fix
```

SQLFluff is configured via `.sqlfluff` for BigQuery dialect with auto-formatting on pre-commit.
```

No badges or marketing language.

---

## Smoke Test

All project types MUST include `tests/test_smoke.py`:

```python
"""Smoke test to verify the package is importable."""


def test_import():
    """Verify that the package can be imported."""
    import {{ package_name }}

    assert {{ package_name }} is not None
```

---

## Quality Bar

A generated project MUST:
- Install via `uv sync`
- Pass `task check`
- Be immediately usable without modification
- Build documentation locally via `task docs` (package type only)
- Be importable as a Python package

---

## Future Considerations

This template is designed to be splittable if complexity grows. If any of the following occur, consider splitting into separate templates:

- 5+ project types
- Project types diverge in core tooling (e.g., different dependency managers)
- Different maintainers or release cadences needed
- Users frequently need to change project type after creation
