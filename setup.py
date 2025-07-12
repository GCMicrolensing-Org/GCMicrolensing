"""Packaging script for the :mod:`GCMicrolensing` project."""

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
    url="https://github.com/GregCuautle/SURP25",
    packages=find_packages(),
    package_data={
        "GCMicrolensing.triplelens": [
            "pymodule/python_bindings.cpp",
            "src/VBBinaryLensingLibrary.cpp",
            "src/TripleLensingLibrary.cpp",
            "src/VBBinaryLensingLibrary.h",
            "src/TripleLensingLibrary.h",
            "setup.py",
            "setup.cfg",
            "README.md",
            "LICENSE.md",
        ],
    },
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
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
