# copier-python-mlplatform — Project Specification

## Purpose

`copier-python-mlplatform` is a Copier template that provides a production-grade Python project foundation with opinionated tooling choices: **uv** for dependency management and **Taskfile** for automation.

It supports three project types:
- **base**: Minimal foundation for any Python project
- **package**: Python libraries with documentation-first conventions
- **kfp-pipeline**: Kubeflow Pipelines ML workflow projects

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
│   │   └── test_smoke.py.jinja
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
    └── test_smoke.py
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

### Documentation Requirements

- Sphinx with furo theme
- Google-style docstrings (napoleon extension)
- Narrative documentation structure with `index.rst` and `overview.rst`
- Local HTML build support
- No `_templates/` or `_static/` directories (add when needed)

---

## Project Type: kfp-pipeline

The pipeline-kfp type extends base with Kubeflow Pipelines ML workflow structure.

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
├── Dockerfile
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

### Additional Taskfile Commands

- `compile`: Compile the pipeline to JSON
- `run-local`: Run pipeline components locally for testing

### Directory Purposes

- `configs/`: YAML configuration files
- `notebooks/`: Jupyter notebooks for exploration and dataset IDs
- `components/`: KFP component definitions
- `core/`: Core logic as plain python functions (data generation, training, prediction, model registration)
- `pipelines/`: Pipeline definitions

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
requires-python = ">={{ py_mm }}"
dependencies = []

[dependency-groups]
dev = [
    "ruff",
    "pytest",
    "pre-commit",
    "jupytext",
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

### Pre-commit

The pre-commit configuration MUST include:
- `ruff` (rev: v0.4.4)
- `ruff-format` (rev: v0.4.4)
- `check-yaml`
- `check-toml`
- `end-of-file-fixer`
- `trailing-whitespace`
- `detect-private-key`
- `check-added-large-files` with `args: ["--maxkb=1000"]`

Use pinned versions: ruff v0.4.4, pre-commit-hooks v4.5.0

---

## Taskfile (All Project Types)

A `Taskfile.yml` MUST be generated using version: '3'.

### Base Tasks (all project types)

| Task | Command | Description |
|------|---------|-------------|
| `install` | `uv sync` | Install dependencies |
| `lint` | `uv run ruff check .` | Run ruff linter |
| `lint-fix` | `uv run ruff check --fix .` | Run ruff linter with auto-fix |
| `format` | `uv run ruff format .` | Run ruff formatter |
| `test` | `uv run pytest` | Run pytest |
| `ci` | install + lint + test | Run full CI pipeline |
| `all-precommit` | `uv run pre-commit run --all-files` | Run all pre-commit hooks |

### Package Tasks (project_type == 'package')

| Task | Command | Description |
|------|---------|-------------|
| `docs` | `uv run sphinx-build -b html docs docs/_build/html` | Build HTML documentation locally |
| `docs-clean` | `rm -rf docs/_build` | Remove built documentation |

### KFP Pipeline Tasks (project_type == 'kfp-pipeline')

| Task | Command | Description |
|------|---------|-------------|
| `compile` | TBD | Compile pipeline to JSON |
| `run-local` | TBD | Run pipeline components locally |

CI providers MUST call `task ci` and MUST NOT duplicate logic.

---

## CI Provider Support

### General Rules

- CI configuration files are optional
- CI logic lives in `Taskfile.yml`
- CI files are thin wrappers only

### GitHub Actions

If `ci_provider == "github"`:
- Generate `.github/workflows/ci.yml`
- Use `.python-version`
- Install `uv`
- Run `task ci`

If `ci_provider == "none"`, no CI files are generated.

Use Copier's `_exclude` to ensure the GitHub Actions CI file is only created when `ci_provider == "github"`.

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
task install       # Run uv sync
task lint          # Run linters
task lint-fix      # Run linters with automated fixes
task format        # Auto-format code
task test          # Run tests
task ci            # Run full CI suite
task all-precommit # Run precommit hooks on all files
```

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

**pipeline-kfp:** (base + configs/, notebooks/, notes/, Dockerfile, expanded src/)
```text
.
├── configs
│   └── config.yaml
├── Dockerfile
├── .gitignore
├── notebooks
│   └── .gitkeep
├── notes
│   └── project_design_doc.md
├── .pre-commit-config.yaml
├── .python-version
├── pyproject.toml
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
- `notes/` — Project design documentation
- `src/{{ package_name }}/components/` — KFP component definitions
- `src/{{ package_name }}/core/` — Core business logic
- `src/{{ package_name }}/pipelines/` — Pipeline definitions
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
- Pass `task ci`
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
