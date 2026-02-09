# Video Recording Configuration Guide

## Overview

Playwright can record videos of your tests. This guide shows you how to:

- **Disable** video recording completely
- **Enable** video recording for all tests
- **Enable** video recording for failed tests only
- **Delete** videos from passing tests automatically

---

## Current Configuration

**Status:** Videos are **DISABLED** by default

Videos are turned off to save storage space. You can enable them using the options below.

---

## Option 1: Disable Videos (Current Setup)

Videos are already disabled. The configuration in `tests/conftest.py` has the video setting commented out:

```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        # Uncomment the line below to enable video recording for ALL tests:
        # "record_video_dir": "./reports/videos"
    }
```

**Pros:**

- ✓ Saves disk space
- ✓ Tests run faster
- ✓ No video cleanup needed

**Cons:**

- ✗ Can't debug failed tests with video playback

---

## Option 2: Enable Videos for All Tests

Uncomment the `record_video_dir` line in `tests/conftest.py`:

```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "./reports/videos"  # ← Uncomment this line
    }
```

**Pros:**

- ✓ Record all test executions
- ✓ Easy debugging of failures
- ✓ Visual test documentation

**Cons:**

- ✗ Uses significant disk space
- ✗ Tests run slightly slower
- ✗ Need to clean up old videos

---

## Option 3: Record Only Failed Tests (Recommended)

Use this approach with the built-in `--video` option from pytest-playwright:

### Method A: Command Line Flag

Run tests with the `--video` option:

```bash
# Record failures only
python -m pytest tests/ --video=retain-on-failure

# Record all
python -m pytest tests/ --video=on

# Never record
python -m pytest tests/ --video=off
```

**Available Options:**

- `on` - Record all tests
- `off` - Record no tests
- `retain-on-failure` - Record all, keep only failed test videos
- `retain-on-failure-page` - Record all, keep failed test navigation

### Method B: Environment Variable

Set an environment variable before running tests:

**Windows (PowerShell):**

```powershell
$env:PYTEST_ADDOPTS = "--video=retain-on-failure"
python -m pytest tests/ -v
```

**Windows (Command Prompt):**

```cmd
set PYTEST_ADDOPTS=--video=retain-on-failure
python -m pytest tests/ -v
```

**macOS/Linux:**

```bash
PYTEST_ADDOPTS="--video=retain-on-failure" python -m pytest tests/ -v
```

### Method C: pytest.ini Configuration

Add to `pytest.ini`:

```ini
[pytest]
addopts = --video=retain-on-failure
```

**Pros:**

- ✓ Only saves videos for failed tests
- ✓ Minimal disk space
- ✓ Automatic cleanup of passing test videos

**Cons:**

- ✗ Can't see videos for passing tests
- ✗ Passing tests are slower (records then deletes)

---

## Option 4: Auto-Delete Passing Test Videos

Use the optional `cleanup_videos` fixture available in `tests/conftest.py`:

### Step 1: Enable Video Recording

Uncomment in `tests/conftest.py`:

```python
"record_video_dir": "./reports/videos"
```

### Step 2: Add Fixture to Tests

```python
def test_example(cleanup_videos):
    """
    This test will record video and delete it if test passes.
    Video is kept if test fails for debugging.
    """
    # ... test code ...
```

Or use for all tests by creating a marker:

```python
# In conftest.py, add:
@pytest.fixture(autouse=True)
def auto_cleanup_videos(cleanup_videos):
    """Automatically clean up videos from passing tests"""
    yield
```

**Pros:**

- ✓ Record all tests
- ✓ Keep only failed videos
- ✓ Manual control per test

**Cons:**

- ✗ Requires modifying test code
- ✗ Slower execution (record then delete)

---

## Video Storage Location

```
reports/
└── videos/           ← Video recordings stored here
    ├── test_*.webm   ← Individual test videos
    ├── test_*.mp4    ← Converted formats (if applicable)
    └── ...
```

**Estimated Storage:**

- Per test video: 1-5 MB (depending on test duration)
- Full suite (7 tests): 7-35 MB
- 100 test runs: 700-3500 MB (0.7-3.5 GB)

---

## Recommended Configuration

### For Development (Local Testing)

Disable videos to speed up testing:

```bash
python -m pytest tests/ -v
```

### For CI/CD Pipeline

Record only failed tests:

```bash
PYTEST_ADDOPTS="--video=retain-on-failure" python -m pytest tests/ -v
```

### For QA/Debugging

Enable all videos:

```bash
# Edit pytest.ini to add:
addopts = --video=on
```

---

## How to View Recorded Videos

Videos are saved in `.webm` format at:

```
reports/videos/
```

### Play Videos

1. **Windows/macOS:** Double-click to open in default video player
2. **VLC Player:** Open with VLC (supports all formats)
3. **Browser:** Drag `.webm` files into Chrome/Firefox address bar
4. **Online:** Upload to online player like https://media.io/

### Video Details

- **Format:** WebM (VP9 codec)
- **Resolution:** 1920x1080 (matching viewport)
- **Frame Rate:** 25 fps
- **Duration:** Variable (test execution time)

---

## Clean Up Old Videos

### Remove All Videos

```bash
# Using PowerShell
Remove-Item -Path "reports/videos/*" -Force -Recurse

# Using Command Prompt
rmdir /s /q reports\videos

# Using Python
import shutil
shutil.rmtree("reports/videos")
```

### Remove Videos Older Than X Days

```python
import shutil
from pathlib import Path
from datetime import datetime, timedelta

video_dir = Path("reports/videos")
days_to_keep = 7

for video_file in video_dir.glob("*.webm"):
    age = datetime.now() - datetime.fromtimestamp(video_file.stat().st_mtime)
    if age > timedelta(days=days_to_keep):
        video_file.unlink()
        print(f"Deleted old video: {video_file}")
```

---

## Quick Reference

| Use Case           | Command                                               | Video Size        |
| ------------------ | ----------------------------------------------------- | ----------------- |
| **Local Dev**      | `pytest tests/ -v`                                    | None              |
| **Fast CI**        | `pytest tests/ --video=retain-on-failure`             | Min (failed only) |
| **Full Recording** | `pytest tests/ --video=on`                            | Max (all tests)   |
| **Debug Failures** | `pytest tests/ --video=on` + review `reports/videos/` | All tests         |

---

## Troubleshooting

### Issue: Videos not being recorded

**Solution:** Ensure `record_video_dir` is uncommented in conftest.py

### Issue: Videos consume too much space

**Solution:** Use `--video=retain-on-failure` when running tests

### Issue: Can't play recorded videos

**Solution:** Install VLC player or use online player at https://media.io/

### Issue: Old videos taking up space

**Solution:** Run cleanup script or manually delete `reports/videos/`

---

## Summary

- **Current Setup:** Videos disabled (saves space)
- **Recommended:** Use `--video=retain-on-failure` for CI/CD
- **For Development:** Keep videos disabled, enable only when debugging
- **For QA:** Enable all videos with `--video=on`

Choose the option that best fits your workflow!
