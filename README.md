# automation_playwright_dele

[![Tests Status](https://img.shields.io/badge/tests-maintained-brightgreen)]()
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Playwright Version](https://img.shields.io/badge/playwright-latest-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

A **professional-grade, production-ready Playwright-based test automation framework** for e-commerce testing with comprehensive Page Object Model (POM) architecture, data-driven testing, CI/CD integration and advanced reporting capabilities.

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Running Tests](#-running-tests)
- [Test Organization](#-test-organization)
- [Page Objects](#-page-objects)
- [Utilities](#-utilities)
- [Advanced Features](#-advanced-features)
- [CI/CD Integration](#-cicd-integration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🎯 Features

✅ **Playwright Browser Automation** - Chromium, Firefox, WebKit support  
✅ **Page Object Model (POM)** - Clean, maintainable, reusable test structure  
✅ **Data-Driven Testing** - Parametrized tests with JSON/CSV test data  
✅ **API Testing** - RESTful API integration and endpoint testing  
✅ **Screenshot & Video Capture** - Automatic failure screenshots and optional video recording  
✅ **Consent Banner Handling** - Auto-dismisses cookie and consent modals  
✅ **Pytest Integration** - Comprehensive markers, fixtures, and configuration  
✅ **Test Fixtures** - Reusable browser, page, and test data fixtures  
✅ **Advanced Logging** - Detailed test execution logs with configurable levels  
✅ **Allure Reporting** - Beautiful HTML test reports with trends and analytics  
✅ **Error Handling** - Robust error handling with descriptive error messages  
✅ **Performance Testing** - API response time and page load performance tests

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### 1. Setup Environment

```bash
# Clone repository
git clone <repo-url>
cd automation_playwright_dele

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (required before running tests)
python -m playwright install
```

### 2. Configure Credentials

Credentials are loaded from environment variables (never committed to git).
Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your test account details:

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

Non-sensitive test data (invalid credentials, API config, selectors) lives in `test_data/test_data.json` — no changes needed there.

### 3. Run Tests

```bash
# Run all tests
pytest tests/

# Run only smoke tests (critical path)
pytest tests/ -m smoke

# Run UI tests only
pytest tests/ui/ -v

# Run API tests only
pytest tests/api/ -v

# Run with specific markers
pytest -m "smoke or api" -v

# Run single test file
pytest tests/ui/test_login.py -v

# Run single test
pytest tests/ui/test_login.py::TestLogin::test_valid_login -v

# Run with custom options
pytest tests/ -v --tb=long --capture=no
```

## 📁 Project Structure

```
automation_playwright_dele/
│
├── pages/                          # Page Object Models
│   ├── __init__.py
│   ├── base_page.py               # Base class for all page objects
│   ├── home_page.py               # Home/dashboard page interactions
│   ├── login_page.py              # Login and registration page
│   ├── product_page.py            # Product listing and details
│   └── cart_page.py               # Shopping cart interactions
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and configuration
│   │
│   ├── ui/                         # UI and E2E tests
│   │   ├── test_smoke.py          # Critical path smoke tests
│   │   ├── test_login.py          # Login/auth tests (data-driven)
│   │   ├── test_checkout.py       # Checkout process tests
│   │   └── __init__.py
│   │
│   ├── api/                        # REST API tests
│   │   ├── test_product_api.py    # Product endpoint tests
│   │   └── __init__.py
│   │
│   └── performance/                # Performance tests (future)
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── web_utils.py               # Web automation utilities
│   ├── api_utils.py               # API testing utilities
│   └── helpers/                    # Additional helpers (future)
│
├── test_data/                      # Test data and fixtures
│   ├── test_data.json             # Test credentials and data
│   └── test_data.csv              # Alternative CSV format
│
├── reports/                        # Test execution reports
│   ├── screenshots/               # Failure screenshots
│   ├── videos/                    # Test recordings (optional)
│   ├── test-report.html          # HTML test report
│   └── allure-results/           # Allure report data
│
├── docs/                          # Documentation
│   ├── generate_allure_report.py
│   ├── generate_test_report.py
│   └── *.md                       # Various guides
│
├── .vscode/                       # VS Code configuration
│   ├── settings.json
│   ├── launch.json
│   ├── tasks.json
│   └── extensions.json
│
├── .github/                       # GitHub CI/CD & automation
│   ├── workflows/
│   │   ├── ci-cd.yml              # Main pipeline (push/PR/schedule)
│   │   ├── pr-checks.yml          # PR validation & smoke tests
│   │   ├── scheduled-smoke-tests.yml  # Scheduled health checks
│   │   └── manual-test-run.yml    # On-demand test runs
│   └── dependabot.yml             # Dependency vulnerability scanning
│
├── .env.example                   # Template for credentials (committed)
├── .env                           # Actual credentials (git-ignored)
├── .gitignore
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## ⚙️ Configuration

### Pytest Configuration (pytest.ini)

The `pytest.ini` file contains:

- Test discovery patterns (test file naming)
- Execution options (verbosity, timeout, markers)
- Logging configuration
- Report generation settings

```bash
# Key options:
testpaths = tests              # Where to find tests
python_files = test_*.py       # Test file naming pattern
python_functions = test_*      # Test function naming pattern

# Markers:
@pytest.mark.smoke            # Critical path tests
@pytest.mark.regression       # Full regression suite
@pytest.mark.api              # API tests only
@pytest.mark.ui               # UI tests only
@pytest.mark.slow             # Long-running tests
```

### Browser Configuration

Browser configuration is in `tests/conftest.py`:

- Viewport size: 1920x1080 (adjustable)
- HTTPS error ignoring: Enabled
- Video recording: Disabled by default (can be enabled)

## 🧪 Running Tests

### Common Commands

```bash
# Verbose output with test results
pytest tests/ -v

# Stop on first failure
pytest tests/ -x

# Stop after N failures
pytest tests/ --maxfail=3

# Show print statements
pytest tests/ -v -s

# Only run tests matching pattern
pytest tests/ -k "login"

# Run with specific marker
pytest tests/ -m "smoke"

# Run with HTML report
pytest tests/ --html=reports/test-report.html --self-contained-html

# Run with Allure report
pytest tests/ --alluredir=reports/allure-results

# Run with coverage (requires pytest-cov)
pytest tests/ --cov=pages --cov=utils --cov-report=html

# Show test summary
pytest tests/ -v --tb=short

# Run in parallel (requires pytest-xdist)
pytest tests/ -n auto
```

## 🏗️ Test Organization

### Test Markers

Organize and filter tests using pytest markers:

```python
@pytest.mark.smoke              # Critical path
@pytest.mark.regression         # Full regression
@pytest.mark.api                # API tests
@pytest.mark.ui                 # UI tests
@pytest.mark.login              # Login-specific
@pytest.mark.cart               # Cart-specific
@pytest.mark.checkout           # Checkout-specific
@pytest.mark.slow               # Long-running
@pytest.mark.skip_ci            # Skip in CI/CD
```

### Test Scopes

Tests are organized by scope:

- **Smoke Tests** - Quick critical path tests (5-10 minutes)
- **UI Tests** - Full UI/E2E coverage
- **API Tests** - REST API verification
- **Integration Tests** - Full workflow testing
- **Performance Tests** - Load and stress testing (future)

## 📄 Page Objects

All page objects inherit from `BasePage` and provide:

- Element interaction methods (click, fill, get_text)
- Wait mechanisms (implicit and explicit)
- Error handling and logging
- Screenshot capture

### Creating a New Page Object

```python
from pages.base_page import BasePage
from playwright.sync_api import expect

class YourPage(BasePage):
    """Page Object for your page"""

    # Define locators
    BUTTON_SUBMIT = "button[type='submit']"
    INPUT_EMAIL = "input[name='email']"

    def fill_email(self, email: str) -> None:
        """Fill email field"""
        self.fill(self.INPUT_EMAIL, email)

    def click_submit(self) -> None:
        """Click submit button"""
        self.click(self.BUTTON_SUBMIT)
```

### Using Page Objects in Tests

```python
def test_example(page):
    # Create page object
    your_page = YourPage(page)

    # Use page object methods
    your_page.fill_email("test@example.com")
    your_page.click_submit()
```

## 🛠️ Utilities

### WebUtils

Web automation utilities in `utils/web_utils.py`:

```python
from utils.web_utils import WebUtils

web_utils = WebUtils(page)

# Click with wait
web_utils.wait_and_click("button.save")

# Fill form field
web_utils.fill_field("input[name='name']", "John Doe")

# Get element text
text = web_utils.get_element_text("p.error")

# Check visibility (non-blocking)
if web_utils.is_element_visible("div.success"):
    print("Success!")

# Screenshot
screenshot_path = web_utils.take_screenshot("test_success")

# Scroll to element
web_utils.scroll_to_element("button.checkout")
```

### APIUtils

API testing utilities in `utils/api_utils.py`:

```python
from utils.api_utils import APIUtils

api = APIUtils("https://api.example.com")

# GET request
response = api.get("/products", params={"page": 1})

# POST request
response = api.post("/users", data={"name": "John"})

# Set authentication
api.set_auth_token("your-token")

# Verify status code
api.verify_status_code(response, 200)

# Save response
api.save_response_to_file(response, "response.json")
```

## 🔧 Advanced Features

### Data-Driven Testing

Tests are parametrized from JSON test data:

```python
@pytest.mark.parametrize("user_id,email,password", get_valid_users())
def test_login(page, user_id, email, password):
    # Test runs once per user in test_data.json
    pass
```

### Screenshot Capture

Automatic on failure, manual capture:

```python
# Automatic (in conftest.py)
# Captured on test failure to reports/screenshots/

# Manual capture
page_obj.take_screenshot("custom_name")
```

### Video Recording

Optional video recording (disabled by default):

1. Uncomment in `conftest.py`:

```python
"record_video_dir": "./reports/videos"
```

2. Run tests - videos saved to `reports/videos/`

3. Optional cleanup:

```python
def test_example(cleanup_videos, page):
    # Video deleted if test passes
    pass
```

### Logging

Configure logging level in `pytest.ini` or code:

```python
logger.info("Test starting...")
logger.debug("Debug information")
logger.warning("Warning message")
logger.error("Error occurred")
```

## 🔄 CI/CD Integration

### GitHub Actions

The project includes 4 production-ready workflow files — see the [CI/CD Integration](#-cicd-integration-1) section below for details.

### Jenkins Example

```groovy
pipeline {
    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && python -m playwright install'
            }
        }
        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest tests/ -v --tb=short'
            }
        }
        stage('Report') {
            steps {
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'test-report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
}
```

## 🚀 CI/CD Integration

### GitHub Actions

Four workflow files in `.github/workflows/`:

| Workflow                    | Trigger                    | Purpose                                                             |
| --------------------------- | -------------------------- | ------------------------------------------------------------------- |
| `ci-cd.yml`                 | Push, PR, schedule, manual | Full pipeline: lint → multi-browser test → coverage → Allure report |
| `pr-checks.yml`             | Pull request               | Validate commits, smoke tests, coverage gate (60%)                  |
| `scheduled-smoke-tests.yml` | Every 6 hours              | Continuous health monitoring with Slack alerts                      |
| `manual-test-run.yml`       | Manual dispatch            | On-demand runs with suite/browser/parallel selection                |

All actions are **pinned to commit SHAs** and use **least-privilege permissions**.

## 📊 Reports

### HTML Report

Generate after test run:

```bash
pytest tests/ --html=reports/test-report.html --self-contained-html
```

### Allure Report

```bash
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 🐛 Troubleshooting

### Common Issues

**Playwright browsers not installed:**

```bash
python -m playwright install
```

**Port already in use:**

```bash
# Change browser port in conftest.py if needed
```

**Element not found:**

- Check selector in browser DevTools
- Verify page loaded (check network tab)
- Add explicit waits

**Timeout errors:**

- Increase timeout in BasePage.timeout
- Check internet connectivity
- Verify selectors

**Screenshot/video not captured:**

- Check `reports/` directory permissions
- Ensure directory exists: `os.makedirs("reports/screenshots", exist_ok=True)`

## 📝 Best Practices

1. **DRY Principle** - Use page objects and utilities
2. **Explicit Waits** - Use `wait_for_element()` not `sleep()`
3. **Meaningful Names** - Clear test and method names
4. **One Assert** - One action per test
5. **Test Data** - Externalize in JSON/CSV
6. **Logging** - Log important steps
7. **Error Handling** - Descriptive error messages
8. **Isolation** - Each test independent
9. **Cleanup** - Proper teardown (handled by fixtures)
10. **Documentation** - Docstrings for complex logic

## 🤝 Contributing

1. Follow existing code style
2. Add comprehensive docstrings
3. Update README for new features
4. Test locally before submitting
5. Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues, questions, or suggestions:

1. Check existing issues/documentation
2. Review test logs and screenshots
3. Enable debug logging
4. Check browser/network connectivity

---

## 📊 Test Markers

Markers help organize and run test groups:

```bash
pytest -m smoke              # Critical path tests
pytest -m login              # Authentication tests
pytest -m api                # API tests
pytest -m checkout           # Checkout process tests
pytest -m cart               # Shopping cart tests
pytest -m regression         # Full regression suite
```

## 🧪 Test Coverage

### UI Tests

- **test_smoke.py** - Homepage, registration, cart operations (3 tests)
- **test_login.py** - Data-driven valid/invalid login scenarios (3 parametrized tests)
- **test_checkout.py** - Cart and checkout functionality (4 tests)
- **test_payment.py** - Full order flow: login → browse → checkout → payment → logout (1 test)

### API Tests

- **test_product_api.py** - Product listing and search APIs (4 tests)
- **test_auth_api.py** - Authentication endpoints (8 parametrized tests)
- **test_user_api.py** - User CRUD operations (4 tests)

### Performance Tests

- **test_api_performance.py** - API response time thresholds (4 endpoint tests)
- **test_page_performance.py** - Page load times and CLS metrics (8 parametrized tests)

**Total: 39 tests**

## 🔧 Configuration Files

### pytest.ini

Centralized pytest configuration:

- Test paths and discovery patterns
- Logging and output options
- Test markers definition
- Allure reporting

### conftest.py

Pytest fixtures:

- `browser_context_args` - Browser viewport and settings
- `page` - Auto-navigated Playwright page with consent banner blocked at network level
- `test_data` - Loads non-sensitive config from test_data.json
- `load_dotenv` - Credentials loaded from `.env` before any tests run
- `cleanup_videos` - Optional cleanup fixture

### .pre-commit-config.yaml

Automated code quality hooks:

- Black formatting
- Ruff linting
- Type checking with mypy
- YAML validation

## 📝 Data-Driven Testing

Tests are parameterized using `pytest.parametrize` with data from `test_data.json`:

```python
# test_login.py automatically creates test variations:
# - test_valid_login[valid_user_1]
# - test_invalid_login[invalid_email_password]
# - test_invalid_login[empty_email]
```

Add new test scenarios by updating `test_data.json` - no code changes needed!

## 🛠️ Development Workflow

### Adding New Tests

1. Create page object in `pages/`
2. Add test file in `tests/ui/` or `tests/api/`
3. Use fixtures: `page`, `test_data`
4. Add test data to `test_data.json` if data-driven

### Example Test

```python
import pytest
from pages.home_page import HomePage

class TestNewFeature:
    @pytest.mark.smoke
    def test_feature_works(self, page, test_data):
        """Test description"""
        home_page = HomePage(page)
        # Test implementation
```

### Pre-commit Hooks

```bash
# Install hooks
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Hooks run automatically on git commit
```

## 🐛 Debugging

### Capture Traces

Playwright traces help debug failures:

```bash
python -m pytest tests/ui/test_login.py -v --trace=retain-on-failure
```

Traces save to `.playwright/traces/` for inspection.

### Screenshots

Automatic screenshots on failures:

```
./reports/screenshots/failure_test_name_TIMESTAMP.png
```

### Logs

Test logs in terminal output:

```
tests/ui/test_login.py::TestLogin::test_valid_login - Test execution logs
```

## 📊 Reports

### HTML Report

```bash
python -m pytest tests/ -v --html=reports/test-report.html
```

### Allure Report

```bash
python -m pytest tests/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

## ✅ Quality Standards

- ✅ All tests passing (39 tests)
- ✅ Type hints on all functions
- ✅ Docstrings on all classes/methods
- ✅ Error handling with meaningful messages
- ✅ Logging throughout test execution
- ✅ Code formatted with Black
- ✅ Linted with Ruff
- ✅ Pre-commit hooks enabled

## 📦 Dependencies

| Package           | Version | Purpose               |
| ----------------- | ------- | --------------------- |
| pytest            | 8.4.0   | Test framework        |
| playwright        | 1.58.0  | Browser automation    |
| pytest-playwright | 0.7.2   | Pytest integration    |
| python-dotenv     | 1.2.1   | Load .env credentials |
| allure-pytest     | 2.13.5  | Advanced reporting    |
| requests          | 2.32.3  | HTTP requests         |
| pytest-html       | 4.1.1   | HTML reports          |

## 🔐 Security

- **Credentials in `.env`** — loaded via `python-dotenv` at runtime; `.env` is git-ignored
- **CI/CD secrets** — `TEST_USER_*` and `CARD_*` vars are set as GitHub repository secrets
- **No secrets in committed files** — `test_data.json` contains only non-sensitive test data
- **GitHub Actions pinned to commit SHAs** — prevents supply-chain attacks from mutable tags
- **Least-privilege CI permissions** — each job declares only the permissions it needs
- **Dependabot enabled** — weekly vulnerability scanning for pip packages and GitHub Actions
- HTTPS errors ignored only in test context (`ignore_https_errors: True`)

### Required Repository Secrets

Set these in **Settings → Secrets → Actions**:

| Secret               | Purpose                                 |
| -------------------- | --------------------------------------- |
| `TEST_USER_NAME`     | Valid test account name                 |
| `TEST_USER_EMAIL`    | Valid test account email                |
| `TEST_USER_PASSWORD` | Valid test account password             |
| `CARD_NAME`          | Payment card name                       |
| `CARD_NUMBER`        | Payment card number                     |
| `CARD_CVC`           | Payment card CVC                        |
| `CARD_EXPIRY_MONTH`  | Payment card expiry month               |
| `CARD_EXPIRY_YEAR`   | Payment card expiry year                |
| `SLACK_WEBHOOK_URL`  | _(optional)_ Slack notification webhook |

## 📞 Support

For issues or questions:

1. Check logs in terminal output
2. Review screenshots in `./reports/screenshots/`
3. Capture Playwright trace with `--trace=on`
4. Check `.pre-commit-config.yaml` for code quality

## 📄 License

MIT License

## 👨‍💻 Contributing

1. Follow POM pattern for new pages
2. Add docstrings and type hints
3. Keep tests atomic and independent
4. Add test data instead of hardcoding
5. Run pre-commit hooks before commit

---

**Last Updated:** February 11, 2026  
**Playwright Version:** 1.58.0  
**Python Version:** 3.14+
