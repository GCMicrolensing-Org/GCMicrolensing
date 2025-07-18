#!/usr/bin/env python3
"""
Script to bump version numbers across project files.

This script updates version numbers in setup.py, CITATION.cff, and README.md
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

# Update GCMicrolensing/__init__.py
init_file = Path("GCMicrolensing/__init__.py")
if init_file.exists():
    text = init_file.read_text()
    text = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{version}"', text)
    init_file.write_text(text)

# Update setup.py
setup_py = Path("setup.py")
if setup_py.exists():
    text = setup_py.read_text()
    text = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{version}"', text)
    setup_py.write_text(text)

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
