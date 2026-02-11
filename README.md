# Playwright + Pytest Automation Framework

[![Tests](https://img.shields.io/badge/tests-38%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.14-blue)]()
[![Playwright](https://img.shields.io/badge/playwright-1.58.0-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

A **production-ready** test automation framework for [automationexercise.com](https://automationexercise.com) built with **Playwright**, **Pytest** and the **Page Object Model** pattern.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Architecture & Design Decisions](#architecture--design-decisions)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [API Endpoint Coverage](#api-endpoint-coverage)
- [Page Objects](#page-objects)
- [Data-Driven Testing](#data-driven-testing)
- [Performance Testing](#performance-testing)
- [Reporting](#reporting)
- [Dependencies](#dependencies)
- [CI/CD Integration](#cicd-integration)
- [Contributing & Development Guide](#contributing--development-guide)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Page Object Model (POM)** — clean separation between locators, actions and tests
- **Data-Driven Testing** — all credentials and config loaded from `test_data/test_data.json`
- **UI Tests** — smoke, login, registration, add-to-cart, checkout
- **API Tests** — all 14 REST endpoints (products, brands, auth, user CRUD)
- **Performance Tests** — API response-time thresholds + page-load metrics (TTFB, CLS, resource count)
- **Consent Banner Blocking** — network-level route blocking + DOM mutation observer (zero flakiness)
- **Reporting** — pytest-html, Allure, JUnit XML, code coverage
- **Parallel Execution** — `pytest-xdist` support for faster CI runs
- **Automatic Retry** — `pytest-retry` for flaky network-dependent tests
- **CI/CD Ready** — GitHub Actions example included

---

## Quick Start

### Prerequisites

- **Python 3.14+** (or 3.10+ minimum)
- **pip** (Python package manager)
- **Git** (for cloning)

### 1. Setup Environment

> **Why a virtual environment?** This project **must** run inside a virtual environment (`.venv`), not the global Python installation. A venv isolates all project dependencies (Playwright, pytest plugins, etc.) so they don't conflict with other projects or your system Python. It also ensures every contributor uses identical package versions pinned in `requirements.txt`. Never install project dependencies into your global Python — doing so can break other tools and makes version management unreliable.

```bash
# Clone repository
git clone https://github.com/thompsonoloko-droid/automation_playwright_dele.git
cd automation_playwright_dele

# Create virtual environment (isolates dependencies from global Python)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate          # Windows PowerShell
# source .venv/bin/activate     # macOS / Linux

# Verify you're in the venv (should show .venv path)
python -c "import sys; print(sys.prefix)"

# Install dependencies (into .venv only, not global)
pip install -r requirements.txt

# Install Playwright browsers (Chromium, Firefox, WebKit)
python -m playwright install
```

> **Tip:** If you see `ModuleNotFoundError` when running tests, you likely forgot to activate the venv. Run `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS/Linux) first.

### 2. Configure Test Data

Edit `test_data/test_data.json` with your test credentials. The file ships with working defaults — update the `users` section with a valid account on automationexercise.com:

```json
{
  "users": [
    {
      "id": "valid_user_1",
      "name": "Your Name",
      "email": "your_email@example.com",
      "password": "YourPassword123",
      "valid": true
    }
  ]
}
```

### 3. Run Tests

```bash
pytest tests/ -v --tb=short
```

---

## Project Structure

```
automation_playwright_dele/
├── pages/                            # Page Object Models
│   ├── base_page.py                  #   Base class: click, fill, screenshot, overlay handling
│   ├── home_page.py                  #   Navigation: login, products, cart, contact
│   ├── login_page.py                 #   Login form & registration form
│   ├── product_page.py               #   Product listing & add-to-cart
│   └── cart_page.py                  #   Cart count, checkout, empty check
│
├── tests/
│   ├── conftest.py                   # Shared fixtures & pytest hooks
│   ├── ui/                           # UI / E2E tests (10 tests)
│   │   ├── test_smoke.py             #   Homepage, registration, add-to-cart
│   │   ├── test_login.py             #   Valid & invalid login (data-driven)
│   │   └── test_checkout.py          #   Cart method & return-type checks
│   ├── api/                          # REST API tests (18 tests)
│   │   ├── test_product_api.py       #   Products list & search
│   │   ├── test_brands_api.py        #   Brands list & unsupported PUT
│   │   ├── test_auth_api.py          #   Login verify, unsupported methods
│   │   └── test_user_api.py          #   User CRUD + negative tests
│   └── performance/                  # Performance tests (10 tests)
│       ├── test_api_performance.py   #   API response-time thresholds
│       └── test_page_performance.py  #   Page load, CLS, resource count
│
├── utils/
│   ├── api_utils.py                  # REST client with validation & logging
│   └── web_utils.py                  # Playwright helpers (wait, click, fill)
│
├── test_data/
│   ├── test_data.json                # Credentials, API config, perf thresholds
│   └── test_data.csv                 # Alternative CSV format
│
├── reports/                          # Generated at runtime
│   ├── allure-results/               #   Allure report data
│   ├── screenshots/                  #   Auto-captured on failure
│   └── videos/                       #   Optional video recordings
│
├── pytest.ini                        # Markers, logging, timeout config
├── requirements.txt                  # Pinned dependency versions
└── README.md
```

---

## Architecture & Design Decisions

### Page Object Model (POM)

Every web page under test gets its own class in `pages/`. Each class:

1. **Inherits from `BasePage`** — which provides `click()`, `fill()`, `get_text()`, `take_screenshot()`, and automatic overlay dismissal
2. **Defines locators as class constants** (e.g. `LOGIN_BTN = "button[type='submit']"`) — if a selector changes, you update one line, not every test
3. **Exposes action methods** (e.g. `login(email, password)`) that tests call — tests read like plain English

```
BasePage
  ├── HomePage        (navigate_to_login, navigate_to_products, ...)
  ├── LoginPage       (login, register_new_user)
  ├── ProductPage     (add_product_to_cart)
  └── CartPage        (get_cart_items_count, proceed_to_checkout)
```

### Consent Banner Strategy

Cookie-consent overlays (the `fc-consent-root` widget) cause flaky clicks across the entire site. Instead of dismissing the banner per-test, we eliminate it at the infrastructure level in `conftest.py`:

1. **Network-level blocking** — `page.route()` aborts requests to known consent SDK domains so the overlay never loads
2. **DOM mutation observer** — an `addInitScript` watches for any element with `id="fc-consent-root"` and removes it immediately

This means **no test ever needs to handle consent** — it simply never appears.

### Data-Driven Design

All test inputs are externalised into `test_data/test_data.json`:

- **User credentials** — valid and invalid login scenarios
- **API configuration** — base URL, timeouts, search terms, login attempts
- **Performance thresholds** — per-endpoint response-time limits, page-load budgets, CLS thresholds
- **User templates** — registration and update payloads for API tests

Adding a new test scenario (e.g. a third invalid-login case) requires only a JSON edit — zero code changes.

### Fixture Architecture (`conftest.py`)

| Fixture                | Scope    | Purpose                                                              |
| ---------------------- | -------- | -------------------------------------------------------------------- |
| `browser_context_args` | session  | Sets viewport to 1920×1080, ignores HTTPS errors                     |
| `page`                 | function | Blocks consent routes, navigates to base URL, screenshots on failure |
| `test_data`            | function | Loads `test_data.json` into a backward-compatible list format        |
| `cleanup_videos`       | function | Deletes video recordings for passing tests (opt-in)                  |

---

## Running Tests

### Common Commands

```bash
# All tests (verbose, short traceback)
pytest tests/ -v --tb=short

# By marker
pytest -m smoke -v                # Critical-path smoke tests
pytest -m api -v                  # REST API tests only
pytest -m performance -v          # Performance tests only
pytest -m login -v                # Authentication tests
pytest -m regression -v           # Full regression suite

# Single file
pytest tests/ui/test_login.py -v

# Single test
pytest tests/ui/test_login.py::TestLogin::test_valid_login -v

# Keyword filter
pytest tests/ -k "brands or product" -v

# Stop on first failure
pytest tests/ -x -v

# With HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# With Allure report
pytest tests/ --alluredir=reports/allure-results

# With code coverage
pytest tests/ --cov=pages --cov=utils --cov-report=html

# Parallel execution (auto-detect cores)
pytest tests/ -n auto

# Headed mode (watch the browser)
pytest tests/ui/ -v --headed
```

### Test Markers

| Marker        | Scope                           | Example filter          |
| ------------- | ------------------------------- | ----------------------- |
| `smoke`       | Critical-path tests (3 tests)   | `pytest -m smoke`       |
| `regression`  | Full regression suite           | `pytest -m regression`  |
| `api`         | REST API tests (18 tests)       | `pytest -m api`         |
| `performance` | Response-time & page-load tests | `pytest -m performance` |
| `login`       | Authentication tests            | `pytest -m login`       |
| `cart`        | Shopping-cart tests             | `pytest -m cart`        |
| `checkout`    | Checkout-flow tests             | `pytest -m checkout`    |

---

## Test Coverage

### UI Tests — 10 tests across 3 files

#### `test_smoke.py` — Critical Path (3 tests)

| Test                          | What it verifies                                           |
| ----------------------------- | ---------------------------------------------------------- |
| `test_homepage_loads`         | Page title is "Automation Exercise"; logo image is visible |
| `test_user_registration_flow` | Register new user with timestamped email; verify URL       |
| `test_add_to_cart_flow`       | Navigate to products → add item → verify cart count ≥ 1    |

#### `test_login.py` — Data-Driven Login (5 tests)

| Test                                         | What it verifies                                             |
| -------------------------------------------- | ------------------------------------------------------------ |
| `test_valid_login[valid_user_1]`             | Login succeeds; "Logged in as" text is visible               |
| `test_invalid_login[invalid_email_password]` | Wrong credentials show error message                         |
| `test_invalid_login[empty_email]`            | Empty email field triggers HTML5 validation                  |
| _(additional parametrised runs)_             | One run per entry in `test_data.json` → scales automatically |

#### `test_checkout.py` — Cart Verification (2 tests)

| Test                                   | What it verifies                                      |
| -------------------------------------- | ----------------------------------------------------- |
| `test_cart_has_checkout_button`        | `CartPage.proceed_to_checkout` exists and is callable |
| `test_cart_item_count_returns_integer` | `get_cart_items_count()` returns `int`                |

---

### API Tests — 18 tests across 4 files

#### `test_product_api.py` — Products (4 tests)

| Test                         | API # | What it verifies                                        |
| ---------------------------- | ----- | ------------------------------------------------------- |
| `test_get_products_list`     | 1     | Returns non-empty `products` array, responseCode 200    |
| `test_search_product[Top]`   | 5     | POST search returns matching products with `name` field |
| `test_search_product[Dress]` | 5     | Same validation for "Dress" search term                 |
| `test_search_product[Jeans]` | 5     | Same validation for "Jeans" search term                 |

#### `test_brands_api.py` — Brands (2 tests)

| Test                               | API # | What it verifies                              |
| ---------------------------------- | ----- | --------------------------------------------- |
| `test_get_all_brands`              | 3     | Returns non-empty `brands` array (34 brands)  |
| `test_put_brands_list_returns_405` | 4     | PUT returns responseCode 405, "not supported" |

#### `test_auth_api.py` — Authentication (7 tests)

| Test                                                      | API # | What it verifies                     |
| --------------------------------------------------------- | ----- | ------------------------------------ |
| `test_post_to_products_list_returns_405`                  | 2     | POST to `/productsList` returns 405  |
| `test_search_product_without_param`                       | 6     | Missing `search_product` returns 400 |
| `test_verify_login_valid_credentials`                     | 7     | Valid email + password returns 200   |
| `test_verify_login_without_email`                         | 8     | Missing email param returns 400      |
| `test_delete_verify_login_returns_405`                    | 9     | DELETE to `/verifyLogin` returns 405 |
| `test_verify_login_invalid_credentials[nonexistent_user]` | 10    | Unknown email returns 404            |
| `test_verify_login_invalid_credentials[wrong_password]`   | 10    | Wrong password returns 404           |

#### `test_user_api.py` — User CRUD (5 tests)

| Test                                     | API # | What it verifies                     |
| ---------------------------------------- | ----- | ------------------------------------ |
| `test_create_user_account`               | 11    | POST `/createAccount` returns 201    |
| `test_delete_user_account`               | 12    | DELETE `/deleteAccount` returns 200  |
| `test_update_user_account`               | 13    | PUT `/updateAccount` returns 200     |
| `test_get_user_detail_by_email`          | 14    | GET returns user with correct fields |
| `test_get_user_detail_nonexistent_email` | —     | Unknown email returns 404            |

---

### Performance Tests — 10 tests across 2 files

#### `test_api_performance.py` (5 tests)

| Test                                    | What it measures                                             |
| --------------------------------------- | ------------------------------------------------------------ |
| `test_api_response_time[productsList]`  | GET `/productsList` responds within configured `max_ms`      |
| `test_api_response_time[brandsList]`    | GET `/brandsList` responds within configured `max_ms`        |
| `test_api_response_time[searchProduct]` | POST `/searchProduct` responds within configured `max_ms`    |
| `test_api_response_time[verifyLogin]`   | POST `/verifyLogin` responds within configured `max_ms`      |
| `test_api_concurrent_products_search`   | 5 concurrent search requests complete within burst tolerance |

#### `test_page_performance.py` (5 tests)

| Test                              | What it measures                                                |
| --------------------------------- | --------------------------------------------------------------- |
| `test_page_load_time[home]`       | TTFB + DOMContentLoaded within page-specific `max_ms` threshold |
| `test_page_load_time[products]`   | Same for `/products`                                            |
| `test_page_load_time[login]`      | Same for `/login`                                               |
| `test_page_load_time[contact_us]` | Same for `/contact_us`                                          |
| `test_page_load_time[test_cases]` | Same for `/test_cases`                                          |
| `test_homepage_resource_count`    | Homepage loads fewer than 100 network resources                 |
| `test_no_large_layout_shifts`     | Cumulative Layout Shift (CLS) stays below configured threshold  |

---

## API Endpoint Coverage

All 14 public API endpoints from [automationexercise.com/api_list](https://automationexercise.com/api_list) are tested:

| API # | Method   | Endpoint                    | Test File             | Status |
| ----- | -------- | --------------------------- | --------------------- | ------ |
| 1     | `GET`    | `/productsList`             | `test_product_api.py` | ✅     |
| 2     | `POST`   | `/productsList`             | `test_auth_api.py`    | ✅     |
| 3     | `GET`    | `/brandsList`               | `test_brands_api.py`  | ✅     |
| 4     | `PUT`    | `/brandsList`               | `test_brands_api.py`  | ✅     |
| 5     | `POST`   | `/searchProduct`            | `test_product_api.py` | ✅     |
| 6     | `POST`   | `/searchProduct` (no param) | `test_auth_api.py`    | ✅     |
| 7     | `POST`   | `/verifyLogin`              | `test_auth_api.py`    | ✅     |
| 8     | `POST`   | `/verifyLogin` (no email)   | `test_auth_api.py`    | ✅     |
| 9     | `DELETE` | `/verifyLogin`              | `test_auth_api.py`    | ✅     |
| 10    | `POST`   | `/verifyLogin` (invalid)    | `test_auth_api.py`    | ✅     |
| 11    | `POST`   | `/createAccount`            | `test_user_api.py`    | ✅     |
| 12    | `DELETE` | `/deleteAccount`            | `test_user_api.py`    | ✅     |
| 13    | `PUT`    | `/updateAccount`            | `test_user_api.py`    | ✅     |
| 14    | `GET`    | `/getUserDetailByEmail`     | `test_user_api.py`    | ✅     |

---

## Page Objects

All pages inherit from `BasePage` which provides:

| Method                      | Purpose                                           |
| --------------------------- | ------------------------------------------------- |
| `click(selector)`           | Click with 3-retry overlay dismissal              |
| `fill(selector, text)`      | Clear and type text into an input                 |
| `get_text(selector)`        | Return trimmed text content                       |
| `take_screenshot(name)`     | Save screenshot to `reports/screenshots/`         |
| `verify_url_contains(text)` | Assert current URL contains expected string       |
| `_dismiss_overlays()`       | Internal: remove consent/ad overlays before click |

### Creating a New Page Object

```python
# pages/contact_page.py
from pages.base_page import BasePage

class ContactPage(BasePage):
    """Contact Us page interactions."""

    # Locators (CSS selectors)
    NAME_INPUT = "input[data-qa='name']"
    EMAIL_INPUT = "input[data-qa='email']"
    SUBJECT_INPUT = "input[data-qa='subject']"
    MESSAGE_INPUT = "textarea[data-qa='message']"
    SUBMIT_BTN = "input[data-qa='submit-button']"

    def submit_contact_form(self, name: str, email: str, subject: str, message: str) -> None:
        """Fill and submit the contact form."""
        self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.SUBJECT_INPUT, subject)
        self.fill(self.MESSAGE_INPUT, message)
        self.click(self.SUBMIT_BTN)
```

### Using Page Objects in Tests

```python
# tests/ui/test_contact.py
import pytest
from pages.contact_page import ContactPage

class TestContact:
    @pytest.mark.regression
    def test_submit_contact_form(self, page):
        """Fill and submit the contact us form."""
        contact = ContactPage(page)
        contact.submit_contact_form("Joe", "joe@test.com", "Help", "Need assistance")
        # Assert success message, etc.
```

---

## Data-Driven Testing

All test data lives in `test_data/test_data.json`. Tests use `pytest.mark.parametrize` to generate one test run per data entry — **add new scenarios without writing code**.

### JSON Structure

```json
{
  "users": [
    { "id": "valid_user_1", "email": "...", "password": "...", "valid": true }
  ],
  "invalid_credentials": [
    { "id": "empty_email", "email": "", "password": "...", "error_contains": "..." }
  ],
  "api": {
    "base_url": "https://automationexercise.com/api",
    "timeout": 10,
    "search_terms": ["Top", "Dress", "Jeans"],
    "invalid_login_attempts": [ ... ],
    "test_user_template": { ... },
    "update_user_template": { ... }
  },
  "performance": {
    "api_response_time_ms": 3000,
    "page_load_time_ms": 5000,
    "cls_threshold": 0.35,
    "api_endpoints": [ ... ],
    "pages": [ ... ]
  }
}
```

### How Parametrisation Works

```python
# In test_login.py — this loads data at collection time
def get_valid_users():
    data = load_test_data()
    return [(u["id"], u["email"], u["password"]) for u in data["users"] if u["valid"]]

@pytest.mark.parametrize("user_id,email,password", get_valid_users())
def test_valid_login(self, page, user_id, email, password):
    # Runs once per valid user in test_data.json
    ...
```

### Adding a New Test Scenario

To add a second valid user, just add an entry to the `users` array in `test_data.json`:

```json
{
  "id": "valid_user_2",
  "name": "Second User",
  "email": "second@example.com",
  "password": "Pass123!",
  "valid": true
}
```

Pytest will automatically generate `test_valid_login[valid_user_2-second@example.com-Pass123!]`.

---

## Performance Testing

Performance tests run against the live site and assert measurable thresholds defined in `test_data.json`. All thresholds are deliberately generous to avoid false failures — the target site (automationexercise.com) runs on free shared hosting with variable response times.

### Threshold Rationale

Thresholds are set at roughly **2× typical observed response times** to absorb network jitter, CDN latency, and server-side load spikes while still catching genuine regressions.

| Metric                        | Typical Range | Peak Observed           | Threshold        | Why                                                                                |
| ----------------------------- | ------------- | ----------------------- | ---------------- | ---------------------------------------------------------------------------------- |
| API response (per endpoint)   | 500–2000 ms   | 4737 ms (searchProduct) | **5000 ms**      | Shared hosting spikes to 3–5 s under load                                          |
| Page DOMContentLoaded         | 1500–4000 ms  | 6305 ms (home)          | **8000 ms**      | Ad scripts & consent overlays add latency                                          |
| CLS (Cumulative Layout Shift) | 0.05–0.20     | 0.32                    | **0.35**         | Dynamic ad banners cause layout shifts beyond our control (Google "good" is ≤ 0.1) |
| API burst (5 sequential)      | 5000–12000 ms | —                       | **global × 1.5** | 50% burst tolerance for sequential request queuing                                 |

> **Tuning for your environment:** If testing against faster/dedicated infrastructure, lower the `max_ms` values in `test_data/test_data.json → performance`. Each endpoint and page has its own configurable threshold plus an inline `_comment` field documenting the reasoning.

### API Performance

- Each endpoint is timed over 3 iterations with a configurable `max_ms` per request
- A **5% tolerance** (`max_ms * 1.05`) is applied to each individual request to allow for minor network jitter
- A **concurrent burst test** fires 5 sequential search requests and asserts total time stays within a 50% burst tolerance of the global threshold
- Thresholds are tuned in `test_data.json → performance.api_endpoints`

### Page Load Performance

- **TTFB** (Time to First Byte) and **DOMContentLoaded** are measured via `window.performance.timing`
- Each page has its own `max_ms` threshold in `test_data.json → performance.pages`
- **Resource count** — asserts the homepage loads fewer than 100 network resources
- **CLS** (Cumulative Layout Shift) — measured via `PerformanceObserver` and asserted against `cls_threshold`

---

## Reporting

### HTML Report (pytest-html)

```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

Opens in any browser. Contains pass/fail status, duration, and captured logs.

### Allure Report

```bash
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

Interactive dashboard with trends, categories, timelines and attachments.

### JUnit XML (for CI)

```bash
pytest tests/ --junitxml=reports/junit.xml
```

### Code Coverage

```bash
pytest tests/ --cov=pages --cov=utils --cov-report=html
# Open htmlcov/index.html
```

### Screenshots

Failure screenshots are captured automatically by the `page` fixture and saved to `reports/screenshots/`. File pattern:

```
failure_{test_name}_{YYYYMMDD_HHMMSS}.png
```

---

## Dependencies

| Package           | Version | Purpose                         |
| ----------------- | ------- | ------------------------------- |
| pytest            | 8.4.0   | Test framework                  |
| playwright        | 1.58.0  | Browser automation              |
| pytest-playwright | 0.7.2   | Pytest ↔ Playwright integration |
| requests          | 2.32.5  | HTTP client for API tests       |
| allure-pytest     | 2.15.3  | Allure reporting                |
| pytest-html       | 4.2.0   | HTML test reports               |
| pytest-xdist      | 3.8.0   | Parallel test execution         |
| pytest-cov        | 6.1.0   | Code coverage                   |
| pytest-retry      | 1.7.0   | Flaky test retry                |
| pytest-timeout    | 2.4.0   | Timeout management              |
| pytest-base-url   | 2.1.0   | Configurable base URLs          |
| pytest-metadata   | 3.1.1   | Test run metadata               |
| pillow            | 12.1.0  | Screenshot image processing     |
| python-dotenv     | 1.2.1   | `.env` file loading             |
| black             | 26.1.0  | Code formatter                  |
| flake8            | 7.3.0   | Linter                          |
| isort             | 6.1.0   | Import sorter                   |
| mypy              | 1.19.1  | Static type checker             |

See [requirements.txt](requirements.txt) for the full pinned list.

---

## CI/CD Integration

This framework is designed to plug into any CI/CD platform. Below are production-ready examples for **GitHub Actions**, **Jenkins**, and **Azure DevOps** along with guidance on pipeline architecture, environment management, secrets handling, and notification strategies.

### Pipeline Architecture Overview

A recommended multi-stage pipeline follows this flow:

```
┌──────────┐     ┌────────────┐     ┌──────────┐     ┌──────────┐    ┌──────────┐
│  Lint &  │───▶│  Install &  │───▶│   Test   │───▶│  Report  │───▶│  Notify  │
│  Quality │     │   Setup    │     │  Matrix  │     │ & Publish│    │ & Gates  │
└──────────┘     └────────────┘     └──────────┘     └──────────┘    └──────────┘
```

| Stage                | What runs                                                                   |
| -------------------- | --------------------------------------------------------------------------- |
| **Lint & Quality**   | `black --check`, `flake8`, `mypy` — fail fast if code quality is poor       |
| **Install & Setup**  | `pip install -r requirements.txt`, `playwright install --with-deps`         |
| **Test Matrix**      | Run tests in parallel across browsers (Chromium, Firefox, WebKit)           |
| **Report & Publish** | Generate HTML / Allure / JUnit XML reports, upload as artifacts             |
| **Notify & Gates**   | Slack/email notifications on failure, quality gate enforcement (coverage %) |

### Triggers & Scheduling

| Trigger             | When to use                                       |
| ------------------- | ------------------------------------------------- |
| `push` to main      | Validate merged code immediately                  |
| `pull_request`      | Gate PRs — tests must pass before merge           |
| `schedule` (cron)   | Nightly regression run (e.g. `cron: '0 2 * * *'`) |
| `workflow_dispatch` | Manual trigger with optional parameter overrides  |

### Secrets & Environment Variables

Store sensitive data (test credentials, API keys) as CI secrets — **never commit them to the repo**:

| Variable             | Where to set                         | Used by                   |
| -------------------- | ------------------------------------ | ------------------------- |
| `TEST_USER_EMAIL`    | GitHub Secrets / Jenkins Credentials | `test_data.json` override |
| `TEST_USER_PASSWORD` | GitHub Secrets / Jenkins Credentials | `test_data.json` override |
| `SLACK_WEBHOOK_URL`  | GitHub Secrets / Jenkins Credentials | Failure notifications     |
| `ALLURE_SERVER_URL`  | GitHub Secrets (optional)            | Allure report publishing  |

Override test data at runtime using environment variables:

```bash
TEST_USER_EMAIL=${{ secrets.TEST_USER_EMAIL }} \
TEST_USER_PASSWORD=${{ secrets.TEST_USER_PASSWORD }} \
pytest tests/ -v
```

---

### GitHub Actions (Full Example)

`.github/workflows/tests.yml`:

```yaml
name: Playwright Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * 1-5" # Weekday nightly regression at 2 AM UTC
  workflow_dispatch: # Manual trigger from GitHub UI
    inputs:
      markers:
        description: "Pytest markers to run (e.g. smoke, api, regression)"
        required: false
        default: ""

permissions:
  contents: read
  checks: write # Needed for JUnit report annotations

jobs:
  # ── Stage 1: Code Quality ──────────────────────────────────
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.14"
          cache: "pip"

      - name: Install linters
        run: pip install black flake8 isort mypy

      - name: Check formatting (Black)
        run: black --check pages/ tests/ utils/

      - name: Lint (flake8)
        run: flake8 pages/ tests/ utils/ --max-line-length=120

      - name: Import order (isort)
        run: isort --check pages/ tests/ utils/

  # ── Stage 2: Test Matrix ───────────────────────────────────
  test:
    name: Tests (${{ matrix.browser }})
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false # Run all browsers even if one fails
      matrix:
        browser: [chromium, firefox, webkit]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.14"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install --with-deps ${{ matrix.browser }}

      - name: Run tests
        env:
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
        run: |
          MARKERS="${{ github.event.inputs.markers }}"
          MARKER_FLAG=""
          if [ -n "$MARKERS" ]; then MARKER_FLAG="-m $MARKERS"; fi
          pytest tests/ -v --tb=short \
            --browser ${{ matrix.browser }} \
            --html=reports/report-${{ matrix.browser }}.html --self-contained-html \
            --junitxml=reports/junit-${{ matrix.browser }}.xml \
            --alluredir=reports/allure-results \
            $MARKER_FLAG

      - name: Upload test reports
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-reports-${{ matrix.browser }}
          path: reports/
          retention-days: 30

      - name: Publish JUnit results
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: Test Results (${{ matrix.browser }})
          path: reports/junit-${{ matrix.browser }}.xml
          reporter: java-junit

  # ── Stage 3: Coverage ──────────────────────────────────────
  coverage:
    name: Code Coverage
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.14"
          cache: "pip"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install --with-deps chromium

      - name: Run with coverage
        run: |
          pytest tests/ -v --tb=short \
            --cov=pages --cov=utils \
            --cov-report=html:reports/coverage \
            --cov-report=xml:reports/coverage.xml \
            --cov-fail-under=60

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-report
          path: reports/coverage/

  # ── Stage 4: Notifications ─────────────────────────────────
  notify:
    name: Notify on Failure
    needs: [test, coverage]
    runs-on: ubuntu-latest
    if: failure()
    steps:
      - name: Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          fields: repo,message,commit,author,workflow
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### Key Features

- **`fail-fast: false`** — all three browsers complete even if one fails, so you see the full picture
- **`cache: 'pip'`** — caches installed pip packages between runs for faster installs
- **`workflow_dispatch` with inputs** — lets you trigger a run from the GitHub UI and optionally filter by marker (e.g. `smoke`)
- **JUnit reporter** — shows pass/fail annotations directly on the PR's Checks tab
- **Coverage quality gate** — `--cov-fail-under=60` fails the build if coverage drops below 60%
- **Retention policy** — artifacts kept for 30 days to save storage

---

### Jenkins Pipeline

`Jenkinsfile`:

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser to run tests on')
        string(name: 'MARKERS', defaultValue: '', description: 'Pytest markers (e.g. smoke, api)')
    }

    environment {
        VENV = "${WORKSPACE}/.venv"
    }

    stages {

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m playwright install --with-deps ${BROWSER}
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    black --check pages/ tests/ utils/
                    flake8 pages/ tests/ utils/ --max-line-length=120
                '''
            }
        }

        stage('Test') {
            steps {
                withCredentials([
                    string(credentialsId: 'test-user-email', variable: 'TEST_USER_EMAIL'),
                    string(credentialsId: 'test-user-password', variable: 'TEST_USER_PASSWORD')
                ]) {
                    sh """
                        . ${VENV}/bin/activate
                        MARKER_FLAG=""
                        if [ -n "${MARKERS}" ]; then MARKER_FLAG="-m ${MARKERS}"; fi
                        pytest tests/ -v --tb=short \
                            --browser ${BROWSER} \
                            --html=reports/report.html --self-contained-html \
                            --junitxml=reports/junit.xml \
                            --alluredir=reports/allure-results \
                            \$MARKER_FLAG
                    """
                }
            }
        }

        stage('Coverage') {
            steps {
                sh '''
                    . ${VENV}/bin/activate
                    pytest tests/ --cov=pages --cov=utils \
                        --cov-report=html:reports/coverage \
                        --cov-report=xml:reports/coverage.xml
                '''
            }
        }
    }

    post {
        always {
            // Publish JUnit results in Jenkins UI
            junit 'reports/junit.xml'

            // Publish HTML report
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Test Report',
                keepAll: true
            ])

            // Publish Allure report (requires Allure Jenkins plugin)
            allure includeProperties: false,
                   results: [[path: 'reports/allure-results']]

            // Archive all artifacts
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }

        failure {
            // Send Slack notification on failure
            slackSend(
                channel: '#test-automation',
                color: 'danger',
                message: "❌ Tests FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
            )
        }

        success {
            slackSend(
                channel: '#test-automation',
                color: 'good',
                message: "✅ Tests PASSED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

#### Jenkins Plugins Required

| Plugin                | Purpose                              |
| --------------------- | ------------------------------------ |
| HTML Publisher        | Render pytest-html report in Jenkins |
| Allure Jenkins Plugin | Allure report tab in build page      |
| JUnit                 | Test result trends and history       |
| Slack Notification    | Failure alerts to Slack              |
| Credentials Binding   | Inject secrets into build env        |

---

### Azure DevOps Pipeline

`azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include: [main]

pr:
  branches:
    include: [main]

schedules:
  - cron: "0 2 * * 1-5"
    displayName: "Nightly Regression"
    branches:
      include: [main]
    always: true

strategy:
  matrix:
    Chromium:
      browser: chromium
    Firefox:
      browser: firefox
    WebKit:
      browser: webkit

pool:
  vmImage: "ubuntu-latest"

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: "3.14"

  - script: |
      pip install -r requirements.txt
      python -m playwright install --with-deps $(browser)
    displayName: "Install dependencies"

  - script: |
      black --check pages/ tests/ utils/
      flake8 pages/ tests/ utils/ --max-line-length=120
    displayName: "Lint & format check"

  - script: |
      pytest tests/ -v --tb=short \
        --browser $(browser) \
        --html=reports/report-$(browser).html --self-contained-html \
        --junitxml=reports/junit-$(browser).xml \
        --alluredir=reports/allure-results \
        --cov=pages --cov=utils \
        --cov-report=html:reports/coverage
    displayName: "Run tests"
    env:
      TEST_USER_EMAIL: $(TEST_USER_EMAIL)
      TEST_USER_PASSWORD: $(TEST_USER_PASSWORD)

  - task: PublishTestResults@2
    condition: always()
    inputs:
      testResultsFormat: "JUnit"
      testResultsFiles: "reports/junit-$(browser).xml"
      testRunTitle: "Tests - $(browser)"
      mergeTestResults: true

  - task: PublishCodeCoverageResults@2
    condition: always()
    inputs:
      summaryFileLocation: "reports/coverage.xml"
      pathToSources: "$(Build.SourcesDirectory)"

  - task: PublishBuildArtifacts@1
    condition: always()
    inputs:
      PathtoPublish: "reports"
      ArtifactName: "test-reports-$(browser)"
```

---

### Docker Support (Any CI Platform)

For consistent environments across all developers and CI runners, use a Dockerfile:

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.58.0-noble

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "tests/", "-v", "--tb=short"]
```

Run locally or in any CI:

```bash
docker build -t pw-tests .
docker run --rm pw-tests                           # all tests
docker run --rm pw-tests pytest -m smoke -v         # smoke only
docker run --rm pw-tests pytest -m api -v           # API only
```

---

### Pipeline Integration Best Practices

| Practice                         | Why                                                                    |
| -------------------------------- | ---------------------------------------------------------------------- |
| **Separate lint from test jobs** | Fail fast on formatting without waiting for slow browser tests         |
| **Matrix across browsers**       | Catch browser-specific bugs; use `fail-fast: false` to see all results |
| **Cache pip & browsers**         | Playwright browsers are ~300 MB each — caching saves minutes per run   |
| **JUnit XML output**             | Universal format for CI dashboards (GitHub Checks, Jenkins, Azure)     |
| **Coverage quality gates**       | Enforce `--cov-fail-under=60` to prevent coverage regression           |
| **Artifact retention policy**    | Keep reports 14–30 days; nightly runs generate a lot of data           |
| **Nightly schedule**             | Full regression run at off-peak hours catches intermittent failures    |
| **Manual dispatch with markers** | Let QA trigger specific test subsets without code changes              |
| **Secrets for credentials**      | Never hardcode passwords — use CI secret stores                        |
| **Docker for consistency**       | Same OS, browser versions, and Python version everywhere               |

---

## Contributing & Development Guide

### Adding a New Page Object

1. Create `pages/your_page.py` inheriting from `BasePage`
2. Define locators as **class-level constants** (CSS selectors)
3. Add action methods that call `self.click()`, `self.fill()`, etc.
4. Import and use in your tests

### Adding a New UI Test

1. Create `tests/ui/test_your_feature.py`
2. Use `page` fixture (provides a Playwright page with consent blocking)
3. Instantiate your page objects, call actions, assert with `expect()`
4. Add appropriate markers: `@pytest.mark.smoke`, `@pytest.mark.regression`, etc.

### Adding a New API Test

1. Create or extend a file in `tests/api/`
2. Load config from `test_data.json` using the pattern in existing files
3. Use `requests` library directly (or `utils/api_utils.py` for complex flows)
4. Mark with `@pytest.mark.api`

### Adding a New Data-Driven Scenario

1. Add your data to the relevant section in `test_data/test_data.json`
2. If the test is already `@pytest.mark.parametrize`-driven, it picks up new entries automatically
3. No code changes needed

### Coding Standards

| Standard        | Tool   | Command                       |
| --------------- | ------ | ----------------------------- |
| Code formatting | Black  | `black pages/ tests/ utils/`  |
| Import sorting  | isort  | `isort pages/ tests/ utils/`  |
| Linting         | flake8 | `flake8 pages/ tests/ utils/` |
| Type checking   | mypy   | `mypy pages/ utils/`          |

### Commit & PR Guidelines

1. Run `pytest tests/ -v` locally — all tests must pass
2. Run `black` + `isort` to format code
3. Keep tests **atomic and independent** — no test should depend on another
4. Externalise data in `test_data.json` rather than hardcoding
5. Add docstrings for new classes, methods, and complex logic
6. Use descriptive commit messages (e.g. `feat: add contact-us page object`)

---

## Troubleshooting

| Problem                       | Fix                                                     |
| ----------------------------- | ------------------------------------------------------- |
| Browsers not installed        | `python -m playwright install`                          |
| Element not found             | Check selector in DevTools; add explicit waits          |
| Timeout errors                | Increase timeout in `BasePage` or `pytest.ini`          |
| Consent overlay blocks clicks | Already handled in `conftest.py` — check route patterns |
| Screenshots not saving        | Ensure `reports/screenshots/` exists                    |
| Performance test flaky        | Adjust `max_ms` in `test_data.json → performance`       |
| `ModuleNotFoundError`         | Activate venv: `.venv\Scripts\activate`                 |
| Tests collected but 0 run     | Check marker filter: `pytest -m smoke --collect-only`   |
| Parallel tests fail           | Some UI tests share state — use `-n 1` for UI tests     |

---

## License

MIT

---

**Last Updated:** February 2026 · Python 3.14 · Playwright 1.58.0 · 38 tests
