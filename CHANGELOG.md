# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- MIT LICENSE, CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md
- GitHub Issue & PR templates
- `.editorconfig` for consistent formatting across editors
- `requirements-dev.txt` for development-only dependencies
- `CHANGELOG.md`
- Runtime deprecation warning on `WebUtils`
- Dependabot reviewers and assignees
- `BASE_URL` environment variable support in conftest

### Changed

- CI lint jobs (ci-cd.yml & pr-checks.yml) now use **Ruff** instead of Black + Flake8 + isort
- All GitHub Actions workflows: added `permissions: contents: read` and `timeout-minutes`
- `ci-cd.yml`: added `concurrency` group to cancel stale runs
- `ci-cd.yml`: `continue-on-error` set to `false` on test steps
- API test files refactored to share config via `tests/api/conftest.py`
- `test_user_api.py`: unique emails use `uuid4` instead of `time.time()`
- `manual-test-run.yml`: `HAS_SLACK_WEBHOOK` moved to job-level env
- Pre-commit mypy: `types-all` → `types-requests`
- `product_page.py`: removed hardcoded domain from cart URL
- `cleanup_videos` fixture: fixed glob pattern and added existence check

### Removed

- Orphaned `test_data/test_data.csv` (unused by any code)
- Duplicate `[tool.pytest.ini_options]` from `pyproject.toml`
- Dev-only packages removed from `requirements.txt` (moved to `requirements-dev.txt`)

### Fixed

- `pyproject.toml`: removed `tests/` from mypy `exclude` so tests are type-checked
- `test_payment.py`: added missing pytest markers
