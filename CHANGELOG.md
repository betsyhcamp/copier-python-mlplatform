# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).
This changelog format is based on [Keep a Changelog](https://keepachangelog.com/).


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