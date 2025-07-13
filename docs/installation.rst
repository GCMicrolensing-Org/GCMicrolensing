Installation
===========

GCMicrolensing can be installed using pip or conda. The package requires Python 3.10 or higher.

Prerequisites
------------

This package requires a custom version of `TripleLensing` with modifications by Gregory Costa Cuautle. The installation process depends on how you obtained this package:

Option 1: From Source (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you cloned this repository, the custom `TripleLensing` is included and will be installed automatically:

.. code-block:: bash

   git clone <repository-url>
   cd Costa
   pip install -e .

Option 2: Manual Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're installing from a distribution that doesn't include `TripleLensing`, you'll need to install it manually:

.. code-block:: bash

   # First install GCMicrolensing
   pip install GCMicrolensing

   # Then install the custom TripleLensing (instructions to be provided)
   # This requires the custom version with Greg's modifications

Dependencies
-----------

GCMicrolensing depends on the following packages:

* numpy
* matplotlib
* pandas
* scipy
* seaborn
* astropy
* astroquery
* pyvo
* emcee
* corner
* requests
* tqdm
* pybind11
* jupyter
* ipywidgets
* VBMicrolensing
* TripleLensing

Installation Methods
-------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install GCMicrolensing

From Source
~~~~~~~~~~~

Clone the repository and install in development mode:

.. code-block:: bash

   git clone https://github.com/GCMicrolensing-Org/GCMicrolensing.git
   cd GCMicrolensing
   pip install -e .

Using Conda
~~~~~~~~~~~

.. code-block:: bash

   conda install -c conda-forge gcmicrolensing

Verification
-----------

After installation, verify that the package works correctly:

.. code-block:: python

   from GCMicrolensing.models import OneL1S
   print("GCMicrolensing installed successfully!")

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

**Import Error for VBMicrolensing or TripleLensing**

These are specialized microlensing libraries that may need to be installed separately:

.. code-block:: bash

   # Install VBMicrolensing
   pip install VBMicrolensing

   # Install TripleLensing (if available)
   pip install TripleLensing

**C++ Compiler Issues**

If you encounter compilation errors, ensure you have a C++ compiler installed:

* **Windows**: Install Visual Studio Build Tools
* **macOS**: Install Xcode Command Line Tools
* **Linux**: Install gcc/g++

**Python Version Issues**

Ensure you're using Python 3.10 or higher:

.. code-block:: bash

   python --version
   # Should show Python 3.10.x or higher

Getting Help
-----------

If you encounter issues during installation:

1. Check the `troubleshooting` section above
2. Search existing issues on the `GitHub repository <https://github.com/GCMicrolensing-Org/GCMicrolensing/issues>`_
3. Create a new issue with detailed error information

Development Installation
-----------------------

For developers who want to contribute to the project:

.. code-block:: bash

   git clone https://github.com/GCMicrolensing-Org/GCMicrolensing.git
   cd GCMicrolensing
   pip install -e ".[dev]"

This installs additional development dependencies for testing and documentation building.

Pre-commit Setup
~~~~~~~~~~~~~~~

To ensure code quality and consistency, set up pre-commit hooks:

.. code-block:: bash

   # Install pre-commit hooks
   pre-commit install

   # Run all hooks on all files (optional)
   pre-commit run --all-files

The pre-commit configuration includes:
- **Code formatting**: Black for consistent code style
- **Import sorting**: isort for organized imports
- **Linting**: flake8 for code quality checks
- **Type checking**: mypy for type safety
- **Security checks**: bandit for security vulnerabilities
- **Documentation**: pydocstyle for docstring consistency
- **Notebook formatting**: nbQA for Jupyter notebooks

These hooks will run automatically on every commit to ensure code quality.

Release Checklist
================

Follow these steps for each new release:

1. **Bump the version**
   - Update the version in `setup.py`.
   - Update the version and date in `CITATION.cff`.
   - Optionally update the version in `README.md` and documentation.

2. **Update citation and metadata**
   - Ensure `CITATION.cff` has the correct version, date, and DOI (if using Zenodo).
   - Add any new recommended citations for dependencies if needed.

3. **Commit and tag**
   - Commit all changes: `git commit -am "Release vX.Y.Z"`
   - Tag the release: `git tag vX.Y.Z`
   - Push: `git push && git push --tags`

4. **Create a GitHub Release**
   - Go to the GitHub Releases page and publish the new tag.

5. **Publish to PyPI**
   - Build and upload: `python -m build && twine upload dist/*`

6. **Check CI and documentation**
   - Ensure CI passes and ReadTheDocs builds the new docs.

7. **Verify badges**
   - Confirm that PyPI, CI, and ReadTheDocs badges are up to date in the README and docs.

Automated workflows will help with some of these steps, but always double-check before publishing!
