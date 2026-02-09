# GitHub Actions CI/CD Integration Guide

Complete setup and usage guide for integrating your Playwright automation project with GitHub CI/CD pipelines.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Workflow Files](#workflow-files)
3. [GitHub Secrets Setup](#github-secrets-setup)
4. [Branch Protection Rules](#branch-protection-rules)
5. [GitHub Pages Setup](#github-pages-setup)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Repository Setup

- ✅ Your project is already in a GitHub repository
- ✅ `main` and `develop` branches are protected
- ✅ `.github/workflows/` directory exists with workflow files

### 2. Required Permissions

Ensure your GitHub account has:

- Admin access to the repository
- Ability to create secrets
- Ability to enable GitHub Pages
- Ability to create branch protection rules

---

## Workflow Files

### Available Workflows

#### 1. **ci-cd.yml** - Main CI/CD Pipeline

**Trigger Events:**

- Push to `main` or `develop` branches
- Pull requests to `main` branch
- Daily schedule at 8 AM UTC
- Manual trigger via GitHub UI

**Jobs:**

- `lint-and-quality` - Code quality checks (black, flake8, isort)
- `test` - Run tests across 3 browsers (Chromium, Firefox, WebKit)
- `coverage` - Generate and upload code coverage reports
- `allure-report` - Generate Allure test reports
- `notify` - Send Slack notifications and create issues

**Reports Generated:**

- HTML test reports
- JUnit XML results
- Coverage reports
- Allure reports (deployed to GitHub Pages)

---

#### 2. **pr-checks.yml** - Pull Request Validation

**Trigger Events:**

- Pull request opened/updated/reopened on `main` or `develop`

**Jobs:**

- `validate` - Check commit messages and sensitive files
- `smoke-test` - Run smoke tests on PR changes
- `test-coverage` - Verify minimum coverage threshold
- `code-quality` - Format and lint checks
- `summary` - Post automated PR review as comment

**PR Requirements:**

- All smoke tests must pass
- Code coverage ≥ 60%
- Conventional commit format
- No sensitive files detected

---

#### 3. **scheduled-smoke-tests.yml** - Automated Smoke Tests

**Trigger Events:**

- Every 6 hours (production health check)
- Daily at 9 PM (night report)
- Manual trigger with environment selection

**Browsers Tested:**

- Chromium
- Firefox

**Features:**

- Auto-retry flaky tests (2 retries with 5-second delay)
- Slack notifications
- Summary report generation

---

#### 4. **manual-test-run.yml** - On-Demand Test Execution

**Manual Trigger Options:**

```yaml
Test Suite:
  - all (full test suite)
  - smoke (quick sanity check)
  - regression (full regression)
  - api (API tests only)
  - ui-only (UI/E2E tests)
  - high-priority (smoke + API)

Browser:
  - chromium
  - firefox
  - webkit
  - all-browsers (run all 3)

Parallel Execution: true/false
Retry Count: 0, 1, 2, 3
Headless Mode: true/false
Environment: staging/production
```

---

## GitHub Secrets Setup

### Required Secrets

Add these secrets to your GitHub repository:

1. **GitHub Repository Settings → Secrets and variables → Actions**

```
Secrets to Create:
├── SLACK_WEBHOOK_URL (Optional)
│   └── For Slack notifications
│       Format: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
│
├── CODECOV_TOKEN (Optional)
│   └── For Codecov coverage reporting
│       Get from: https://codecov.io
│
├── BASE_URL_STAGING
│   └── Staging environment URL
│       Value: https://automationexercise.com (or your staging URL)
│
└── BASE_URL_PRODUCTION
    └── Production environment URL
        Value: https://automationexercise.com
```

### Environment Variables

Set in workflow files or .env:

```bash
PYTHONPATH=${WORKSPACE}
HEADLESS=true
TIMEOUT=30000
BROWSER=chromium
PARALLEL_TESTS=true
RETRY_COUNT=1
```

---

## Branch Protection Rules

### Setup Branch Protection

1. Go to: **Settings → Branches → Branch protection rules**

2. **Protection for `main` branch:**
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
     - Select: `Test Suite (chromium)`
     - Select: `Test Suite (firefox)`
     - Select: `Test Suite (webkit)`
     - Select: `Code Quality Checks`
     - Select: `Lint and quality`
   - ✅ Require branches to be up to date before merging
   - ✅ Dismiss stale pull request approvals
   - ✅ Require code reviews: **1 approval minimum**
   - ✅ Include administrators

3. **Protection for `develop` branch:**
   - Same as above but allow 1 approval before merging

### Status Check Configuration

```
Required Status Checks:
├── Test Suite (chromium)
├── Test Suite (firefox)
├── Test Suite (webkit)
├── Code Quality Checks
├── Lint and quality
└── Pull Request Checks (for PRs)
```

---

## GitHub Pages Setup

### Enable GitHub Pages for Test Reports

1. **Settings → Pages**
   - Source: Deploy from a branch
   - Branch: `gh-pages`
   - Folder: `/ (root)`

2. **Workflow Configuration:**
   - Allure reports auto-deploy on successful pushes to `main`
   - Reports available at: `https://YOUR-USERNAME.github.io/YOUR-REPO/`
   - Coverage reports available at: `https://YOUR-USERNAME.github.io/YOUR-REPO/coverage/`

3. **Access Reports:**
   - View latest Allure report (auto-updated)
   - Historical reports with trend analysis
   - Coverage trend reports

---

## Slack Integration (Optional)

### Setup Slack Notifications

1. **Create Slack Webhook:**
   - Go to your Slack workspace
   - Create incoming webhook for #test-automation channel
   - Copy webhook URL

2. **Add to GitHub Secrets:**
   - Secret name: `SLACK_WEBHOOK_URL`
   - Value: Your webhook URL from step 1

3. **Notifications Sent For:**
   - All CI/CD pipeline runs
   - Test failure automatic issues
   - Scheduled smoke test results

### Example Slack Message:

```
✅ GitHub Actions Build
Passed on main branch
Branch: refs/heads/main
Commit: abc123def456
[View Details]
```

---

## Running Tests

### 1. Automatic Triggers

**On Push to `main`:**

```bash
$ git push origin main
→ Runs: Full test suite (all browsers)
→ Duration: ~15-20 minutes
→ Report: Auto-deployed to GitHub Pages
```

**On Pull Request:**

```bash
$ git push origin feature-branch
$ # Create pull request
→ Runs: Smoke tests + coverage check
→ Duration: ~5-10 minutes
→ Result: Comment on PR with summary
```

### 2. Manual Test Runs

**Via GitHub UI:**

1. Go to: **Actions → Manual Test Run**
2. Click: **Run workflow**
3. Select:
   - Test Suite: `smoke` (quick) or `regression` (full)
   - Browser: `chromium` or `all-browsers`
   - Parallel: ✅ (faster execution)
   - Retries: `1` or `2`
4. Click: **Run workflow**

**Via GitHub CLI:**

```bash
gh workflow run manual-test-run.yml \
  -f test_suite=smoke \
  -f browser=chromium \
  -f parallel=true
```

### 3. Scheduled Automatic Runs

```
Smoke Tests:
├── Every 6 hours (health check)
├── Daily at 9 PM (night report)
└── Auto-cleanup old artifacts (7 days)

Full Tests:
├── Daily at 8 AM UTC
└── Weekly regression on Sunday
```

---

## Accessing Test Reports

### 1. GitHub UI

**From Actions Tab:**

- Click any workflow run
- Scroll to "Artifacts"
- Download test reports and logs

**From PR:**

- Automated comment appears with test summary
- Links to full test results
- Coverage report preview

### 2. Allure Reports (GitHub Pages)

Access at: `https://USERNAME.github.io/REPO-NAME/`

Features:

- Interactive test timeline
- Test case details and attachments
- Trend analysis
- Failure reasons

### 3. Coverage Reports

- Generated on every test run
- Uploaded to Codecov (optional)
- Available as artifact
- Minimum 60% coverage requirement on PRs

---

## Troubleshooting

### Issue: Tests timeout in CI

**Solution:**

```yaml
# In workflow file, increase timeout:
timeout-minutes: 60  # Default is 20

# Or in pytest.ini:
[pytest]
timeout = 30  # seconds
```

### Issue: Playwright browsers not found

**Solution:**

```bash
# Ensure this step runs:
- name: Install Playwright browsers
  run: playwright install --with-deps
```

### Issue: Slack notifications not sending

**Solution:**

- Verify `SLACK_WEBHOOK_URL` secret is set correctly
- Test webhook URL manually:
  ```bash
  curl -X POST -H 'Content-type: application/json' \
    --data '{"text":"Test"}' \
    YOUR_WEBHOOK_URL
  ```

### Issue: GitHub Pages not updating

**Solution:**

- Ensure `.github/workflows/ci-cd.yml` includes Allure deployment step
- Check `gh-pages` branch exists
- Verify GitHub Pages enabled in Settings

### Issue: PR checks not blocking merge

**Solution:**

1. Create branch protection rule
2. Add required status checks:
   - `Test Suite (chromium)`
   - `Test Suite (firefox)`
   - `Test Suite (webkit)`

### Issue: Out of memory during parallel tests

**Solution:**

```yaml
# Disable parallel execution:
- run: pytest tests/ -v # Remove: -n auto

# Or limit workers:
- run: pytest tests/ -n 2
```

---

## Best Practices

### 1. Commit Messages

```
# ✅ Good
feat(tests): add login validation tests
fix(utils): correct page wait timeout
docs(readme): update setup instructions

# ❌ Avoid
Updated tests
Fixed stuff
Changed code
```

### 2. PR Workflow

```bash
# Create feature branch
git checkout -b feat/new-test-suite

# Make changes and commit
git add .
git commit -m "feat(tests): add checkout flow tests"

# Push to GitHub
git push origin feat/new-test-suite

# Create PR and wait for checks
# Automated comments appear with test results
```

### 3. Monitoring

**Review Regularly:**

- Workflow run history
- Test failure trends
- Slow test detection
- Coverage trends

**Set Alerts:**

- Branch protection enforcement
- Failed workflow notifications
- High flake rate detection

---

## Advanced Configuration

### Matrix Testing with Different Environments

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    browser: [chromium, firefox]
    python-version: ["3.10", "3.11"]
```

### Artifact Retention

```yaml
retention-days: 30 # Default
# Options: 1-90 days
```

### Conditional Steps

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && success()
  run: ./deploy.sh
```

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Playwright Documentation](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org)
- [Allure Report Documentation](https://docs.qameta.io/allure/)
- [GitHub Pages Documentation](https://docs.github.com/pages)

---

## Support

For issues or questions:

1. Check [GitHub Actions logs](https://docs.github.com/actions/monitoring-and-troubleshooting-workflows)
2. Review workflow file syntax
3. Verify secrets are properly configured
4. Check branch protection rule settings
