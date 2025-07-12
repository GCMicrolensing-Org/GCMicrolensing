"""Packaging script for the :mod:`GCMicrolensing` project."""

import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup
from setuptools.command.install import install

current_dir = Path(__file__).resolve().parent
triplelens_path = current_dir / "triplelens"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class InstallWithTripleLensing(install):
    """Custom install command that builds TripleLensing first."""

    def run(self):
        """Run the install command, building TripleLensing if present."""
        # Build TripleLensing first
        if triplelens_path.exists():
            print("Building TripleLensing...")
            try:
                subprocess.check_call(
                    [sys.executable, "setup.py", "build_ext", "--inplace"], cwd=triplelens_path
                )
                print("TripleLensing built successfully")
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to build TripleLensing: {e}")
                print("GCMicrolensing will be installed without TripleLensing support")
        else:
            print(f"TripleLensing path not found: {triplelens_path}")
            print(f"Current directory contents: {list(current_dir.iterdir())}")
            gcmicrolensing_path = current_dir / "GCMicrolensing"
            if gcmicrolensing_path.exists():
                print(f"GCMicrolensing directory contents: {list(gcmicrolensing_path.iterdir())}")

        # Run the normal install
        install.run(self)


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
    cmdclass={"install": InstallWithTripleLensing},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
