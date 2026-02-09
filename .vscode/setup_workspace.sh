# setup_workspace.sh
#!/bin/bash

# Playwright Automation Framework - Workspace Setup Script
# This script initializes a complete test automation workspace with Playwright, pytest, and auxiliary tools.

set -e  # Exit on error

PROJECT_NAME="automation-exercise-tests"
BASE_DIR="$PROJECT_NAME"

echo "🚀 Setting up Playwright Test Automation Workspace..."
echo ""

# Create project structure
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

# Create directory structure
echo "📁 Creating project structure..."
mkdir -p .vscode
mkdir -p tests/ui
mkdir -p tests/api
mkdir -p tests/performance
mkdir -p pages
mkdir -p utils/helpers
mkdir -p reports/{screenshots,videos,allure-results,coverage}
mkdir -p test_data
mkdir -p docs
mkdir -p logs
mkdir -p components

# Create .vscode/settings.json
echo "⚙️  Configuring VS Code settings..."
cat > .vscode/settings.json << 'EOF'
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests", "-v", "--tb=short"],
  "python.testing.unittestEnabled": false,
  "python.defaultInterpolationFormat": "fstring",
  "terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}"
  },
  "terminal.integrated.env.linux": {
    "PYTHONPATH": "${workspaceFolder}"
  },
  "terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}"
  },
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/*.pyc": true
  },
  "python.analysis.extraPaths": [
    "${workspaceFolder}/pages",
    "${workspaceFolder}/utils",
    "${workspaceFolder}/tests"
  ]
}
EOF

# Create requirements.txt with comprehensive dependencies
echo "📦 Creating requirements.txt with all dependencies..."
cat > requirements.txt << 'EOF'
# =====================================
# Test Automation Framework Dependencies
# =====================================
# 
# Core Testing & Automation
pytest==8.4.0                      # Test framework with advanced features
pytest-playwright==0.8.0           # Pytest integration for Playwright
playwright==1.58.0                 # Cross-browser automation library (Chromium, Firefox, WebKit)

# API Testing
requests==2.32.5                   # HTTP client for API testing and REST endpoints

# Test Reporting & Visualization
pytest-html==4.2.0                 # HTML report generation with detailed results
allure-pytest==2.15.3              # Allure test report integration for beautiful dashboards

# Environment & Configuration
python-dotenv==1.2.1               # Load environment variables from .env files

# Quality & Performance Tools
pytest-cov==6.1.0                  # Code coverage measurement and reporting
pytest-xdist==3.8.0                # Parallel test execution for faster runs
pytest-timeout==2.4.0              # Test timeout management to prevent hanging tests
pytest-retry==1.7.0                # Automatic retry of flaky tests
pillow==12.1.0                     # Image processing for screenshot management

# Code Quality & Style
black==26.1.0                      # Code formatter for consistent styling
flake8==7.3.0                      # Code linter for quality checks
isort==6.1.0                       # Import statement sorter
mypy==1.20.0                       # Static type checker for Python

# Optional: Documentation
# sphinx==8.5.0                    # Documentation generator (uncomment if needed)

# =====================================
# Installation Instructions
# =====================================
# Install all dependencies:
#   pip install -r requirements.txt
#
# Install only core testing libraries:
#   pip install pytest playwright pytest-playwright requests
#
# Update specific package:
#   pip install --upgrade <package-name>
#
# Check outdated packages:
#   pip list --outdated
# =====================================
EOF

# Create pytest.ini with comprehensive configuration
echo "✅ Creating pytest.ini with markers and logging..."
cat > pytest.ini << 'EOF'
[pytest]
# Test discovery patterns
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Core execution options
addopts = 
    --strict-markers
    --tb=short
    --maxfail=5
    -v
    --disable-warnings
    --color=yes

# HTML reporting (optional: --html=reports/test-report.html)
# Allure reporting (optional: --alluredir=./reports/allure-results)

# Test markers
markers =
    smoke: Critical path/smoke tests for core functionality
    regression: Regression test suite
    api: API integration tests
    ui: UI/E2E tests
    cart: Shopping cart functionality
    login: Authentication and login tests
    checkout: Checkout process tests
    slow: Tests that take longer to execute
    skip_ci: Tests to skip in CI/CD pipeline

# Logging
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Output options
console_output_style = progress
junit_family = xunit2
EOF

# Create base Python files
echo "🐍 Creating base Python module files..."
touch __init__.py
touch tests/__init__.py
touch tests/ui/__init__.py
touch tests/api/__init__.py
touch tests/performance/__init__.py
touch pages/__init__.py
touch utils/__init__.py
touch utils/helpers/__init__.py
touch components/__init__.py

# Create sample conftest.py
cat > tests/conftest.py << 'EOF'
"""
pytest configuration and shared fixtures for all tests.
Fixtures are provided by pytest-playwright plugin.
"""
import pytest
import logging

logger = logging.getLogger(__name__)

# pytest-playwright provides these fixtures automatically:
# - page: Fresh page for each test
# - context: Fresh browser context
# - browser: Browser instance
# - playwright: Playwright instance

@pytest.fixture(autouse=True)
def log_test_info(request):
    """Log test information at start and end"""
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Completed test: {request.node.name}")
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Pytest
.pytest_cache/
.coverage
htmlcov/

# Test Reports
reports/
*.html

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.venv
venv/
ENV/

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
EOF

# Create .env.example
cat > .env.example << 'EOF'
# Test Configuration
BASE_URL=https://automationexercise.com
API_BASE_URL=https://automationexercise.com/api

# Playwright Settings
HEADLESS=true
TIMEOUT=30000
BROWSER=chromium

# Test Execution
PARALLEL_TESTS=false
RETRY_COUNT=1
EOF

# Create README.md with setup instructions
cat > README.md << 'EOF'
# Playwright Test Automation Framework

Complete test automation framework using Playwright, pytest, and Python.

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone/Setup the workspace**
   ```bash
   cd automation-exercise-tests
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

### Running Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test file:**
```bash
pytest tests/ui/test_login.py -v
```

**Run tests with specific marker:**
```bash
pytest -m smoke -v
pytest -m api -v
```

**Run tests in parallel:**
```bash
pytest tests/ -n auto -v
```

**Generate HTML report:**
```bash
pytest tests/ -v --html=reports/report.html
```

**Generate Allure report:**
```bash
pytest tests/ -v --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Project Structure

```
automation-exercise-tests/
├── tests/                 # Test files
│   ├── ui/               # UI/E2E tests
│   ├── api/              # API tests
│   └── performance/      # Performance tests
├── pages/                # Page Object Models
├── utils/                # Utility functions and helpers
├── components/           # Reusable components
├── reports/              # Test reports and artifacts
├── test_data/            # Test data files
├── .vscode/              # VS Code configuration
├── pytest.ini            # pytest configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

### pytest.ini
Configure test discovery, markers, and reporting.

### .vscode/settings.json
VS Code Python and testing settings.

### requirements.txt
All project dependencies with pinned versions.

## Available Test Markers

- `smoke` - Critical path tests
- `regression` - Full regression suite
- `api` - API tests
- `ui` - UI/E2E tests
- `cart` - Shopping cart tests
- `login` - Authentication tests
- `checkout` - Checkout process tests
- `slow` - Long-running tests
- `skip_ci` - Skip in CI/CD

## Best Practices

1. **Use Page Object Model** - Encapsulate page interactions
2. **Data-driven testing** - Parametrize with test data
3. **Comprehensive logging** - Track test execution
4. **Screenshot on failure** - Enable visual debugging
5. **Parallel execution** - Speed up test runs
6. **Type hints** - Use for code clarity

## Troubleshooting

**Import errors:**
```bash
pip install -r requirements.txt --upgrade
```

**Playwright issue:**
```bash
playwright install --with-deps
```

**Tests timeout:**
Update timeout in pytest.ini or .env file
EOF

echo ""
echo "✅ Workspace setup complete!"
echo ""
echo "Next steps:"
echo "  1. cd $BASE_DIR"
echo "  2. python -m venv venv"
echo "  3. source venv/bin/activate  (or venv\\Scripts\\activate on Windows)"
echo "  4. pip install -r requirements.txt"
echo "  5. playwright install"
echo "  6. pytest tests/ -v"
echo ""
echo "📚 Read README.md for more information"
echo ""