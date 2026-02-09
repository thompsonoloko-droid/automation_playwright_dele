#!/usr/bin/env python
# generate_allure_report.py - Script to generate and open Allure test reports
"""
Generate and open Allure test reports
"""

import subprocess
import os
import sys
import platform
import shutil
from pathlib import Path


def check_allure_installed():
    """Check if Allure is installed"""
    result = subprocess.run(["allure", "--version"], capture_output=True, text=True)
    return result.returncode == 0


def install_allure():
    """Provide instructions for installing Allure"""
    print("\n" + "=" * 70)
    print("Allure CLI is not installed")
    print("=" * 70)

    if platform.system() == "Windows":
        print("\nTo install Allure on Windows, use one of these methods:")
        print("\n1. Using Chocolatey (recommended):")
        print("   choco install allure")
        print(
            "\n2. Download from: https://github.com/allure-framework/allure2/releases"
        )
        print("   Then add the bin directory to your PATH")
    elif platform.system() == "Darwin":
        print("\nTo install Allure on macOS:")
        print("   brew install allure")
    else:  # Linux
        print("\nTo install Allure on Linux:")
        print("   sudo apt-get install allure")

    print("\n" + "=" * 70)
    return False


def generate_report(
    results_dir="reports/allure-results", report_dir="reports/allure-report"
):
    """Generate Allure report from results"""
    print(f"\n{'='*70}")
    print(f"Generating Allure Report...")
    print(f"{'='*70}")

    # Check if results directory exists and has data
    results_path = Path(results_dir)
    if not results_path.exists() or not list(results_path.glob("*.json")):
        print(f"\n⚠ No test results found in {results_dir}")
        print("Run tests first: python -m pytest tests/")
        return False

    try:
        # Create report directory
        report_path = Path(report_dir)
        if report_path.exists():
            shutil.rmtree(report_path)

        # Generate report
        cmd = ["allure", "generate", results_dir, "-o", report_dir, "--clean"]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Report generated successfully!")
            print(f"✓ Location: {os.path.abspath(report_dir)}")
            return True
        else:
            print(f"✗ Error generating report:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def open_report(report_dir="reports/allure-report"):
    """Open Allure report in browser"""
    report_path = Path(report_dir)

    if not report_path.exists():
        print(f"\n✗ Report directory not found: {report_dir}")
        return False

    index_file = report_path / "index.html"
    if not index_file.exists():
        print(f"\n✗ Report index.html not found")
        return False

    try:
        print(f"\n{'='*70}")
        print(f"Opening Allure Report in browser...")
        print(f"{'='*70}\n")

        url = f"file:///{index_file.absolute()}".replace("\\", "/")

        if platform.system() == "Windows":
            os.startfile(str(index_file.absolute()))
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(index_file.absolute())])
        else:  # Linux
            subprocess.run(["xdg-open", str(index_file.absolute())])

        print(f"✓ Report opened at: {url}\n")
        return True

    except Exception as e:
        print(f"✗ Error opening report: {str(e)}")
        print(f"\n✓ You can manually open the report at:")
        print(f"  {index_file.absolute()}\n")
        return False


def main():
    """Main function"""
    # Check if Allure is installed
    if not check_allure_installed():
        if not install_allure():
            print("\nPlease install Allure CLI and try again.")
            sys.exit(1)

    # Generate report
    if not generate_report():
        sys.exit(1)

    # Open report
    open_report()

    print("=" * 70)
    print("Allure Report Generation Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
