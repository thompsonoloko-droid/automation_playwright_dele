# Python Virtual Environment Setup Guide

## Virtual Environment Status

A Python virtual environment has been created for this project at `.venv/`

---

## How to Use the Virtual Environment

### Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

When activated, your terminal prompt will show `(.venv)` prefix.

### Deactivate the Virtual Environment

```bash
deactivate
```

---

## Project Setup

### Step 1: Activate Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install playwright allure-pytest
```

Or install all at once:

```bash
python -m pip install -r requirements.txt playwright allure-pytest
```

### Step 3: Install Playwright Browsers

```bash
python -m playwright install
```

### Step 4: Verify Installation

```bash
python -m pytest --version
python -m playwright --version
```

---

## Running Tests from Virtual Environment

With venv activated, use normal commands:

```bash
# Run all tests
python -m pytest tests/ -v

# Run API tests
python -m pytest tests/api/ -v

# Run UI tests (requires Playwright browsers)
python -m pytest tests/ui/ -v

# Run smoke tests
python -m pytest tests/ -m smoke -v

# Generate test report
python generate_test_report.py
```

---

## VS Code Integration

### Step 1: Select Virtual Environment Interpreter

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `.venv interpreter` from the list

### Step 2: Verify Test Discovery

If tests don't appear in Test Explorer:

1. Press `Ctrl+Shift+P`
2. Run "Test: Discover Tests"
3. Click `.venv interpreter` when prompted

### Step 3: Use Test Explorer

- Click the test flask icon in left sidebar
- Browse and run tests visually
- Right-click for debug options

---

## Project Structure

```
automation_playwright_dele/
├── .venv/                  ← Virtual environment (created)
│   ├── Scripts/           ← Executable scripts (python.exe, pip.exe, etc.)
│   ├── Lib/               ← Installed packages
│   └── pyvenv.cfg         ← Venv configuration
├── .vscode/               ← VS Code settings
├── pages/                 ← Page Object Models
├── tests/                 ← Test suites
├── utils/                 ← Utility modules
├── reports/              ← Test results & artifacts
├── requirements.txt       ← Project dependencies
└── pytest.ini            ← Pytest configuration
```

---

## Installing Additional Packages

With venv activated:

```bash
# Install a single package
python -m pip install package-name

# Install from requirements file
python -m pip install -r requirements.txt

# Upgrade a package
python -m pip install --upgrade package-name

# List installed packages
python -m pip list
```

---

## Common Issues & Solutions

### Issue: "venv\Scripts\python: not found"

**Solution:** Make sure you've activated the venv:

```powershell
.venv\Scripts\Activate.ps1
python --version  # Should show Python 3.x.x
```

### Issue: Pytest not found

**Solution:** Install pytest in the venv:

```bash
python -m pip install pytest
```

### Issue: Playwright browsers not installed

**Solution:** Install browsers:

```bash
python -m playwright install
```

### Issue: Test discovery not working in VS Code

**Solution:** Select the correct interpreter:

1. `Ctrl+Shift+P` → "Python: Select Interpreter"
2. Choose `.venv\Scripts\python.exe`
3. Run Python: Discover Tests

---

## Virtual Environment Cleanup

### Remove venv (if needed)

```powershell
Remove-Item .venv -Recurse -Force
```

Then recreate:

```bash
python -m venv .venv
```

### Remove cached packages

```bash
python -m pip cache purge
```

---

## Best Practices

1. **Always activate venv before working**

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. **Keep requirements.txt updated**

   ```bash
   python -m pip freeze > requirements.txt
   ```

3. **Use venv in VS Code**
   - Select it as the Python interpreter
   - Run tests through the venv

4. **Don't commit venv to git**
   - Already excluded in `.gitignore`
   - Venv is machine and OS specific

5. **Share only requirements.txt**
   - Others can recreate venv with:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

---

## Quick Reference

| Task                         | Command                                     |
| ---------------------------- | ------------------------------------------- |
| **Activate venv**            | `.venv\Scripts\Activate.ps1`                |
| **Deactivate venv**          | `deactivate`                                |
| **Install dependencies**     | `python -m pip install -r requirements.txt` |
| **Install Playwright**       | `python -m playwright install`              |
| **Run tests**                | `python -m pytest tests/ -v`                |
| **Check installed packages** | `python -m pip list`                        |
| **Upgrade pip**              | `python -m pip install --upgrade pip`       |
| **Generate reports**         | `python generate_test_report.py`            |

---

## Summary

✅ Virtual environment created at `.venv/`
✅ Not yet activated (run `.venv\Scripts\Activate.ps1`)
✅ Next: Activate and install dependencies from requirements.txt
✅ Then: Select interpreter in VS Code
✅ Finally: Run tests using the venv

Your project is ready to use a clean, isolated Python environment!
