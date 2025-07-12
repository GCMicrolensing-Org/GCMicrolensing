#!/usr/bin/env python3
"""
Script to bump version numbers across project files.

This script updates version numbers in pyproject.toml, CITATION.cff, and README.md
files when creating a new release. It's designed to be run from GitHub Actions
during the release process.

Usage:
    python bump_version.py <version> <date>
"""
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    print("Usage: bump_version.py <version> <date>")
    sys.exit(1)

version = sys.argv[1]
date = sys.argv[2]

# Update pyproject.toml
pyproject = Path("pyproject.toml")
if pyproject.exists():
    text = pyproject.read_text()
    text = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{version}"', text)
    pyproject.write_text(text)

# Update CITATION.cff
citation = Path("CITATION.cff")
if citation.exists():
    text = citation.read_text()
    text = re.sub(r'^version: ".*"', f'version: "{version}"', text, flags=re.MULTILINE)
    text = re.sub(r'^date-released: ".*"', f'date-released: "{date}"', text, flags=re.MULTILINE)
    citation.write_text(text)

# Optionally update README.md version badge (if present)
readme = Path("README.md")
if readme.exists():
    text = readme.read_text()
    # Example: replace version in a badge or text like 'GCMicrolensing vX.Y.Z'
    text = re.sub(r"GCMicrolensing v[0-9]+\.[0-9]+\.[0-9]+", f"GCMicrolensing v{version}", text)
    readme.write_text(text)
