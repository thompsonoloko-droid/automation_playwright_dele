# Test Report Generation Guide

## Overview

This project includes multiple ways to generate and view test reports:

1. **HTML Test Report** - Professional dashboard with test information
2. **Pytest JSON Report** - Machine-readable test results
3. **Allure Reports** (optional) - Advanced interactive test reporting
4. **VS Code Test Explorer** - Built-in test discovery and execution

---

## Quick Start

### Generate HTML Report

```bash
python generate_test_report.py
```

This will:

- ✓ Run all API tests
- ✓ Generate an HTML report with test information
- ✓ Open the report in your default browser

### Run Tests Only

```bash
python -m pytest tests/ -v
```

### Run Tests with HTML Report (pytest-html)

```bash
python -m pytest tests/ --html=reports/report.html --self-contained-html
```

---

## Report Generation Scripts

### `generate_test_report.py`

**Purpose:** Generate a professional HTML test report dashboard

**Features:**

- Beautiful, responsive UI
- Project overview and statistics
- Test category information
- Command reference for running tests
- Project structure visualization
- Next steps guidance

**Usage:**

```bash
python generate_test_report.py
```

**Output:**

- `reports/test-report.html` - Main report file
- Automatically opens in default browser

### `generate_allure_report.py`

**Purpose:** Generate Allure interactive test reports (requires Allure CLI)

**Features:**

- Interactive HTML report viewer
- Test timeline and history
- Failure analysis
- Object repository
- Retry history

**Prerequisites:**

```bash
# Install Allure CLI
# On Windows (Chocolatey):
choco install allure

# On macOS:
brew install allure

# On Linux:
sudo apt-get install allure
```

**Usage:**

```bash
# After running tests with allure reporting
python generate_allure_report.py
```

---

## Running Tests with Reports

### Option 1: Using VS Code Tasks

Press `Ctrl+Shift+B` and select:

- "Run All Tests" - Run tests only
- "Run UI Tests" - Run UI test suite
- "Run API Tests" - Run API test suite
- "Run Smoke Tests" - Run smoke test markers
- "Generate Test Report" - Create HTML report

### Option 2: Using Command Line

```bash
# Run all tests
python -m pytest tests/ -v

# Run by category
python -m pytest tests/api/ -v        # API tests only
python -m pytest tests/ui/ -v         # UI tests only

# Run by marker
python -m pytest tests/ -m smoke -v   # Smoke tests only
python -m pytest tests/ -m api -v     # API marked tests
```

### Option 3: Using VS Code Test Explorer

1. Click the Test Flask icon in the left sidebar
2. Browse your test hierarchy
3. Click ▶ next to any test to run it
4. Right-click for more options (debug, run with settings, etc.)

---

## Report Locations

```
reports/
├── test-report.html          ← Main HTML report
├── report.html              ← pytest-html report (if generated)
├── api-report.json          ← JSON report for API tests
├── allure-results/          ← Allure JSON results (if available)
├── allure-report/           ← Allure HTML report (if generated)
├── screenshots/             ← Test failure screenshots
├── videos/                  ← Test recordings
└── allure-results/          ← Allure results data
```

---

## Setting Up Allure Reports (Optional)

### Step 1: Install Allure CLI

**Windows (Chocolatey):**

```powershell
choco install allure
```

**macOS:**

```bash
brew install allure
```

**Linux:**

```bash
sudo apt-get install allure
```

### Step 2: Run Tests with Allure

```bash
python -m pytest tests/ --alluredir=reports/allure-results -v
```

### Step 3: Generate Allure Report

```bash
python generate_allure_report.py
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Reports

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install -r requirements.txt
          python -m playwright install

      - name: Run tests
        run: python -m pytest tests/ --html=reports/report.html --self-contained-html

      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: reports/
```

---

## Interpreting Test Reports

### HTML Report Dashboard

- **Project Overview:** Framework, test runner, and generation timestamp
- **Test Suite Information:** Statistics on total, API, and UI tests
- **How to Run Tests:** Command reference for different test scenarios
- **Project Structure:** Visual representation of directory organization
- **Next Steps:** Recommended actions after reviewing the report

### Understanding Test Results

- ✓ **Passed** - Test executed successfully
- ✗ **Failed** - Test did not meet assertions
- ⊘ **Skipped** - Test was intentionally skipped
- ⚠ **Error** - Test setup/teardown failed

---

## Troubleshooting Report Generation

### Issue: "allure command not found"

**Solution:** Install Allure CLI (see "Setting Up Allure Reports" above)

### Issue: No test results in report

**Solution:** Run tests first with `python -m pytest tests/ -v`

### Issue: Report not opening in browser

**Solution:** Manually open the report file:

```bash
# Open with default browser
python -c "import webbrowser; webbrowser.open('reports/test-report.html')"
```

### Issue: "allure-pytest" not installed

**Solution:** Install the package:

```bash
python -m pip install allure-pytest
```

---

## Best Practices

1. **Always run tests before generating reports**

   ```bash
   python -m pytest tests/ -v
   python generate_test_report.py
   ```

2. **Use meaningful test markers**
   - `@pytest.mark.smoke` - Critical path tests
   - `@pytest.mark.api` - API integration tests
   - `@pytest.mark.checkout` - Checkout flow tests

3. **Capture failures with screenshots**
   - Tests automatically capture screenshots on failure
   - Located in `reports/screenshots/`

4. **Version control reports**
   - Add `reports/` to `.gitignore`
   - Keep reports separate from source code

5. **Review reports regularly**
   - Monitor test trends over time
   - Identify flaky tests that need investigation

---

## Advanced Options

### Custom Report Generation

Modify `generate_test_report.py` to:

- Change styling and branding
- Add custom metrics
- Integrate with external systems
- Generate PDF reports

### Performance Profiling

Add test performance metrics:

```bash
python -m pytest tests/ --durations=10
```

### Test Coverage Analysis

Generate coverage reports:

```bash
pip install pytest-cov
python -m pytest tests/ --cov=pages --cov-report=html
```

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-html Plugin](https://pytest-html.readthedocs.io/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [Playwright Testing](https://playwright.dev/python/docs/intro)

---

## Summary

- 📊 **HTML Reports** - Use `generate_test_report.py` for quick dashboards
- 🧪 **Test Execution** - Use `pytest` from command line or VS Code
- 🎯 **Test Discovery** - Use VS Code Test Explorer for visual interface
- 🔍 **Allure Reports** - Use for advanced failure analysis and trends (optional)

Choose the report format that best fits your workflow!
