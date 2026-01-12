# copier-python-base — Project Specification

## Purpose

`copier-python-base` is a Copier template that provides a **minimal, production-grade Python project foundation**.

It is intended to:
- Standardize Python tooling and project hygiene
- Support data science, MLE, and library projects *indirectly*
- Serve as a stable base for future specialized templates

This template is intentionally **boring, small, and opinionated**.

---

## Explicit Non-Goals

The following are **out of scope** for this template and MUST NOT be implemented:

- Domain-specific directory structures (data science, MLE, libraries)
- Notebooks, pipelines, models, or datasets
- Dockerfiles
- Cloud provider configuration
- Template layering or `_extends`
- Project-type conditionals
- GitLab CI or other CI providers beyond those explicitly listed

Future templates will handle specialization.

---

## Template Root Structure

The template repository MUST have the following structure:

copier-python-base/
├── copier.yml
├── project_spec.md
├── template/
│ ├── README.md.jinja
│ ├── pyproject.toml.jinja
│ ├── Taskfile.yml.jinja
│ ├── .pre-commit-config.yaml.jinja
│ ├── .python-version.jinja
│ ├── .gitignore.jinja
│ ├── src/
│ │ └── {{ package_name }}/
│ │ └── __init__.py
│ └── tests/
│ └── test_smoke.py


All files under `template/` are rendered into the target project.

`src/{{ package_name }}/__init__.py` should be an empty file.
---

## Copier Configuration (`copier.yml`)

The template MUST prompt for the following variables:

### Required
- `project_name` (string)
- `package_name` (string, valid Python identifier)
- `python_version` (string, default: `3.11.14`)
- `author_name` (string)
- `author_email` (string)

### Optional
- `ci_provider` (string enum)
  - Allowed values: `none`, `github`
  - Default: `none`

In the event that `ci_provider=github` is specified an additional item should be in the template `template/.github/workflows/ci.yml.jinja` . In contrast, if `ci_provider=none` where the defualt value is present, do not add a CI .yml file. Use Copier approach `_exclude` to ensure the Github Actions CI file is only created when `ci_provider=github`. 

No other prompts are allowed.

---

## Python Tooling Requirements

### Environment & Packaging
- Python version managed via `.python-version`
- Dependency management via `uv`
- Build backend: `hatchling`
- `src/` layout is mandatory

### pyproject.toml
The generated `pyproject.toml` MUST include:

- `[project]` metadata
  - The [project] table MUST include a static version = "0.1.0"
  - Have requires-python = ">=3.11" based on the major.minor version of the default python version in this template. 
- `dependencies = []` (empty by default)
- `[dependency-groups.dev]` containing:
  - `ruff`
  - `pytest`
  - `pre-commit`
  - `jupytext`

- `[tool.ruff]` left empty for now
- `[tool.pytest.ini_options]` with only minimal configuration `testpaths = ["tests"]` and `pythonpath = ["src"]`

No optional dependencies, extras, or version pinning beyond reasonable defaults.

### .gitignore
The `.gitignore` should be default exlude the following:
- Data file types including: 
  - `*.csv`
  - `*.parquet'
  - `*.xlsx`
- IPthython notebook checkpoints `.ipynb_checkpoints/`
- Ignore files and directories including `*.pyc`, `__pycache__/`, `.venv/`, `dist/`, `*.egg-info/`
- Environment file `.env`
- VS Code settings file `.vscode/settings.json` although an example `.settings-example.json` should not be excluded.
---

## Code Quality Tooling

### Ruff
- Used for linting and formatting
- Formatting must be enabled via `ruff format`

### Pre-commit
The pre-commit configuration MUST include:
- `ruff`
- `ruff-format`
- `check-yaml`
- `check-toml`
- `end-of-file-fixer`
- `trailing-whitespace`
- `detect-private-key`
- `check-added-large-files` with `args: ["--maxkb=1000"]`
  
Use pinned versions for ruff (rev: v0.4.4) and pinned version for pre-commit (rev: v4.5.0)
---

## Taskfile

A `Taskfile.yml` MUST be generated and act as the **single source of truth** for automation.

Use Taskfile version: '3'

Required tasks:
- `install` to run `uv sync`
- `lint` to run ruff checks
- `format` to run ruff format
- `test` to run pytest
- `ci` in run install + lint + test
- `all-precommit` to run all precommit hooks

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

---

## README

A minimal `README.md` MUST be generated automatically containing:
- Project name
- Short description
- Setup instructions:
  - `uv sync`
  - `task lint`
  - `task test`

No badges or marketing language.

Nothing else should be automatically generated in the `README.md` as part of the template

---
## Copier Validation
Add validation only to `package_name` . Do not validate other fields so trust user imput on other fields. Let the Regex for validating `package_name` be `^[a-z][a-z0-9_]*$`


---
## Quality Bar

The generated project MUST:
- Pass `uv sync`
- Pass `task ci`
- Be immediately usable without modification
