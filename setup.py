"""Packaging script for the :mod:`GCMicrolensing` project."""

import os
from pathlib import Path
from setuptools import setup, find_packages

current_dir = Path(__file__).resolve().parent
triplelens_path = current_dir / "triplelens"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="GCMicrolensing",
    version="0.1.0",
    author="Gregory Costa Cuautle",
    author_email="costa.130@buckeyemail.osu.edu",
    description="Tools for simulating gravitational microlensing events.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GregCuautle/SURP25",
    packages=find_packages(exclude=["triplelens", "triplelens.*"]),
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "astropy",
        "VBMicrolensing",
        "pandas",
        f"TripleLensing @ file://{triplelens_path}",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
