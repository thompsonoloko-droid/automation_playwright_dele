# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue.

Instead, email **[thompsonoloko-droid]** (or use GitHub's private vulnerability reporting feature) with:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

We will acknowledge receipt within **48 hours** and aim to release a fix within **7 days** for critical issues.

## Security Practices

- **Secrets**: All credentials are stored in GitHub Secrets / environment variables — never committed to the repository.
- **Dependencies**: Dependabot monitors for known CVEs weekly.
- **CI Permissions**: Workflows use least-privilege `permissions: contents: read`.
- **Pin Actions**: All GitHub Actions are pinned to full commit SHAs.
