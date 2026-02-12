#!/usr/bin/env pwsh
Set-StrictMode -Version Latest
Write-Host "Installing detect-secrets (local user)..."
python -m pip install --user --upgrade pip detect-secrets

Write-Host "Running detect-secrets scan (including ignored files)..."
detect-secrets scan --all-files > .secrets.baseline

if (Test-Path .secrets.baseline) {
    Write-Host ".secrets.baseline written — size:" (Get-Item .secrets.baseline).Length
} else {
    Write-Host "Baseline not created. Inspect output above for errors."
    exit 1
}

Write-Host "Done. Commit .secrets.baseline to the repo if it is reviewed and has no secrets."
