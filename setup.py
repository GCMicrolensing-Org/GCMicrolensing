"""Packaging script for the :mod:`GCMicrolensing` project."""

import os
import subprocess
import sys

from setuptools import find_packages, setup

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
    url="https://github.com/GCMicrolensing-Org/GCMicrolensing",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "astropy",
        "VBMicrolensing>=5.0.0",
        "pandas",
        "seaborn",
        "astroquery",
        "pyvo",
        "emcee",
        "corner",
        "requests",
        "tqdm",
        "pybind11",
        "jupyter",
        "ipywidgets",
    ],
    extras_require={
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "nbsphinx>=0.8.0",
            "ipython>=8.0.0",
            "myst-parser>=0.18.0",
            "sphinx-autodoc-typehints>=1.19.0",
            "sphinx-gallery>=0.10.0",
            "sphinx-copybutton>=0.5.0",
            "sphinx-panels>=0.6.0",
            "sphinx-tabs>=3.0.0",
            "sphinxcontrib-bibtex>=2.4.0",
            "sphinxcontrib-mermaid>=0.7.0",
        ],
        "dev": [
            "black",
            "isort",
            "flake8",
            "mypy",
            "bandit",
            "pydocstyle",
            "nbqa",
            "pre-commit",
            "pytest",
            "pytest-cov",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)

# Build the C++ extension
try:
    # Import and run the triplelens setup
    triplelens_dir = os.path.join("GCMicrolensing", "triplelens")
    if os.path.exists(triplelens_dir):
        subprocess.check_call(
            [sys.executable, "setup.py", "build_ext", "--inplace"], cwd=triplelens_dir
        )
except subprocess.CalledProcessError as e:
    print(f"Warning: Failed to build TripleLensing extension: {e}")
    print("The package will be installed without the C++ extension.")
