# VS Code Test Discovery Setup

## ✅ Configuration Complete

The project is now fully configured for test discovery in VS Code's Testing menu.

### What Was Fixed

1. **Created `.vscode/settings.json`** - Configured pytest as the test runner with proper discovery paths
2. **Created `.vscode/launch.json`** - Added debug configurations for running tests
3. **Created `.vscode/tasks.json`** - Added convenient test running tasks
4. **Created `.vscode/extensions.json`** - Recommended required extensions
5. **Added missing `__init__.py` files** in test directories for proper package discovery

### To Enable Test Discovery in VS Code

#### Step 1: Install Required Extensions

VS Code will prompt you to install the recommended extensions. Click "Install" when prompted, or manually install:

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Playwright Test for VSCode** (ms-playwright.playwright) - optional

#### Step 2: Reload VS Code

Press `Ctrl+Shift+P` and select:

- "Developer: Reload Window"

Or simply close and reopen VS Code.

#### Step 3: Access Test Explorer

The tests will now appear in VS Code's Testing menu. You can access them via:

1. **Testing Sidebar** - Click the test flask icon in the left sidebar
2. **Command Palette** - `Ctrl+Shift+P` → "Test: Focus on Test Explorer"

### Running Tests

#### From Test Explorer

- Click the play button next to test names or classes to run them
- Right-click for more options (debug, run with settings, etc.)

#### From Command Palette

- `Ctrl+Shift+P` → "Test: Run All Tests"
- `Ctrl+Shift+P` → "Test: Run Tests in File"
- `Ctrl+Shift+P` → "Test: Debug Test at Cursor"

#### From Tasks Menu

Press `Ctrl+Shift+B` and select from available tasks:

- Run All Tests
- Run UI Tests
- Run API Tests
- Run Smoke Tests
- Install Playwright Browsers

### Test Organization

```
tests/
├── api/                    # API integration tests
│   └── test_product_api.py
├── ui/                     # UI/Browser tests
│   ├── test_smoke.py       # Critical path tests
│   ├── test_checkout.py    # Checkout flow tests
│   └── wip.py             # Work in progress
├── performance/            # Performance tests (future)
└── conftest.py            # Pytest fixtures and configuration
```

### Available Test Markers

Run tests by marker using command palette or tasks:

- `@pytest.mark.smoke` - Critical functionality tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.checkout` - Checkout flow tests
- `@pytest.mark.login` - Authentication tests
- `@pytest.mark.cart` - Shopping cart tests

### Important Notes

**Playwright Browser Installation**
UI tests require Playwright browsers. Install them via:

```powershell
python -m playwright install
```

Or use the VS Code task: `Ctrl+Shift+B` → "Install Playwright Browsers"

**PYTHONPATH Configuration**
The workspace PYTHONPATH is automatically configured to include the workspace folder, allowing imports like:

```python
from pages.home_page import HomePage
from utils.web_utils import WebUtils
```

### Troubleshooting

If tests still don't appear:

1. **Check Python Interpreter**
   - `Ctrl+Shift+P` → "Python: Select Interpreter"
   - Choose the `.venv` interpreter

2. **Clear Test Cache**
   - Delete `.pytest_cache/` directory
   - Press `Ctrl+Shift+P` → "Test: Clear Test Results"

3. **Verify pytest Installation**

   ```powershell
   python -m pip install pytest pytest-playwright --upgrade
   ```

4. **Check if Tests Are Discovered**
   ```powershell
   python -m pip install pytest pytest-playwright --upgrade
   ```

All tests should be listed. If not, check for import errors in test files.
