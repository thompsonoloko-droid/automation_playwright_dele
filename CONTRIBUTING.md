# Contributing to Automation Playwright

Thank you for considering contributing! Here's how to get started.

## Getting Started

1. **Fork** this repository and clone your fork locally.
2. Create a **virtual environment** and install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate   # Linux/macOS
    .venv\Scripts\activate      # Windows
    pip install -r requirements-dev.txt
    playwright install
    ```
3. Install **pre-commit hooks**:
    ```bash
    pre-commit install
    ```

## Development Workflow

1. Create a feature branch from `develop`:
    ```bash
    git checkout -b feature/my-change develop
    ```
2. Make your changes following the existing code style (PEP 8, Ruff-formatted).
3. Add or update tests as appropriate.
4. Run the test suite locally:
    ```bash
    pytest tests/ -v --tb=short
    ```
5. Commit with a clear message and push your branch.
6. Open a **Pull Request** against `develop`.

## Code Style

- **Formatter / Linter**: [Ruff](https://docs.astral.sh/ruff/) (enforced via pre-commit)
- **Type Checking**: mypy (strict on `pages/` and `utils/`)
- **Line Length**: 100 characters max
- **Imports**: sorted by Ruff (isort-compatible)

## Reporting Bugs

Open an issue using the **Bug Report** template and include:

- Steps to reproduce
- Expected vs actual behaviour
- Environment details (OS, Python version, browser)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).
