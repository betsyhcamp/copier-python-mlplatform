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

## Contributing

- Check the latest changes in `CHANGELOG.md`
- Use [semantic commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
- Feel free to open a GitHub issue

---

Made with :heart: in Portland, OR.
