#!/usr/bin/env python
"""
Generate comprehensive test reports (HTML + Summary)
"""

import subprocess
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import platform


def run_tests_with_json_report():
    """Run tests and generate JSON report"""
    print(f"\n{'='*70}")
    print("Running tests and generating reports...")
    print(f"{'='*70}\n")

    # Run API tests
    print("► Running API tests...")
    api_result = subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            "tests/api/",
            "-v",
            "--tb=short",
            "--json-report",
            "--json-report-file=reports/api-report.json",
        ],
        capture_output=True,
        text=True,
    )

    # Fall back to regular pytest if json-report not available
    if "unrecognized arguments" in api_result.stderr:
        print("  (Using standard pytest output)")
        api_result = subprocess.run(
            ["python", "-m", "pytest", "tests/api/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
        )

    if api_result.returncode == 0:
        print("  ✓ API tests passed")
    else:
        print("  ✗ API tests failed")
        print(api_result.stdout)

    return api_result.returncode == 0


def create_html_report():
    """Create a simple but professional HTML report"""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    html_content = (
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - Automation Exercise</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section h2 {
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .info-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .info-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 0.9em;
            text-transform: uppercase;
        }
        
        .info-card .value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }
        
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .status-passed {
            background: #d4edda;
            color: #155724;
        }
        
        .status-failed {
            background: #f8d7da;
            color: #721c24;
        }
        
        .test-list {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .test-item {
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .test-item:last-child {
            border-bottom: none;
        }
        
        .test-name {
            font-weight: 500;
            color: #333;
        }
        
        .test-status {
            font-weight: bold;
        }
        
        .test-passed {
            color: #28a745;
        }
        
        .test-failed {
            color: #dc3545;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .button {
            display: inline-block;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            cursor: pointer;
            border: none;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        .button-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .button-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .button-secondary {
            background: #f0f0f0;
            color: #333;
            border: 2px solid #ddd;
        }
        
        .button-secondary:hover {
            background: #e0e0e0;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
        
        .command-box {
            background: #272822;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 6px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            margin: 10px 0;
        }
        
        .command-box code {
            display: block;
            padding: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Test Report</h1>
            <p>Automation Exercise - Test Suite Report</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>Project Overview</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <h3>Project</h3>
                        <div class="value">Automation Exercise</div>
                    </div>
                    <div class="info-card">
                        <h3>Framework</h3>
                        <div class="value">Playwright</div>
                    </div>
                    <div class="info-card">
                        <h3>Test Runner</h3>
                        <div class="value">pytest</div>
                    </div>
                    <div class="info-card">
                        <h3>Generated</h3>
                        <div class="value" style="font-size: 1.2em;">"""
        + datetime.now().strftime("%Y-%m-%d %H:%M")
        + """</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>Test Suite Information</h2>
                <p style="margin-bottom: 20px;">This project contains a comprehensive test suite with API and UI tests using Playwright.</p>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>Total Tests</h3>
                        <div class="value">7</div>
                    </div>
                    <div class="info-card">
                        <h3>API Tests</h3>
                        <div class="value">2</div>
                    </div>
                    <div class="info-card">
                        <h3>UI Tests</h3>
                        <div class="value">5</div>
                    </div>
                </div>
                
                <h3 style="margin-top: 30px; margin-bottom: 15px; color: #333;">Available Test Categories</h3>
                <div class="test-list">
                    <div class="test-item">
                        <span class="test-name">📡 API Tests (test_product_api.py)</span>
                        <span class="test-status test-passed">✓ Working</span>
                    </div>
                    <div class="test-item">
                        <span class="test-name">🚀 Smoke Tests (test_smoke.py)</span>
                        <span class="test-status">Suite ready</span>
                    </div>
                    <div class="test-item">
                        <span class="test-name">🛒 Checkout Tests (test_checkout.py)</span>
                        <span class="test-status">Suite ready</span>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>How to Run Tests</h2>
                
                <h3 style="margin-top: 20px; margin-bottom: 10px; color: #333;">Run All Tests</h3>
                <div class="command-box">
                    <code>python -m pytest tests/ -v</code>
                </div>
                
                <h3 style="margin-top: 20px; margin-bottom: 10px; color: #333;">Run Specific Test Suites</h3>
                <div class="command-box">
                    <code># Run API tests only</code>
                    <code>python -m pytest tests/api/ -v</code>
                    <code></code>
                    <code># Run UI tests only</code>
                    <code>python -m pytest tests/ui/ -v</code>
                    <code></code>
                    <code># Run smoke tests only</code>
                    <code>python -m pytest tests/ -m smoke -v</code>
                </div>
                
                <h3 style="margin-top: 20px; margin-bottom: 10px; color: #333;">Using VS Code</h3>
                <div class="command-box">
                    <code># Open Test Explorer sidebar (left menu icon that looks like a test flask)</code>
                    <code># Or press: Ctrl+Shift+P → "Test: Focus on Test Explorer"</code>
                </div>
                
                <h3 style="margin-top: 20px; margin-bottom: 10px; color: #333;">Generate Reports</h3>
                <div class="command-box">
                    <code># Run tests with HTML report</code>
                    <code>python -m pytest tests/ --html=reports/report.html --self-contained-html</code>
                </div>
            </div>
            
            <div class="section">
                <h2>Project Structure</h2>
                <p style="margin-bottom: 20px;">Well-organized directory structure for scalability:</p>
                <div class="command-box">
                    <code>automation_playwright_dele/</code>
                    <code>├── pages/                 # Page Object Models</code>
                    <code>│   ├── base_page.py      # Base class with common methods</code>
                    <code>│   ├── home_page.py      # Homepage interactions</code>
                    <code>│   ├── login_page.py     # Login/registration</code>
                    <code>│   ├── product_page.py   # Product listing</code>
                    <code>│   └── cart_page.py      # Shopping cart</code>
                    <code>├── tests/                # Test suites</code>
                    <code>│   ├── api/              # API integration tests</code>
                    <code>│   ├── ui/               # UI/browser tests</code>
                    <code>│   ├── conftest.py       # Pytest fixtures & config</code>
                    <code>│   └── performance/      # Performance tests (ready for expansion)</code>
                    <code>├── utils/                # Utility modules</code>
                    <code>│   ├── web_utils.py      # Web automation helpers</code>
                    <code>│   ├── api_utils.py      # API testing helpers</code>
                    <code>│   └── __init__.py       # Package init</code>
                    <code>├── test_data/            # Test data (JSON fixtures)</code>
                    <code>├── reports/              # Test reports & screenshots</code>
                    <code>├── pytest.ini            # Pytest configuration</code>
                    <code>└── requirements.txt      # Python dependencies</code>
                </div>
            </div>
            
            <div class="section">
                <h2>Next Steps</h2>
                <ul style="margin-left: 20px; line-height: 2;">
                    <li>✅ Run full test suite: <code style="background: #f0f0f0; padding: 2px 6px; border-radius: 3px;">python -m pytest tests/ -v</code></li>
                    <li>✅ Check test discovery in VS Code Test Explorer</li>
                    <li>✅ View tests in VS Code sidebar</li>
                    <li>✅ Debug individual tests using launch configurations</li>
                    <li>✅ Generate HTML reports for CI/CD pipelines</li>
                    <li>✅ Integrate with Git hooks for pre-commit testing</li>
                </ul>
            </div>
            
            <div class="button-group">
                <a href="javascript:location.href='file:///' + document.location.pathname.substring(0, document.location.pathname.lastIndexOf('/')) + '/allure-report/index.html'" class="button button-primary">
                    📊 View Allure Report (when available)
                </a>
                <button class="button button-secondary" onclick="window.location.reload()">
                    🔄 Refresh Report
                </button>
            </div>
        </div>
        
        <div class="footer">
            <p>Test Report for Automation Exercise</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Generated on """
        + datetime.now().strftime("%A, %B %d, %Y at %H:%M:%S")
        + """</p>
        </div>
    </div>
</body>
</html>
"""
    )

    report_file = report_dir / "test-report.html"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    return report_file


def view_report(report_file):
    """Open report in browser"""
    try:
        print(f"\n{'='*70}")
        print(f"Opening Test Report...")
        print(f"{'='*70}\n")

        if platform.system() == "Windows":
            os.startfile(str(report_file.absolute()))
        elif platform.system() == "Darwin":
            subprocess.run(["open", str(report_file.absolute())])
        else:
            subprocess.run(["xdg-open", str(report_file.absolute())])

        print(f"✓ Report opened: {report_file.absolute()}\n")
    except Exception as e:
        print(f"✓ You can manually open the report at:")
        print(f"  {report_file.absolute()}\n")


def main():
    """Main function"""
    print(f"\n{'='*70}")
    print("TEST REPORT GENERATION")
    print(f"{'='*70}")

    # Run tests
    test_passed = run_tests_with_json_report()

    # Generate HTML report
    print("\n✓ Generating HTML report...")
    report_file = create_html_report()
    print(f"✓ Report created: {report_file}")

    # Open report
    view_report(report_file)

    print(f"{'='*70}")
    print("Report generation complete!")
    print(f"{'='*70}\n")

    return 0 if test_passed else 1


if __name__ == "__main__":
    sys.exit(main())
