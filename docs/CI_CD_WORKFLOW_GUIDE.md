# Comprehensive CI/CD Setup and GitHub Workflow Processing Guide

**Project:** Playwright Automation Framework
**Date:** February 9, 2026
**Version:** 1.0

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [GitHub Configuration](#github-configuration)
5. [Workflow Descriptions](#workflow-descriptions)
6. [Workflow Triggers](#workflow-triggers)
7. [Manual Workflow Execution](#manual-workflow-execution)
8. [Reports and Artifacts](#reports-and-artifacts)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Overview

### What is CI/CD?

**Continuous Integration (CI):** Automatically build, test, and validate code on every push
**Continuous Deployment (CD):** Automatically deploy validated code to production

### Your GitHub Actions Setup

Your project includes **4 automated workflows**:

| Workflow                     | Trigger                    | Purpose                      | Jobs |
| ---------------------------- | -------------------------- | ---------------------------- | ---- |
| **Test Automation Pipeline** | Push, PR, Schedule, Manual | Main CI/CD pipeline          | 5    |
| **Pull Request Checks**      | PR events                  | Validate PRs before merge    | 5    |
| **Scheduled Smoke Tests**    | Cron schedule              | Continuous health monitoring | 3    |
| **Manual Test Run**          | Manual dispatch            | On-demand flexible testing   | 3    |

**Total:** 4 workflows, 16 automated jobs, comprehensive testing across 3 browsers

---

## Prerequisites

### Required

- ✅ Python 3.11+
- ✅ Git installed and configured
- ✅ GitHub repository access with admin permissions
- ✅ Playwright browsers installed (`playwright install`)

### Recommended

- 📦 Virtual environment configured
- 🔑 GitHub personal access token (for CLI)
- 💬 Slack webhook URL (for notifications)
- 📊 Codecov account (for coverage tracking)

### Dependencies

All dependencies are in `requirements.txt`:

```bash
pytest==9.0.2
pytest-playwright==0.7.2
playwright==1.58.0
allure-pytest==2.15.3
pytest-html==4.2.0
pytest-cov==7.0.0
black==26.1.0
flake8==7.3.0
isort==7.0.0
```

---

## Initial Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/thompsonoloko-droid/automation_playwright_dele.git
cd automation_playwright_dele
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers

```bash
playwright install
```

### Step 5: Verify Installation

```bash
# Run a quick test
pytest tests/ui/test_smoke.py -v --browser=chromium

# Check playwright
playwright --version
```

---

## GitHub Configuration

### Step 1: Add Repository Secrets

Secrets allow workflows to securely access sensitive information.

**Location:** Repository → Settings → Secrets and variables → Actions

**Add these secrets:**

#### 1. **SLACK_WEBHOOK_URL** (Optional - for notifications)

- **What it is:** URL to post test results to Slack
- **Where to get:**
  1. Go to Slack workspace settings
  2. Create incoming webhook
  3. Copy the URL
- **Format:** `https://hooks.slack.com/services/...`

#### 2. **BASE_URL_STAGING** (Optional - test environment)

- **What it is:** Base URL for staging environment
- **Example:** `https://staging.example.com`
- **Default:** `https://automationexercise.com`

#### 3. **BASE_URL_PRODUCTION** (Optional - production URL)

- **What it is:** Base URL for production environment
- **Example:** `https://example.com`

#### 4. **CODECOV_TOKEN** (Optional - code coverage)

- **What it is:** Token for Codecov.io integration
- **Where to get:**
  1. Create account at codecov.io
  2. Connect your GitHub repository
  3. Copy the token

### Step 2: Enable GitHub Pages

**Location:** Repository → Settings → Pages

**Configuration:**

1. **Source:** Deploy from a branch
2. **Branch:** `gh-pages`
3. **Folder:** `/ (root)`
4. Click **Save**

This deploys your Allure reports to: `https://thompsonoloko-droid.github.io/automation_playwright_dele`

### Step 3: Create Branch Protection Rules

**Location:** Repository → Settings → Branches → Add rule

**Rule for `main` branch:**

```
Pattern: main
☑ Require pull request reviews before merging
☑ Require status checks to pass before merging
☑ Require branches to be up to date before merging
☑ Dismiss stale pull request approvals when new commits are pushed
```

**Status checks to require:**

- ✅ Test Results (chromium)
- ✅ Test Results (firefox)
- ✅ Test Results (webkit)
- ✅ Code Coverage Report
- ✅ Code Quality

---

## Workflow Descriptions

### 1. Test Automation Pipeline (ci-cd.yml)

**Purpose:** Main CI/CD pipeline for comprehensive testing
**File:** `.github/workflows/ci-cd.yml`

#### Triggers

- ✅ Push to `main` or `develop` branches
- ✅ Pull requests to `main` branch
- ✅ Daily at 8 AM UTC (cron schedule)
- ✅ Manual dispatch (with optional test suite input)

#### Jobs (5 total)

**Job 1: Lint and Quality**

- Runs code formatters and linters
- Tools: black, flake8, isort
- Status: Must pass for pipeline to continue

**Job 2: Test Suite (Multi-browser Matrix)**

- Runs tests on 3 browsers in parallel:
  - Chromium ✓
  - Firefox ✓
  - WebKit ✓
- Test types:
  - Smoke tests (critical path)
  - Regression tests (full suite)
  - API tests (backend validation)
- Reports: HTML, JUnit XML, Allure
- Timeout: 25 minutes per browser

**Job 3: Code Coverage Report**

- Measures test coverage
- Minimum threshold: 60%
- Uploads to Codecov.io
- Generates detailed HTML report

**Job 4: Allure Report**

- Aggregates results from all browsers
- Generates interactive dashboard
- Deploys to GitHub Pages
- Maintains last 10 report history

**Job 5: Notifications**

- Sends Slack message (if configured)
- Creates GitHub issue on failure
- Posts PR comments with results

#### Artifacts Generated

- 📊 HTML reports (per browser)
- 📋 JUnit XML reports
- 📈 Coverage HTML dashboard
- 📸 Screenshots on failure
- 🎬 Video recordings (optional)

#### Duration

- **Lint check:** 1-2 minutes
- **Test execution (parallel):** 10-15 minutes
- **Report generation:** 2-3 minutes
- **Total:** 15-20 minutes

---

### 2. Pull Request Checks (pr-checks.yml)

**Purpose:** Validate PRs before merge to main
**File:** `.github/workflows/pr-checks.yml`

#### Triggers

- ✅ PR opened, synchronized, or reopened
- ✅ Targets: `main` or `develop` branches

#### Jobs (5 total)

**Job 1: Validate**

- Checks commit message format (conventional commits)
- Detects sensitive files (.env, secrets, credentials)
- Blocks PR if sensitive files detected

**Job 2: Smoke Test**

- Runs smoke tests on Chromium only
- Fast feedback (~3-5 minutes)
- Quick validation before deeper testing

**Job 3: Coverage Check**

- Ensures tests cover 60%+ of code
- Fails if coverage drops below threshold
- Uploads to Codecov

**Job 4: Code Quality**

- Runs black (formatting)
- Runs flake8 (linting)
- Runs isort (import sorting)
- Non-blocking (issues reported but don't fail)

**Job 5: Summary**

- Posts quality report as PR comment
- Shows pass/fail status for each check
- Provides quick feedback to developer

#### Concurrency Control

- ❌ Cancels previous PR checks on new commit
- Prevents wasting resources on old checks

#### Duration

- **Total:** 8-12 minutes per PR

---

### 3. Scheduled Smoke Tests (scheduled-smoke-tests.yml)

**Purpose:** Continuous health monitoring of application
**File:** `.github/workflows/scheduled-smoke-tests.yml`

#### Triggers

- ✅ Every 6 hours (4x per day)
- ✅ Daily at 9 PM UTC (morning report)
- ✅ Manual dispatch (override environment)

#### Jobs (3 total)

**Job 1: Smoke Tests**

- Browsers: Chromium, Firefox (parallel)
- Retry policy: 2 automatic retries
- Retry delay: 5 seconds between attempts
- Timeout: 30 seconds per test (prevents hangs)
- Purpose: Detect flaky tests and environment issues

**Job 2: Slack Notification**

- Sends test results to Slack
- Includes pass/fail status
- Links to full details in GitHub Actions

**Job 3: Report Summary**

- Generates summary for GitHub Actions UI
- Shows dates, status, test count
- Available in email notifications

#### Artifacts

- 📊 HTML reports (7-day retention)
- 📋 JUnit results
- 📊 Allure results

#### Duration

- **Per run:** 8-10 minutes

#### Benefits

- 🔍 Catches flaky tests early
- 📊 Monitors environment health
- 🚨 Alerts team to issues
- 📈 Provides historical trend data

---

### 4. Manual Test Run (manual-test-run.yml)

**Purpose:** Flexible on-demand test execution
**File:** `.github/workflows/manual-test-run.yml`

#### Triggers

- ✅ Manual dispatch only (from GitHub UI)

#### Configurable Inputs

| Input          | Options                                             | Default | Purpose                           |
| -------------- | --------------------------------------------------- | ------- | --------------------------------- |
| **test_suite** | all, smoke, regression, api, ui-only, high-priority | -       | Which tests to run                |
| **browser**    | chromium, firefox, webkit, all-browsers             | -       | Browser selection                 |
| **parallel**   | true, false                                         | true    | Enable/disable parallel execution |
| **retry**      | 0, 1, 2, 3                                          | 1       | Auto-retry count                  |
| **headless**   | true, false                                         | true    | Run headless or with UI           |
| **slug**       | staging, production                                 | staging | Target environment                |

#### Jobs (3 total)

**Job 1: Run Tests**

- Dynamically builds pytest command
- Executes based on selected inputs
- Generates all report types
- Timeout: 60 minutes

**Job 2: Generate Report**

- Downloads and merges all artifacts
- Creates consolidated report
- Organizes results

**Job 3: Notify**

- Posts Slack notification (if configured)
- Includes test results summary

#### Duration

- **Smoke (single browser):** 3-5 minutes
- **All tests (single browser):** 10-15 minutes
- **All tests (all browsers):** 30-45 minutes

#### Common Use Cases

**Quick Smoke Test:**

```
Suite: smoke
Browser: chromium
Parallel: true
Retries: 1
Headless: true
```

⏱️ ~3 minutes

**Debug with Browser:**

```
Suite: smoke
Browser: chromium
Parallel: false
Retries: 0
Headless: false  ← See browser UI
```

**Full Regression on All Browsers:**

```
Suite: regression
Browser: all-browsers
Parallel: true
Retries: 2
Headless: true
```

⏱️ ~30 minutes

---

## Workflow Triggers

### Automatic Triggers

#### 1. Push Events

- **When:** Code pushed to `main` or `develop`
- **What runs:** ci-cd.yml (full pipeline)
- **Status checks:** Posted to commit

#### 2. Pull Request Events

- **When:** PR created, updated, or reopened
- **What runs:** pr-checks.yml (validation)
- **Status checks:** Posted to PR
- **Comments:** Quality report auto-posted

#### 3. Schedule Events (Cron)

**ci-cd.yml:**

```
0 8 * * *  Daily at 8 AM UTC
```

**scheduled-smoke-tests.yml:**

```
0 */6 * * *  Every 6 hours
0 21 * * *   Daily at 9 PM UTC
```

---

## Manual Workflow Execution

### Method 1: GitHub Web UI (Recommended)

#### Step 1: Go to Actions

1. Open repository on GitHub
2. Click **Actions** tab at top
3. See all workflows listed on left sidebar

#### Step 2: Select Workflow

- Click workflow you want to run
- Available workflows:
  - Manual Test Run ⭐
  - Test Automation Pipeline
  - Scheduled Smoke Tests

#### Step 3: Click "Run Workflow"

1. Click **Run workflow** dropdown
2. Configure inputs (varies by workflow)
3. Click **Run workflow** button (green)

#### Step 4: Monitor Execution

1. New run appears at top of list
2. Click to see detailed logs
3. Watch each job and step execute
4. See real-time output

#### Step 5: View Results

1. Scroll to **Artifacts** section
2. Download reports
3. View job summary

### Method 2: GitHub CLI

#### Install GitHub CLI

```bash
# Install: https://cli.github.com/
gh --version
```

#### Authenticate

```bash
gh auth login
```

#### List Workflows

```bash
gh workflow list
```

#### Trigger Manual Test Run

```bash
gh workflow run manual-test-run.yml \
  -f test_suite=smoke \
  -f browser=chromium \
  -f parallel=true \
  -f retry=1 \
  -f headless=true \
  -f slug=staging
```

#### Watch Execution

```bash
gh run watch
```

---

## Reports and Artifacts

### Report Types Generated

#### 1. HTML Test Reports

- **Format:** Self-contained HTML file
- **Contains:**
  - Test execution timeline
  - Pass/fail status for each test
  - Error messages and stack traces
  - Screenshots on failure
  - Test metrics and duration
- **Accessible:** Offline (no dependencies)
- **File:** `reports/smoke-chromium.html`

#### 2. JUnit XML Reports

- **Format:** Machine-readable XML
- **Purpose:** Integration with other tools
- **Used by:** GitHub Actions status checks
- **File:** `reports/junit-smoke-chromium.xml`

#### 3. Allure Reports

- **Format:** Interactive dashboard
- **Deployment:** GitHub Pages
- **URL:** `https://thompsonoloko-droid.github.io/automation_playwright_dele`
- **Features:**
  - Organized by test suite and browser
  - Execution timeline
  - Failure analysis
  - Test trends (last 10 runs)
  - Artifacts and attachments

#### 4. Coverage Reports

- **Format:** HTML dashboard
- **Shows:** Code coverage percentage
- **Metrics:** Lines, branches, functions covered
- **Integration:** Codecov.io
- **File:** `coverage-html/index.html`

#### 5. Screenshots & Videos

- **Screenshots:** Captured on test failure
- **Videos:** Recorded test execution (optional)
- **Location:** `reports/screenshots/`, `reports/videos/`
- **Purpose:** Visual debugging

### Accessing Artifacts

#### During Workflow Run

1. Go to Actions → Select run
2. Scroll to **Artifacts** section
3. Click artifact name to download
4. Extract ZIP file locally

#### Artifact Retention

- **Default:** 30 days
- **Smoke tests:** 7 days
- **Final reports:** 30 days

#### Artifact Structure

```
test-reports-chromium.zip
├── reports/
│   ├── smoke-chromium.html
│   ├── junit-smoke-chromium.xml
│   ├── allure-results/
│   └── screenshots/
└── logs/
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Unable to locate package libgconf-2-4"

**Cause:** Deprecated package in modern Ubuntu
**Solution:** Already fixed in ci-cd.yml
**Verify:** Check line has `sudo apt-get update` only

#### Issue 2: "Could not find a version that satisfies requirement"

**Cause:** Invalid package version in requirements.txt
**Symptoms:** Workflow fails during dependency installation
**Solution:**

```bash
# Check available versions
pip index versions pytest-playwright

# Update requirements.txt with correct version
pip install -r requirements.txt --dry-run
```

**Already Fixed:**

- ✅ pytest-playwright==0.7.2 (was 0.8.0 - doesn't exist)
- ✅ mypy==1.19.1 (was 1.20.0 - doesn't exist)

#### Issue 3: "YAML syntax error on line X"

**Cause:** Invalid YAML formatting
**Solution:**

- No inline comments after array values
- Proper indentation (2 spaces)
- Use `|` for multiline strings

**Check:** Run locally with `yamllint`

#### Issue 4: "Invalid action input 'webhook-url'"

**Cause:** Outdated linter warning (false positive)
**Solution:** Ignore - it's not actually an error
**Note:** GitHub Actions executes successfully despite warning

#### Issue 5: Workflow timeout

**Cause:** Tests taking longer than timeout
**Solutions:**

1. Run smoke tests instead of full suite
2. Enable parallel execution
3. Increase timeout (currently 60 minutes)
4. Check for hanging tests

```bash
# Debug: Run locally with timeout
pytest tests/ --timeout=30 -v
```

#### Issue 6: "No files found" warnings

**Cause:** Looking for files in wrong directory
**Solution:** Already fixed in ci-cd.yml

- ✅ Changed from `junit-combined/*.xml` to `junit-*.xml`
- Tests generate files directly in `reports/` directory

#### Issue 7: Code formatting failures

**Cause:** Black formatter finding formatting issues
**Solution:** Already fixed in ci-cd.yml

- ✅ Changed from `black --check` to auto-format mode
- Workflow now automatically formats files

### Debug Workflow Failures

#### Step 1: Review Logs

1. Go to failed workflow run
2. Click failed job
3. Expand each step to see output
4. Look for error messages

#### Step 2: Check Common Causes

- 🔍 Python version mismatch
- 📦 Missing dependencies
- 🌐 Network/connectivity issues
- ⏱️ Timeout exceeded
- 📝 File encoding issues

#### Step 3: Run Locally

```bash
# Reproduce issue locally first
pytest tests/ui/test_smoke.py -v --browser=chromium

# Check specific step
python -m black tests/ --check
python -m pytest --cov=pages,utils tests/
```

#### Step 4: Check Secrets & Variables

1. Go to Settings → Secrets and variables
2. Verify all secrets are configured
3. Check if secret is used in workflow
4. Ensure correct environment references

---

## Best Practices

### Git and Commit Workflow

#### 1. Use Conventional Commits

```
Format: type(scope): message

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructure
- perf: Performance improvement
- test: Test addition/modification
- chore: Build, CI, dependencies

Examples:
✅ feat(tests): add new login scenarios
✅ fix(ui): resolve dropdown selector
✅ docs(readme): update setup instructions
❌ fixed stuff
❌ changes
```

#### 2. Create Feature Branches

```bash
git checkout -b feature/add-checkout-tests
# Make changes
git add .
git commit -m "feat(checkout): add payment flow tests"
git push origin feature/add-checkout-tests
# Create PR on GitHub
```

#### 3. Keep Commits Atomic

- One feature per commit
- One fix per commit
- Logical grouping of changes

### Test Development

#### 1. Write Tests Incrementally

```python
# ✅ Good: Small, focused test
def test_user_login_with_valid_credentials(page):
    """Test successful login with correct credentials"""
    # Arrange, Act, Assert

# ❌ Bad: Testing multiple scenarios
def test_login_and_checkout_and_logout(page):
    """Test entire user flow"""
```

#### 2. Use Page Object Model

```python
# ✅ Good: Encapsulated page logic
from pages.login_page import LoginPage

def test_login(page):
    login = LoginPage(page)
    login.login("user@example.com", "password")
    assert login.is_logged_in()
```

#### 3. Add Markers for Organization

```python
@pytest.mark.smoke
@pytest.mark.login
def test_valid_login(page):
    pass

# Run specific marker
pytest tests/ -m smoke
```

### Workflow Monitoring

#### 1. Regular Check Schedule

- **Daily:** Check Scheduled Smoke Tests results
- **Per PR:** Monitor PR Check status
- **Weekly:** Review test trends in Allure
- **Monthly:** Analyze coverage trends

#### 2. Set Up Notifications

- 🔔 Watch scheduled test runs
- 📧 Review PR status checks
- 💬 Configure Slack alerts
- 📊 Monitor coverage dashboard

#### 3. Handle Failures

- 🚨 Address failures within 24 hours
- 🔍 Investigate root cause
- 🔄 Re-run to rule out flakiness
- 📝 Update tests if code changed

### Performance Optimization

#### 1. Reduce Test Execution Time

- ⚡ Use smoke tests for quick feedback
- 🔀 Enable parallel execution
- 🎯 Focus on critical path tests
- 🏷️ Use markers to organize tests

#### 2. Optimize Workflows

```yaml
# ✅ Use matrix for parallel execution
strategy:
  matrix:
    browser: [chromium, firefox, webkit]

# ✅ Cache dependencies
uses: actions/setup-python@v4
with:
  cache: "pip"

# ✅ Fail fast on critical issues
strategy:
  fail-fast: true
```

#### 3. Report Generation

- 📊 Limit Allure history (keep last 10)
- 🗑️ Auto-clean old artifacts (7-30 days)
- 📦 Use `--self-contained-html` for portability

### Security Best Practices

#### 1. Protect Secrets

- ✅ Use repository secrets for sensitive data
- ❌ Never commit .env files
- ✅ Rotate secrets regularly
- ✅ Limit secret scope

#### 2. Code Review Before Merge

- ✅ Require PR reviews
- ✅ Check PR status passes
- ✅ Review code changes carefully
- ✅ Never force-push to main

#### 3. Branch Protection

- ✅ Enable for `main` branch
- ✅ Require status checks pass
- ✅ Require PR before merge
- ✅ Dismiss stale reviews

---

## Quick Reference

### Essential Commands

```bash
# Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install

# Run tests locally
pytest tests/ -v
pytest tests/ui/ -m smoke
pytest tests/ --browser=firefox

# Code quality
black .
flake8 tests/ pages/ utils/
isort .

# Clean up
deactivate
rm -rf .venv
```

### Workflow Configuration Paths

| Component       | Path                                          |
| --------------- | --------------------------------------------- |
| Main CI/CD      | `.github/workflows/ci-cd.yml`                 |
| PR Checks       | `.github/workflows/pr-checks.yml`             |
| Scheduled Tests | `.github/workflows/scheduled-smoke-tests.yml` |
| Manual Tests    | `.github/workflows/manual-test-run.yml`       |
| Requirements    | `requirements.txt`                            |
| Pytest Config   | `pytest.ini`                                  |
| Test Code       | `tests/`                                      |
| Page Objects    | `pages/`                                      |
| Utilities       | `utils/`                                      |

### URLs

| Resource       | URL                                                                       |
| -------------- | ------------------------------------------------------------------------- |
| Repository     | https://github.com/thompsonoloko-droid/automation_playwright_dele         |
| Actions        | https://github.com/thompsonoloko-droid/automation_playwright_dele/actions |
| Allure Reports | https://thompsonoloko-droid.github.io/automation_playwright_dele          |
| Codecov        | https://codecov.io/gh/thompsonoloko-droid/automation_playwright_dele      |

---

## Support & Resources

### Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Playwright Documentation](https://playwright.dev)
- [Pytest Documentation](https://docs.pytest.org)
- [Allure Documentation](https://docs.qameta.io/allure)

### Helpful Guides

- [Conventional Commits](https://www.conventionalcommits.org)
- [GitHub Flow](https://guides.github.com/introduction/flow)
- [Page Object Model](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models)

### Community

- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions and share ideas
- Playwright Discord: Get help from community

---

## Conclusion

You now have a **professional-grade CI/CD pipeline** that:

- ✅ Automatically tests on every push and PR
- ✅ Validates code quality and style
- ✅ Measures code coverage
- ✅ Continuously monitors application health
- ✅ Generates comprehensive reports
- ✅ Supports manual on-demand testing
- ✅ Notifies team of failures

**Next Steps:**

1. Configure GitHub secrets (Slack, Codecov)
2. Enable GitHub Pages for Allure reports
3. Set up branch protection rules
4. Run your first manual test
5. Monitor scheduled test results

**Happy Testing! 🚀**
