# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).
This changelog format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- N/A

### Changed
- N/A

### Fixed
- N/A

### Removed
- N/A

---

## [0.1.1] - 2026-01-11

### Added
- `LICENSE` file (MIT).
- `CHANGELOG.md` to document template evolution.
- Maintainer documentation (`docs/MAINTAINER_SPEC.md`) describing scope, non-goals, and design decisions.

> Note: This release contains **no changes to the generated project output**.  
> It is a repository hygiene and documentation-only update.

---

## [0.1.0] - 2026-01-11

### Added
- Initial stable release of `copier-python-base`.
- Copier template with `template/` subdirectory structure.
- `copier.yml` prompts: `project_name`, `package_name`, `python_version`, `author_name`, `author_email`, `ci_provider`.
- `src/` layout with minimal package and smoke test.
- `pyproject.toml` using hatchling as build backend and uv-compatible dependency groups.
- Ruff configuration for linting and formatting.
- Pytest configuration and a minimal smoke test.
- Taskfile with `install`, `lint`, `format`, `test`, `ci`, and `all-precommit` tasks.
- Pre-commit hooks with pinned versions (ruff + basic hygiene hooks).
- Optional GitHub Actions CI that runs `task ci` and reads Python version from `.python-version`.
- `.gitignore` suitable for uv/venv caches and common Python artifacts.
- Optional VS Code settings example (`.vscode/settings.example.json`) aligned with `src/` layout and 88-char ruler.

[Unreleased]: https://github.com/betsyhcamp/copier-python-base/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/betsyhcamp/copier-python-base/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/betsyhcamp/copier-python-base/releases/tag/v0.1.0
