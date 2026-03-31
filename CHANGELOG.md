# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).
This changelog format is based on [Keep a Changelog](https://keepachangelog.com/).



## [0.3.0] - 2026-03-30

### Added

- **Code coverage configuration** for all project types
  - `pytest-cov` as a dev dependency
  - `task test-cov` for running tests with coverage report (term-missing + HTML)
  - `[tool.coverage.*]` sections in `pyproject.toml` with branch coverage, common exclude patterns, and HTML output to `htmlcov/`
- **Markdown format-all tasks** for formatting tracked and untracked Markdown files
  - `task md-format-all` for autoformatting all Markdown files
  - `task md-check-all` for checking all Markdown files
- `htmlcov/` added to `.gitignore`

## [0.2.1] - 2026-02-27

### Fixes

- Fix Dockerfile from being included in project type `package`
- Fix Pre-commit and ruff from scanning notebooks directory
- Ensure Markdown formatting via mdformat and associated Taskfile commands only formats or checks formatting of Markdown files that are being tracked.
- Documentation reflecting above fixes. Included updates in README.md, README.md.jinja and MAINTAINER_SPEC.md

## [0.2.0] - 2026-02-12

### Added

- **mdformat integration** for Markdown formatting across all project types
  - `mdformat` + `mdformat-gfm` as dev dependencies
  - `task md-format` for autoformatting, `task md-check` for check-only
  - Delegated pre-commit hook (`task md-check`) triggers on markdown file changes
  - `--wrap keep` preserves existing line breaks

### Changed

- `trailing-whitespace` pre-commit hook now excludes `.md` files (mdformat owns markdown formatting)

## [0.1.0] - 2025-01-25

### Added

- **Three project types**: `base`, `package`, and `pipeline-kfp`
  - `base`: Minimal Python project with core tooling
  - `package`: Adds Sphinx documentation and package building
  - `pipeline-kfp`: Adds KFP pipeline structure, SQL formatting, notebooks, Dockerfile
- **Taskfile-based automation** with single source of truth architecture
  - Pre-commit delegates linting/formatting to Taskfile
  - CI runs individual tasks for visibility
- **Sphinx documentation** (package and pipeline-kfp types)
  - Furo theme
  - Autodoc with Google-style docstrings
  - MyST parser for Markdown support
- **SQLFluff integration** for SQL formatting (pipeline-kfp type)
- **GitHub Actions CI** (optional)
- **Pre-commit hooks** for file utilities and delegated project checks
- **Development tooling**:
  - uv for dependency management
  - Ruff for linting and formatting
  - pytest for testing