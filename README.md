# copier-python-mlplatform

[![Template CI](https://github.com/betsyhcamp/copier-python-mlplatform/actions/workflows/template-ci.yml/badge.svg)](https://github.com/betsyhcamp/copier-python-mlplatform/actions/workflows/template-ci.yml) ![Python 3.11 | 3.12](https://img.shields.io/badge/python-3.11_%7C_3.12-blue) [![License: Unlicense](https://img.shields.io/badge/license-Unlicense-cyan.svg)](LICENSE)

A Copier template for Python projects, from minimal base projects, Python packages and ML pipelines.

This repository provides a **reliable foundation** for Python codebases by standardizing
project structure, tooling, and development workflows. It supports multiple project types
to accommodate different use cases while maintaining consistent conventions.

---

## Why Templates Still Matter with Coding Agents

Coding agents dramatically reduce the cost of generating code — bootstrapping a project,
writing boilerplate, and scaffolding new files now takes seconds. What they don't eliminate
is the need for repeatable engineering standards.

Every new project still needs consistent answers to the same questions: How are linting rules
configured? What does CI check? Where does package source live? How is documentation built?
What tasks run locally versus in CI? Getting these wrong creates friction — inconsistent
tooling across projects, CI that diverges from local development, and documentation that's
never wired up correctly.

Templates encode those decisions. This one standardizes **uv** for dependency management,
**Taskfile** as the local/CI interface, **Ruff** for lint and format, **Sphinx** for docs
where appropriate, and a project structure that scales from a minimal base to a full ML
pipeline scaffold. Every project generated from this template starts from a verified,
known-good baseline — with CI to prove it.

---

## Design Goals

- **Low cognitive overhead**
  Sensible defaults that work out of the box.

- **Reproducibility**
  `uv.lock` is the generated project's reproducibility mechanism. Tool versions in `pyproject.toml` are intentionally unpinned to avoid false precision; lock the versions you care about in `uv.lock`.

- **Local to CI parity**
  The same commands run locally and in CI via a single Taskfile.

- **Clear separation of concerns on code quality checks**
  File-level checks use pre-commit's native git hooks; Taskfile handles all project-specific checks.

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
- Markdown formatting with **mdformat** (GFM support)
- Testing with **pytest** and optional **coverage** via `pytest-cov`
- Pre-commit hooks (file utilities + delegated linting/formatting/md-check)
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
    └── Delegated: task lint, task format-check, task md-check

CI pipeline:
  ├── task pre-commit (file utilities + lint + format-check + md-check)
  ├── task test
  ├── task docs (package/pipeline-kfp only)
  └── task build (package only)
```

---

## Quickstart

### Prerequisites

- [Copier](https://copier.readthedocs.io/en/stable/) — `uv tool install copier`
- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Task](https://taskfile.dev/) — `brew install go-task` (macOS) or see [installation docs](https://taskfile.dev/installation/)

### Generate a project

```bash
copier copy gh:betsyhcamp/copier-python-mlplatform my-project
```

Copier prompts for seven values. Example answers for a `pipeline-kfp` project with GitHub Actions CI:

```text
Project name []: my-ml-project
Package name (valid Python identifier) []: my_ml_project
Python version [3.11.11]: 3.11.11
Author name []: Your Name
Author email []: your@email.com
Project type (base, package, pipeline-kfp) [base]: pipeline-kfp
CI provider (none, github) [none]: github
```

### Get started

```bash
cd my-project
uv sync
task test
```

### What gets generated

**`base`** — Minimal Python project with linting, formatting, testing, and optional CI:

```text
.
├── .copier-answers.yml
├── .github
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
│   └── my_ml_project
│       └── __init__.py
├── Taskfile.yml
└── tests
    ├── conftest.py
    └── test_smoke.py
```

**`package`** — Everything in base, plus Sphinx documentation and `uv build`:

```text
.
├── .copier-answers.yml
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .vscode
│   └── settings.example.json
├── docs
│   ├── api.rst
│   ├── conf.py
│   ├── index.rst
│   └── overview.rst
├── pyproject.toml
├── README.md
├── src
│   └── my_ml_project
│       └── __init__.py
├── Taskfile.yml
└── tests
    ├── conftest.py
    └── test_smoke.py
```

**`pipeline-kfp`** — Everything in package (minus build), plus KFP structure, SQL formatting,
notebooks, and Docker:

```text
.
├── .copier-answers.yml
├── .dockerignore
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .sqlfluff
├── .sqlfluffignore
├── .vscode
│   └── settings.example.json
├── config
│   └── config.yaml
├── Dockerfile
├── docs
│   ├── api.rst
│   ├── conf.py
│   ├── index.rst
│   └── overview.rst
├── notebooks
│   └── .gitkeep
├── notes
│   └── project_design_doc.md
├── pyproject.toml
├── queries
│   ├── .gitkeep
│   └── example.sql
├── README.md
├── src
│   └── my_ml_project
│       ├── __init__.py
│       ├── components
│       ├── core
│       ├── pipelines
│       └── schemas
├── Taskfile.yml
└── tests
    ├── conftest.py
    └── test_smoke.py
```

---

## Development Tasks

After generating a project, common tasks are:

```bash
task install        # Install dependencies (uv sync)
task lint           # Run linters
task lint-fix       # Run linters with auto-fix
task format         # Auto-format code
task format-check   # Check formatting without modifying
task md-format      # Auto-format Markdown files
task md-check       # Check Markdown formatting without modifying
task md-format-all  # Auto-format all Markdown files (tracked and untracked)
task md-check-all   # Check all Markdown formatting (tracked and untracked)
task test           # Run tests
task test-cov       # Run tests with coverage report
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

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **uv** for dependency management | Fast, deterministic; single tool for venv, sync, and build |
| **Taskfile** as CI/local interface | Single source of truth; CI calls the same commands as local dev |
| **pre-commit** for file hygiene | Native git hook integration; runs only on staged files |
| **Ruff** for lint + format | Single tool replaces flake8 + isort + black; fast |
| **Sphinx** only for package/pipeline types | Docs overhead not justified for minimal base projects |
| **SQLFluff** only for pipeline-kfp | BigQuery-specific; not relevant outside pipeline context |
| **No mypy/pyright by default** | Explicit non-goal; type annotations encouraged but not enforced at the template level |

---

## Contributing

- Check the latest changes in `CHANGELOG.md`
- Use [semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
- Feel free to open a GitHub issue

The full architecture and design decisions are documented in [specs/MAINTAINER_SPEC.md](specs/MAINTAINER_SPEC.md).

---

Made with :heart: in Portland, OR.
