# automation_playwright_dele

[![Test Automation Pipeline](https://github.com/thompsonoloko-droid/automation_playwright_dele/actions/workflows/ci-cd.yml/badge.svg?branch=main)](https://github.com/thompsonoloko-droid/automation_playwright_dele/actions/workflows/ci-cd.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![Playwright Version](https://img.shields.io/badge/playwright-1.58.0-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A **production-ready Playwright-based test automation framework** for e-commerce testing with Page Object Model (POM) architecture, data-driven testing, CI/CD integration and advanced reporting.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Page Objects](#page-objects)
- [Data-Driven Testing](#data-driven-testing)
- [CI/CD Integration](#cicd-integration)
- [Reports](#reports)
- [Security](#security)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Features

- **Cross-Browser Testing** — Chromium, Firefox, WebKit via Playwright
- **Page Object Model** — Clean, maintainable, reusable test structure
- **Data-Driven Testing** — Parametrized tests with JSON test data
- **API Testing** — REST API endpoint verification with retry logic
- **Performance Testing** — API response-time and page-load benchmarks
- **Screenshot & Video** — Automatic failure screenshots, optional video recording
- **Consent Banner Handling** — Network-level blocking + DOM removal of cookie overlays
- **Allure & HTML Reporting** — Rich test reports with trends and analytics
- **CI/CD Pipelines** — 4 GitHub Actions workflows (push, PR, scheduled, manual)
- **Code Quality** — Ruff linting/formatting, mypy type checking, pre-commit hooks

## Quick Start

### Prerequisites

- Python 3.11+
- pip
- Git

### 1. Setup

```bash
git clone https://github.com/thompsonoloko-droid/automation_playwright_dele.git
cd automation_playwright_dele

python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m playwright install
```

### 2. Configure Credentials

Copy the example file and fill in your test account details:

```bash
cp .env.example .env
```

```dotenv
# Valid user login (automationexercise.com)
TEST_USER_NAME=Your Name
TEST_USER_EMAIL=your-email@example.com
TEST_USER_PASSWORD=your-password

# Payment card details (test values only!)
CARD_NAME=Your Name
CARD_NUMBER=4444333322221111
CARD_CVC=000
CARD_EXPIRY_MONTH=12
CARD_EXPIRY_YEAR=2030
```

Non-sensitive test data (invalid credentials, API config) lives in `test_data/test_data.json`.

### 3. Run Tests

```bash
pytest tests/                      # All tests
pytest tests/ -m smoke             # Smoke tests only
pytest tests/ui/ -v                # UI tests
pytest tests/api/ -v               # API tests
pytest tests/performance/ -v       # Performance tests
```

## Project Structure

```
automation_playwright_dele/
├── pages/                              # Page Object Models
│   ├── base_page.py                    # Base class — click, fill, wait, screenshot
│   ├── home_page.py                    # Homepage navigation
│   ├── login_page.py                   # Login & registration forms
│   ├── product_page.py                 # Product listing & cart actions
│   └── cart_page.py                    # Shopping cart interactions
│
├── tests/
│   ├── conftest.py                     # Shared fixtures (page, test_data, browser config)
│   ├── ui/                             # UI / E2E tests
│   │   ├── test_smoke.py               # Homepage, registration, add-to-cart (3 tests)
│   │   ├── test_login.py               # Data-driven login scenarios (2 parametrized)
│   │   ├── test_checkout.py            # Cart & checkout (2 tests)
│   │   └── test_payment.py             # Full order flow (1 test)
│   ├── api/                            # REST API tests
│   │   ├── conftest.py                 # Shared API session with retry logic
│   │   ├── test_auth_api.py            # Authentication endpoints (5 tests)
│   │   ├── test_brands_api.py          # Brands endpoint (2 tests)
│   │   ├── test_product_api.py         # Product listing & search (4 tests)
│   │   └── test_user_api.py            # User CRUD operations (5 tests)
│   └── performance/                    # Performance benchmarks
│       ├── test_api_performance.py     # API response time thresholds (3 tests)
│       └── test_page_performance.py    # Page load, CLS, resource count (4 tests)
│
├── utils/
│   ├── api_utils.py                    # APIUtils — HTTP client with response helpers
│   └── web_utils.py                    # Deprecated — use BasePage instead
│
├── test_data/
│   └── test_data.json                  # Non-sensitive test data & API config
│
├── reports/                            # Generated at runtime (git-ignored)
│   ├── screenshots/                    # Failure screenshots
│   ├── videos/                         # Optional video recordings
│   └── allure-results/                 # Allure report data
│
├── .github/
│   ├── workflows/
│   │   ├── ci-cd.yml                   # Main pipeline (lint → test → coverage → report)
│   │   ├── pr-checks.yml               # PR validation & smoke tests
│   │   ├── scheduled-smoke-tests.yml   # Every-6-hour health checks
│   │   └── manual-test-run.yml         # On-demand test runs
│   ├── dependabot.yml                  # Dependency vulnerability scanning
│   ├── ISSUE_TEMPLATE/bug_report.md    # Bug report template
│   ├── PULL_REQUEST_TEMPLATE.md        # PR checklist
│   └── copilot-instructions.md         # Copilot coding guidelines
│
├── docs/                               # Additional documentation
├── scripts/                            # Utility scripts
├── .env.example                        # Credential template (committed)
├── .editorconfig                       # Editor formatting rules
├── .pre-commit-config.yaml             # Pre-commit hooks (ruff, mypy)
├── pyproject.toml                      # Unified tool config (ruff, mypy, pytest)
├── pytest.ini                          # Pytest configuration & markers
├── requirements.txt                    # Runtime dependencies
├── requirements-dev.txt                # Dev/CI dependencies (ruff, mypy, black)
├── generate_allure_report.py           # Allure report generator
├── CHANGELOG.md                        # Release history
├── CONTRIBUTING.md                     # Contributor guidelines
├── SECURITY.md                         # Security policy
├── CODE_OF_CONDUCT.md                  # Community standards
└── LICENSE                             # MIT License
```

## Running Tests

```bash
# Common commands
pytest tests/ -v                       # Verbose output
pytest tests/ -x                       # Stop on first failure
pytest tests/ --maxfail=3              # Stop after 3 failures
pytest tests/ -v -s                    # Show print/log output
pytest tests/ -k "login"              # Match test name pattern
pytest tests/ -n auto                  # Parallel execution (pytest-xdist)

# By marker
pytest -m smoke                        # Critical path
pytest -m "smoke or api"               # Multiple markers
pytest -m regression                   # Full regression

# Reports
pytest tests/ --html=reports/test-report.html --self-contained-html
pytest tests/ --alluredir=reports/allure-results

# Coverage
pytest tests/ --cov=pages --cov=utils --cov-report=html
```

### Test Markers

```python
@pytest.mark.smoke              # Critical path tests
@pytest.mark.regression         # Full regression suite
@pytest.mark.api                # API tests
@pytest.mark.ui                 # UI tests
@pytest.mark.login              # Login-specific
@pytest.mark.cart               # Cart-specific
@pytest.mark.checkout           # Checkout-specific
@pytest.mark.performance        # Performance benchmarks
@pytest.mark.slow               # Long-running tests
@pytest.mark.skip_ci            # Skip in CI/CD
```

## Test Coverage

**31 tests** across 3 test suites:

### UI Tests (8 tests)

| File | Tests | Description |
|------|-------|-------------|
| `test_smoke.py` | 3 | Homepage load, user registration, add-to-cart flow |
| `test_login.py` | 2 | Data-driven valid/invalid login (parametrized from JSON) |
| `test_checkout.py` | 2 | Cart checkout button, item count verification |
| `test_payment.py` | 1 | Full E2E: login → browse → cart → checkout → payment → logout |

### API Tests (16 tests)

| File | Tests | Description |
|------|-------|-------------|
| `test_auth_api.py` | 5 | Login verification, missing params, invalid methods/credentials |
| `test_brands_api.py` | 2 | Brand listing, unsupported method rejection |
| `test_product_api.py` | 4 | Product listing, search, edge cases (POST/missing params) |
| `test_user_api.py` | 5 | Create, read, update, delete user accounts |

### Performance Tests (7 tests)

| File | Tests | Description |
|------|-------|-------------|
| `test_api_performance.py` | 3 | API response time thresholds, concurrent search burst |
| `test_page_performance.py` | 4 | Page load times, resource count, Cumulative Layout Shift |

## Page Objects

All page objects inherit from `BasePage`, which provides:

- **`click(selector)`** — Click with retry logic and automatic overlay dismissal
- **`fill(selector, text)`** — Fill input with overlay retry
- **`wait_for_element(selector)`** — Wait for visibility before interaction
- **`get_text(selector)`** — Retrieve element text content
- **`take_screenshot(name)`** — Manual screenshot capture
- **`_dismiss_overlays()`** — Remove consent/cookie banners

### Creating a New Page Object

```python
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """Page Object for the checkout page."""

    BUTTON_PLACE_ORDER = "button[data-qa='place-order']"
    INPUT_CARD_NUMBER = "input[name='card_number']"

    def fill_card_number(self, number: str) -> None:
        """Fill the card number field."""
        self.fill(self.INPUT_CARD_NUMBER, number)

    def place_order(self) -> None:
        """Click the place order button."""
        self.click(self.BUTTON_PLACE_ORDER)
```

### Using in Tests

```python
def test_checkout(page):
    checkout = CheckoutPage(page)
    checkout.fill_card_number("4444333322221111")
    checkout.place_order()
```

## Data-Driven Testing

Tests are parametrized from `test_data/test_data.json`:

```python
@pytest.mark.parametrize("user_id,email,password", get_valid_users())
def test_login(page, user_id, email, password):
    """Runs once per valid user defined in test_data.json."""
    login_page = LoginPage(page)
    login_page.login(email, password)
```

- **Valid credentials** load from environment variables (`TEST_USER_EMAIL`, etc.)
- **Invalid credentials** and API config are stored directly in `test_data.json`
- Tests are **automatically skipped** when required env vars are missing

Add new test scenarios by editing `test_data.json` — no code changes needed.

## CI/CD Integration

### GitHub Actions

Four production-ready workflows in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci-cd.yml` | Push, PR, schedule, manual | Full pipeline: Ruff lint → multi-browser tests → coverage → Allure report → Slack notify |
| `pr-checks.yml` | Pull request | Validate commits, smoke tests, coverage gate |
| `scheduled-smoke-tests.yml` | Every 6 hours + daily | Continuous health monitoring with Slack alerts |
| `manual-test-run.yml` | Manual dispatch | On-demand runs with suite/browser/parallel selection |

**Security features:**
- All actions pinned to commit SHAs (supply-chain protection)
- Least-privilege permissions per job
- Secret verification before test execution (fail-fast)
- Concurrency controls to cancel stale duplicate runs
- Dependabot scanning for pip + GitHub Actions dependencies

### Pipeline Overview

```
Push/PR → Ruff Lint → Tests (Chromium + Firefox + WebKit) → Coverage Report → Allure Report → Slack Notification
```

## Reports

### HTML Report

```bash
pytest tests/ --html=reports/test-report.html --self-contained-html
```

### Allure Report

```bash
pytest tests/ --alluredir=reports/allure-results
python generate_allure_report.py    # Or: allure serve reports/allure-results
```

### Failure Screenshots

Captured automatically on test failure:
```
reports/screenshots/failure_<test_name>_<timestamp>.png
```

## Security

- **Credentials in `.env`** — loaded via `python-dotenv`; `.env` is git-ignored
- **CI/CD secrets** — `TEST_USER_*` and `CARD_*` set as GitHub repository secrets
- **No secrets in code** — `test_data.json` contains only non-sensitive data
- **Actions pinned to SHAs** — prevents supply-chain attacks
- **Least-privilege permissions** — each CI job declares only what it needs
- **Dependabot** — weekly vulnerability scanning for pip and GitHub Actions

### Required Repository Secrets

Set in **Settings → Secrets and variables → Actions**:

| Secret | Purpose |
|--------|---------|
| `TEST_USER_NAME` | Test account display name |
| `TEST_USER_EMAIL` | Test account email |
| `TEST_USER_PASSWORD` | Test account password |
| `CARD_NAME` | Payment card name |
| `CARD_NUMBER` | Payment card number |
| `CARD_CVC` | Card CVC code |
| `CARD_EXPIRY_MONTH` | Card expiry month |
| `CARD_EXPIRY_YEAR` | Card expiry year |
| `SLACK_WEBHOOK_URL` | *(optional)* Slack notification webhook |

## Configuration

### pytest.ini

- Test discovery paths and patterns
- Strict markers, verbose output, short tracebacks
- Live logging at INFO level
- JUnit XML output (`xunit2`)

### pyproject.toml

Unified config for Ruff, mypy, isort, and Black — keeps tool settings in one place.

### conftest.py Fixtures

| Fixture | Scope | Description |
|---------|-------|-------------|
| `browser_context_args` | session | 1920×1080 viewport, HTTPS errors ignored |
| `page` | function | Fresh page with consent banners blocked, navigated to base URL |
| `test_data` | function | Loads `test_data.json` as a list of dicts |
| `cleanup_videos` | function | Deletes video recordings for passing tests |

### API Test Fixtures (`tests/api/conftest.py`)

| Fixture / Constant | Description |
|---------------------|-------------|
| `BASE_URL` | API base URL from `test_data.json` |
| `TIMEOUT` | Request timeout from config |
| `api_session` | Session-scoped `requests.Session` with retry logic (3 retries, exponential backoff, handles Cloudflare 520-524) |
| `api_config` | Session-scoped API configuration dict |

## Troubleshooting

**Playwright browsers not installed:**
```bash
python -m playwright install
```

**Element not found / Timeout errors:**
- Consent overlay may be blocking — `BasePage.click()` retries with overlay dismissal
- Check selector in browser DevTools
- Increase timeout: `self.timeout = 60000` in BasePage

**Tests skipped with `[NOTSET]`:**
- Valid-login tests require `TEST_USER_EMAIL` and `TEST_USER_PASSWORD` env vars
- Copy `.env.example` to `.env` and fill in credentials

**Capture Playwright traces for debugging:**
```bash
pytest tests/ui/test_login.py -v --trace=retain-on-failure
```

## Dependencies

### Runtime (`requirements.txt`)

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 9.0.2 | Test framework |
| playwright | 1.58.0 | Cross-browser automation |
| pytest-playwright | 0.7.2 | Pytest-Playwright integration |
| requests | 2.32.5 | HTTP client for API testing |
| python-dotenv | 1.2.1 | Load `.env` credentials |
| pytest-html | 4.2.0 | HTML test reports |
| allure-pytest | 2.15.3 | Allure reporting |
| pytest-cov | 7.0.0 | Code coverage |
| pytest-xdist | 3.8.0 | Parallel execution |
| pytest-retry | 1.7.0 | Retry flaky tests |
| pytest-timeout | 2.4.0 | Test timeout management |
| pytest-base-url | 2.1.0 | Configurable base URLs |
| pillow | 12.1.1 | Screenshot processing |

### Development (`requirements-dev.txt`)

| Package | Purpose |
|---------|---------|
| ruff | Linter & formatter (replaces black/flake8/isort in CI) |
| mypy | Static type checking |
| types-requests | Type stubs for requests |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines. In short:

1. Inherit page objects from `BasePage`
2. Add type hints and Google-style docstrings
3. Use pytest markers to categorize tests
4. Store test data in `test_data.json`, credentials in `.env`
5. Run `pre-commit run --all-files` before committing
6. Test locally before submitting a PR

## License

[MIT License](LICENSE)

---

**Last Updated:** February 13, 2026
**Playwright:** 1.58.0 | **Python:** 3.11+ | **Pytest:** 9.0.2
