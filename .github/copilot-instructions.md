# GitHub Copilot Instructions for automation_playwright_dele

## Project Overview

This is a **production-ready Playwright-based test automation framework** for e-commerce testing with comprehensive Page Object Model (POM) architecture, data-driven testing, CI/CD integration and advanced reporting capabilities.

**Tech Stack:**

- Python 3.8+
- Playwright 1.58.0 (cross-browser automation)
- Pytest 9.0.2 (test framework)
- Page Object Model (POM) architecture
- Data-driven testing with JSON/CSV
- Allure & HTML reporting
- GitHub Actions CI/CD

## Repository Structure

```
automation_playwright_dele/
├── pages/          # Page Object Models (POM)
├── tests/          # Test suite (ui/, api/, performance/)
├── utils/          # Utility modules (web_utils, api_utils)
├── test_data/      # Test data files (JSON, CSV)
├── reports/        # Test execution reports
├── .github/        # CI/CD workflows
└── docs/           # Documentation
```

## Build & Test Commands

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (REQUIRED before running tests)
python -m playwright install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run smoke tests (critical path)
pytest tests/ -m smoke

# Run UI tests only
pytest tests/ui/ -v

# Run API tests only
pytest tests/api/ -v

# Run with HTML report
pytest tests/ --html=reports/test-report.html --self-contained-html

# Run with Allure report
pytest tests/ --alluredir=reports/allure-results
```

### Code Quality

```bash
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Type check with mypy
mypy .

# Run pre-commit hooks
pre-commit run --all-files
```

## Code Style Standards

### Formatting & Linting

- **Black** for code formatting (line length: 88)
- **Ruff** for linting
- **mypy** for static type checking
- **isort** for import sorting
- Pre-commit hooks MUST pass before committing

### Python Standards

- Use type hints on all functions and methods
- Add comprehensive docstrings (Google style)
- Follow PEP 8 naming conventions
- Meaningful variable/function names
- One assertion per test (when possible)

### Example Code Style

```python
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class YourPage(BasePage):
    """Page Object for your page.

    Attributes:
        BUTTON_SUBMIT: CSS selector for submit button
        INPUT_EMAIL: CSS selector for email input
    """

    BUTTON_SUBMIT: str = "button[type='submit']"
    INPUT_EMAIL: str = "input[name='email']"

    def fill_email(self, email: str) -> None:
        """Fill email field with provided value.

        Args:
            email: Email address to enter
        """
        self.fill(self.INPUT_EMAIL, email)
```

## Test Organization

### Test Markers

Use pytest markers to organize tests:

```python
@pytest.mark.smoke              # Critical path tests
@pytest.mark.regression         # Full regression suite
@pytest.mark.api                # API tests
@pytest.mark.ui                 # UI tests
@pytest.mark.login              # Login-specific
@pytest.mark.cart               # Cart-specific
@pytest.mark.checkout           # Checkout-specific
@pytest.mark.slow               # Long-running tests
@pytest.mark.performance        # Performance tests
@pytest.mark.mobile             # Mobile device emulation tests
@pytest.mark.skip_ci            # Skip in CI/CD
```

### Test Structure

```python
import pytest
from pages.home_page import HomePage

class TestFeature:
    """Test suite for feature X."""

    @pytest.mark.smoke
    def test_feature_works(self, page: Page, test_data: dict) -> None:
        """Test that feature X works correctly.

        Args:
            page: Playwright page fixture
            test_data: Test data from test_data.json
        """
        home_page = HomePage(page)
        # Test implementation
        assert expected_condition
```

### Fixtures Available

- `page`: Playwright page fixture (auto-navigated with consent banners blocked)
- `test_data`: Loads non-sensitive config from test_data.json
- `browser_context_args`: Browser viewport and settings configuration
- `cleanup_videos`: Optional cleanup fixture for video recordings
- `mobile_page`: Mobile device emulation page (iPhone, Pixel, Galaxy, iPad)

## Mobile Device Emulation Testing

The framework supports mobile device emulation via the `mobile_page` fixture.

### Supported Devices

- `iPhone 13`, `Pixel 7`, `Galaxy S21`, `iPad Mini`

### Writing Mobile Tests

```python
import pytest

@pytest.mark.mobile
def test_mobile_feature(mobile_page):
    """Test feature on mobile viewport."""
    mobile_page.goto("https://automationexercise.com")
    assert mobile_page.viewport_size["width"] < 1000
```

### Running Mobile Tests

```bash
pytest tests/ui/test_mobile.py -m mobile -v
pytest tests/ui/test_mobile.py --mobile-device "Pixel 7" -v
```

All mobile tests must:

- Use the `mobile_page` fixture (not `page`)
- Be decorated with `@pytest.mark.mobile`
- Avoid relying on hover interactions (touch devices don't hover)
- Use `mobile_page.viewport_size` to verify responsive behaviour

## Data-Driven Testing

Tests are parametrized using data from `test_data/test_data.json`:

```python
@pytest.mark.parametrize("user_id,email,password", get_valid_users())
def test_login(page, user_id, email, password):
    """Test runs once per user in test_data.json"""
    pass
```

**Important:** Add new test data to `test_data.json` instead of hardcoding values.

## Page Object Model (POM)

### Creating New Page Objects

1. **Inherit from BasePage**: All page objects must extend `pages.base_page.BasePage`
2. **Define locators as class constants**: Use descriptive, ALL_CAPS names
3. **Implement action methods**: One method per user action
4. **Use BasePage utilities**: click(), fill(), get_text(), wait_for_element()

```python
from pages.base_page import BasePage

