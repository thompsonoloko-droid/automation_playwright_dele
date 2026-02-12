# Rotate Credentials Checklist

This file documents recommended, repeatable steps to rotate any credentials that may have been exposed.

Steps:

- Identify affected secrets (CI, cloud provider keys, service accounts).
- Revoke or rotate keys in the provider console (AWS/GCP/Azure, payment providers, etc.).
- Update GitHub Secrets and other secret stores with new values.
- Trigger CI to verify new secrets work (use a non-production test run first).
- Revoke old keys after verification.
- Inform team and update README / runbook with new expiry/rotation cadence.

Notes:
- This repo cannot rotate external secrets automatically. Follow provider documentation.
- Consider short-lived credentials and OIDC where possible.
