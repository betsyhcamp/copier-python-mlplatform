# copier-python-base

A minimal, production-grade Copier template for Python projects.

This repository provides a **reliable foundation** for Python codebases by standardizing
project structure, tooling, and development workflows — without imposing any domain-specific
assumptions.

It is intended to be used directly, or as a base layer for more specialized templates
(e.g. data science, machine learning pipelines, or library templates).

---

## Design goals

- **Low cognitive overhead**  
  Sensible defaults that work out of the box.

- **Reproducibility**  
  Pinned tooling versions where appropriate, deterministic scaffolding.

- **Local to CI parity**  
  The same commands run locally and in CI via a single Taskfile.

- **Extensibility**  
  Domain-specific structure is intentionally out of scope.

---

## Non-goals

This template deliberately does **not** include:

- Data science or MLE-specific directory structures
- Notebooks or experiment scaffolding
- Dockerfiles or cloud configuration
- Release automation or dynamic versioning
- Opinionated editor personalization

Those concerns belong in higher-level templates built on top of this base.

---

## What this template provides

- `src/`-layout Python packaging
- Dependency management via **uv**
- Task-based automation using **Taskfile**
- Linting and formatting with **Ruff**
- Testing with **pytest**
- Pre-commit hooks with pinned versions
- Optional GitHub Actions CI
- Clean defaults aligned with modern Python tooling

---

## Usage

Generate a new project:

```bash
copier copy gh:betsyhcamp/copier-python-base my-project
```