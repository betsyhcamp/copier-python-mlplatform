# copier-python-mlplatform

A minimal, production-grade Copier template for Python projects.

This repository provides a **reliable foundation** for Python codebases by standardizing
project structure, tooling, and development workflows without imposing any domain-specific assumptions.

It is intended to be used directly, or as a base layer for more specialized templates. Specialized templates might be those for data science, machine learning pipelines, or packages/libraries.

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

- `src/` layout Python packaging
- Dependency management via **uv**
- Task-based automation using **Taskfile**
- Linting and formatting with **Ruff**
- Testing with **pytest**
- Pre-commit hooks with pinned versions
- Optional GitHub Actions CI
- Clean defaults aligned with modern Python tooling

Here is the layout provided in this template: 
```text
.
├── .github **[optional]**
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── .vscode
│   └── settings.example.json
├── uv.lock
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

---

## Usage

Install `Copier` by following the [latest Copier installation instructions](https://copier.readthedocs.io/en/stable/). Also be sure you've installed [`uv`](https://github.com/astral-sh/uv) and [`Task`](https://taskfile.dev/).

Generate a new project in destination directory `my-project` from the command line by executing:

```bash
copier copy gh:betsyhcamp/copier-python-base my-project
```

---

## Other minor items
* Check the latest changes in `CHANGELOG.md`
* Happy to have others contribute or fork. If contributing, certainly use [semantic git commit messages](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716). 
* Feel free to open a Github issue wherever needed.
* originally derived from [copier-python-base](https://github.com/betsyhcamp/copier-python-base) but diverged to become a more specialized template.


Made with :heart: in Portland, OR.