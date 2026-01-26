# copier-python-mlplatform

A Copier template for Python projects, from minimal base projects, Python packages and ML pipelines.

This repository provides a **reliable foundation** for Python codebases by standardizing
project structure, tooling, and development workflows. It supports multiple project types
to accommodate different use cases while maintaining consistent conventions.

---

## Design Goals

- **Low cognitive overhead**
  Sensible defaults that work out of the box.

- **Reproducibility**
  Pinned tooling versions where appropriate, deterministic scaffolding.

- **Local to CI parity**
  The same commands run locally and in CI via a single Taskfile.

- **Clear seperation of concerns on code quality checks**
  File-level checks done via pre-commit with leveraging pre-commit's native githooks while Taskfile is used for project checks.

- **Extensibility**
  Three project types cover common use cases; the base type can be extended further.

---

## Project Types

| Type | Use Case | Includes |
|------|----------|----------|
| `base` | Minimal Python projects | Core tooling only |
| `package` | Distributable libraries | Sphinx docs, package build |
| `pipeline-kfp` | Kubeflow ML pipelines | Sphinx docs, SQL formatting, notebooks, Dockerfile, pipeline structure |

### Base (default)

A minimal Python project with linting, formatting, testing, and optional CI. Use this as a starting point for simple projects or as a foundation for custom extensions.

### Package

Everything in base, plus Sphinx documentation and package building with `uv build`. Use this for libraries you intend to distribute.

### Pipeline-KFP

Everything in package (minus package build), plus:
- Kubeflow Pipelines project structure (`components/`, `pipelines/`, `core/`)
- SQL queries directory with SQLFluff formatting
- Jupyter notebooks directory
- Dockerfile
- Configuration and notes directories

---

## What This Template Provides

**All project types:**
- `src/` layout Python packaging
- Dependency management via **uv**
- Task-based automation using **Taskfile**
- Linting and formatting with **Ruff**
- Testing with **pytest**
- Pre-commit hooks (file utilities + delegated linting/formatting)
- Optional GitHub Actions CI

**Package and pipeline-kfp types:**
- Sphinx documentation with Furo theme
- Autodoc with Google-style docstrings
- MyST parser for Markdown support

**Pipeline-kfp type only:**
- SQL formatting with SQLFluff (BigQuery dialect)
- KFP pipeline structure and dependencies

---

## How Checks Are Organized

This template uses a **hybrid approach** for code quality:

- **Pre-commit hooks** handle file utilities (whitespace, YAML validation, secrets detection) and delegate linting/formatting to Taskfile
- **Taskfile** is the single source of truth for all project-specific checks
- **CI** runs individual tasks for better visibility in GitHub Actions

```text
Local commits:
  git commit → pre-commit hooks →
    ├── Native file utilities (fast, staged-files only)
    └── Delegated: task lint, task format-check

CI pipeline:
  ├── task pre-commit (file utilities + lint + format-check)
  ├── task test
  ├── task docs (package/pipeline-kfp only)
  └── task build (package only)
```

---

## Project Structure

### Base Layout

```text
.
├── .github              # [optional, if ci_provider=github]
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .vscode
│   └── settings.example.json
├── pyproject.toml
├── README.md
├── src
│   └── {{ package_name }}
│       └── __init__.py
├── Taskfile.yml
└── tests
    ├── conftest.py
    └── test_smoke.py
```

### Package Layout

Base layout plus:
```text
├── docs
│   ├── api.rst
│   ├── conf.py
│   ├── index.rst
│   └── overview.rst
```

### Pipeline-KFP Layout

Package layout plus:
```text
├── configs
│   └── config.yaml
├── Dockerfile
├── notebooks
│   └── .gitkeep
├── notes
│   └── project_design_doc.md
├── queries
│   └── example.sql
├── .sqlfluff
├── .sqlfluffignore
└── src
    └── {{ package_name }}
        ├── config.py
        ├── run_pipeline.py
        ├── components
        │   └── __init__.py
        ├── core
        │   └── __init__.py
        └── pipelines
            └── __init__.py
```

---

## Usage

Install [Copier](https://copier.readthedocs.io/en/stable/), [uv](https://github.com/astral-sh/uv), and [Task](https://taskfile.dev/).

Generate a new project:

```bash
copier copy gh:betsyhcamp/copier-python-mlplatform my-project
```

You'll be prompted to select a project type and other options.

---

## Development Tasks

After generating a project, common tasks are:

```bash
task install        # Install dependencies (uv sync)
task lint           # Run linters
task lint-fix       # Run linters with auto-fix
task format         # Auto-format code
task format-check   # Check formatting without modifying
task test           # Run tests
task check          # Run full CI suite locally
task pre-commit     # Run pre-commit hooks on all files
```

Additional tasks by project type:

| Task | Package | Pipeline-KFP |
|------|---------|--------------|
| `task docs` | ✓ | ✓ |
| `task docs-clean` | ✓ | ✓ |
| `task build` | ✓ | — |
| `task sql-fix` | — | ✓ |
| `task compile` | — | ✓ (placeholder) |
| `task run-local` | — | ✓ (placeholder) |

---

## Contributing

- Check the latest changes in `CHANGELOG.md`
- Use [semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
- Feel free to open a GitHub issue

Originally derived from [copier-python-base](https://github.com/betsyhcamp/copier-python-base) but diverged to become a more specialized template for ML platform work.

---

Made with :heart: in Portland, OR.
