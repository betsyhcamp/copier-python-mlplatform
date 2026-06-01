# copier-python-mlplatform

[![Template CI](https://github.com/betsyhcamp/copier-python-mlplatform/actions/workflows/template-ci.yml/badge.svg)](https://github.com/betsyhcamp/copier-python-mlplatform/actions/workflows/template-ci.yml) ![Python 3.11 | 3.12](https://img.shields.io/badge/python-3.11_%7C_3.12-blue) [![License: Unlicense](https://img.shields.io/badge/license-Unlicense-cyan.svg)](LICENSE)

A Copier template for production-oriented Python projects, including minimal projects, distributable packages, and Kubeflow-based ML pipelines.

This repository provides a **reliable foundation** for Python codebases by standardizing
project structure, tooling, and development workflows. It supports multiple project types
to accommodate different use cases while maintaining consistent conventions.

Use this template when you want a compact but sensible starting point for Python projects that need reproducible tooling, local/CI parity, and a clean path from package code to ML pipeline scaffolding.

---

## Why Templates Still Matter with Coding Agents

Coding agents make it easier to generate code, but they do not eliminate the need for repeatable engineering standards.

Every new project still needs consistent answers to the same questions including how linting is configured, which CI checks to include, where source code lives, how documentation is built, and which commands run locally versus in CI.

When those decisions are made ad hoc, teams accumulate friction through inconsistent tooling and workflows diverge.

---

## Design Goals

- **Low cognitive overhead**
  Sensible defaults that work out of the box.

- **Reproducibility**
  `uv.lock` is the generated project's reproducibility mechanism. Tool versions in `pyproject.toml` are intentionally unpinned to avoid false precision. Lock the package versions important to your work in `uv.lock`.

- **Local to CI parity**
  The same commands run locally and in CI via a single Taskfile.

- **Clear separation of concerns for code quality checks**
  File-level checks use pre-commit's native git hooks; Taskfile handles all project-specific checks.

- **Coverage of common use cases**
  Three project types cover common use cases; the base type can be extended further.

---

## Project Types

| Type | Use Case | Includes |
|------|----------|----------|
| `base` | Minimal Python projects that need consistent tooling | `src/` layout, pytest, Ruff, uv, Taskfile, optional GitHub Actions, optional pre-commit |
| `package` | Distributable Python packages | Everything in `base`, plus package build configuration and optional Sphinx documentation |
| `pipeline-kfp` | ML pipeline projects using Kubeflow Pipelines | Everything in `package`, plus KFP-oriented directories, Dockerfile, SQL formatting, notebooks, and pipeline scaffolding |

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

- [Copier](https://copier.readthedocs.io/en/stable/): Install [Copier here](https://copier.readthedocs.io/en/stable/#installation)
- [uv](https://docs.astral.sh/uv/): Install [uv here](https://docs.astral.sh/uv/getting-started/installation/)
- [Task](https://taskfile.dev/): Install [Task here](https://taskfile.dev/docs/installation)

Installation instructions vary by operating system and may change over time, so this README links to the official installation guides.

### Generate a project

```bash
copier copy gh:betsyhcamp/copier-python-mlplatform my-project
```

There are seven Copier prompts. Here is an example with answers for a `pipeline-kfp` project with GitHub Actions CI:

```text
Project name []: my-ml-project
Package name (valid Python identifier) []: my_ml_project
Python version [3.11.11]: 3.11.11
Author name []: Your Name
Author email []: your@email.com
Project type (base, package, pipeline-kfp) [base]: pipeline-kfp
CI provider (none, github) [none]: github
```

### Initialize the generated project

```bash
cd my-project
task install
task test
```

### What gets generated

#### **`base`** generated structure:

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

#### **`package`** generated structure:

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

#### **`pipeline-kfp`** generated structure:

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
| `task build-image` | — | ✓ |
| `task verify-image` | — | ✓ |
| `task push-image` | — | ✓ |
| `task build-push-image` | — | ✓ |

---

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **uv** for dependency management | Fast, deterministic; single tool for venv, sync, and build |
| **Taskfile** short commands for CI/local interface | Single source of truth; CI calls the same commands as local dev; expressive YAML-like syntax |
| **pre-commit** for file hygiene | Native git hook integration; runs only on staged files; mature tool with a large variety of hooks |
| **Ruff** for lint + format | Fast; one tool replaces separate linters + multiple formatters |
| **Sphinx** only for package/pipeline types | Mature doc generator with many options; compatible with Confluence |
| **SQLFluff** only for pipeline-kfp | Well supported and highly configurable; compatible with BigQuery-specific syntax; only relevant for pipelines |
| **No mypy/pyright by default** | Explicit non-goal; type annotations are encouraged, but enforcement is left to generated projects |

---

## Contributing

- Check the latest changes in `CHANGELOG.md`
- Use [semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
- Feel free to open a GitHub issue

The full architecture and design decisions are documented in [specs/MAINTAINER_SPEC.md](specs/MAINTAINER_SPEC.md).

---

Made with :heart: in Portland, OR.