class NewPage(BasePage):
    """Page Object for new page."""

    # Locators
    BUTTON_SUBMIT = "button[type='submit']"
    INPUT_NAME = "input[name='fullname']"

    def fill_name(self, name: str) -> None:
        """Fill name input field."""
        self.fill(self.INPUT_NAME, name)

    def submit_form(self) -> None:
        """Click submit button."""
        self.click(self.BUTTON_SUBMIT)
```

### Using Page Objects in Tests

```python
def test_example(page):
    new_page = NewPage(page)
    new_page.fill_name("John Doe")
    new_page.submit_form()
```

## Security Guidelines

### Credentials Management

- **NEVER** commit credentials or secrets to git
- Credentials MUST be in `.env` file (git-ignored)
- Load credentials using `python-dotenv` at runtime
- Use environment variables for CI/CD secrets

### .env File Structure

```dotenv
# Valid user login
TEST_USER_NAME=Your Name
TEST_USER_EMAIL=your-email@example.com
TEST_USER_PASSWORD=your-password

# Payment card details (test values only)
CARD_NAME=Your Name
CARD_NUMBER=4444333322221111
CARD_CVC=000
CARD_EXPIRY_MONTH=12
CARD_EXPIRY_YEAR=2030
```

### test_data.json

- Contains **only non-sensitive** test data
- Invalid credentials for negative tests
- API configuration
- Selectors and test constants

### Required GitHub Secrets

For CI/CD workflows, set these in **Settings → Secrets → Actions**:

- `TEST_USER_NAME`
- `TEST_USER_EMAIL`
- `TEST_USER_PASSWORD`
- `CARD_NAME`
- `CARD_NUMBER`
- `CARD_CVC`
- `CARD_EXPIRY_MONTH`
- `CARD_EXPIRY_YEAR`
- `SLACK_WEBHOOK_URL` (optional)

## CI/CD Workflows

Four GitHub Actions workflows in `.github/workflows/`:

| Workflow                    | Trigger                    | Purpose                                      |
| --------------------------- | -------------------------- | -------------------------------------------- |
| `ci-cd.yml`                 | Push, PR, schedule, manual | Full pipeline with multi-browser testing     |
| `pr-checks.yml`             | Pull request               | Validate commits, smoke tests, coverage gate |
| `scheduled-smoke-tests.yml` | Every 6 hours              | Continuous health monitoring                 |
| `manual-test-run.yml`       | Manual dispatch            | On-demand test runs                          |

**Security:** All GitHub Actions are pinned to commit SHAs for supply-chain security.

## Common Pitfalls & Best Practices

### DO:

✅ Use explicit waits (`wait_for_element()`) instead of `sleep()`
✅ Inherit all page objects from `BasePage`
✅ Add type hints and docstrings to all functions
✅ Use pytest markers to categorize tests
✅ Store test data in `test_data.json`
✅ Run pre-commit hooks before committing
✅ Keep tests atomic and independent
✅ Use meaningful test and method names
✅ Log important test steps
✅ Capture screenshots on failures (automatic)

### DON'T:

❌ Hardcode credentials in test files
❌ Commit `.env` file to git
❌ Use `time.sleep()` for waits
❌ Create page objects without inheriting from `BasePage`
❌ Skip type hints or docstrings
❌ Modify working tests for unrelated issues
❌ Add temporary or debug files to git (use `/tmp`)
❌ Remove or modify unrelated tests
❌ Introduce new dependencies without necessity

## Utilities

### WebUtils (`utils/web_utils.py`)

```python
from utils.web_utils import WebUtils

web_utils = WebUtils(page)
web_utils.wait_and_click("button.save")
web_utils.fill_field("input[name='name']", "John Doe")
text = web_utils.get_element_text("p.error")
web_utils.take_screenshot("test_success")
```

### APIUtils (`utils/api_utils.py`)

```python
from utils.api_utils import APIUtils

api = APIUtils("https://api.example.com")
response = api.get("/products", params={"page": 1})
api.verify_status_code(response, 200)
```

## Adding New Features

### Adding a New Test

1. Create page object in `pages/` (if needed)
2. Add test file in `tests/ui/` or `tests/api/`
3. Use fixtures: `page`, `test_data`
4. Add test data to `test_data.json` if data-driven
5. Add appropriate pytest marker
6. Run test locally before committing

### Adding a New Page Object

1. Create file in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class constants
4. Implement action methods
5. Add type hints and docstrings

### Adding Test Data

1. Edit `test_data/test_data.json`
2. Follow existing JSON structure
3. Use descriptive keys
4. Never add sensitive data

## Debugging

### Capture Traces

```bash
pytest tests/ui/test_login.py -v --trace=retain-on-failure
```

### Screenshots

Automatic screenshots on failures: `./reports/screenshots/failure_test_name_TIMESTAMP.png`

### Logs

Test logs appear in terminal output with INFO level by default.

## Dependencies

Install from `requirements.txt`:

- pytest, pytest-playwright, playwright
- requests (API testing)
- pytest-html, allure-pytest (reporting)
- python-dotenv (environment variables)
- pytest-cov, pytest-xdist (coverage & parallel execution)
- black, flake8, mypy (code quality)

## Questions?

1. Check existing tests for examples
2. Review documentation in `docs/`
3. Check logs in terminal output
4. Review screenshots in `./reports/screenshots/`
5. Run pre-commit hooks to catch issues early

---

**Last Updated:** February 2026
**Playwright Version:** 1.58.0
**Python Version:** 3.14+
