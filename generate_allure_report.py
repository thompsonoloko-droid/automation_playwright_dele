"""
Generate Allure Report
======================
Generates and optionally serves the Allure test report from results in reports/allure-results/.

Usage:
    python generate_allure_report.py           # Generate report
    python generate_allure_report.py --serve    # Generate and open in browser
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

RESULTS_DIR = Path("reports/allure-results")
REPORT_DIR = Path("reports/allure-report")


def check_allure_installed() -> bool:
    """Check if Allure CLI is available on PATH."""
    return shutil.which("allure") is not None


def generate_report() -> bool:
    """Generate Allure report from results directory."""
    if not RESULTS_DIR.exists() or not any(RESULTS_DIR.iterdir()):
        print(f"[WARNING] No allure results found in {RESULTS_DIR}")
        print("Run tests with --alluredir=reports/allure-results first.")
        return False

    if not check_allure_installed():
        print("[ERROR] Allure CLI is not installed or not on PATH.")
        print("Install it via: npm install -g allure-commandline")
        print("  or: brew install allure  (macOS)")
        print("  or: scoop install allure  (Windows)")
        return False

    print(f"Generating Allure report from {RESULTS_DIR}...")
    result = subprocess.run(
        ["allure", "generate", str(RESULTS_DIR), "-o", str(REPORT_DIR), "--clean"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[ERROR] Allure generate failed:\n{result.stderr}")
        return False

    print(f"Report generated at {REPORT_DIR}")
    return True


def serve_report() -> None:
    """Open the Allure report in the default browser."""
    if not REPORT_DIR.exists():
        print(f"[ERROR] Report directory {REPORT_DIR} not found. Generate it first.")
        return

    print(f"Opening Allure report from {REPORT_DIR}...")
    subprocess.run(["allure", "open", str(REPORT_DIR)])


def main() -> None:
    os.chdir(Path(__file__).resolve().parent)

    success = generate_report()

    if success and "--serve" in sys.argv:
        serve_report()
    elif success:
        print(f"\nTo view the report, run: allure open {REPORT_DIR}")


if __name__ == "__main__":
    main()
