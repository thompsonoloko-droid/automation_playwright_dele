#!/usr/bin/env python3
import json
from pathlib import Path

BASELINE = Path(".secrets.baseline")
IGNORE_PATTERNS = [
    ".venv/",
    ".venv\\",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "reports/",
    "reports\\",
    "widgets/",
    ".git\\filter-repo",
]


def matches_ignore(path: str) -> bool:
    p = path.replace("\\", "/").lower()
    for pat in IGNORE_PATTERNS:
        if pat.replace("\\", "/").lower() in p:
            return True
    if p.endswith(".pyc") or p.endswith(".png") or p.endswith(".jpg"):
        return True
    return False


def main():
    if not BASELINE.exists():
        print(".secrets.baseline not found")
        return
    # Read as bytes and decode defensively to handle possible BOMs
    raw = BASELINE.read_bytes()
    # detect common BOM/encoding
    if raw.startswith(b"\xff\xfe"):
        text = raw.decode("utf-16")
    elif raw.startswith(b"\xfe\xff"):
        text = raw.decode("utf-16")
    else:
        # fallback to utf-8 with replacement
        text = raw.decode("utf-8", errors="replace")
    try:
        data = json.loads(text)
    except Exception as exc:
        print("Failed to parse .secrets.baseline as JSON:", exc)
        return
    results = data.get("results", {})
    removed = 0
    kept = 0
    new_results = {}
    for fname, findings in results.items():
        if matches_ignore(fname):
            removed += len(findings)
            continue
        # filter any findings that are in ignored paths inside the file
        kept_findings = [f for f in findings if not matches_ignore(f.get("filename", fname))]
        removed += len(findings) - len(kept_findings)
        if kept_findings:
            new_results[fname] = kept_findings
            kept += len(kept_findings)

    data["results"] = new_results
    BASELINE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Filtered baseline: removed {removed} findings, kept {kept} findings")


if __name__ == "__main__":
    main()
