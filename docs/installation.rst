Installation
===========

GCMicrolensing can be installed using pip or conda. The package requires Python 3.10 or higher.

Prerequisites
------------

* Python 3.10 or higher
* pip or conda package manager
* C++ compiler (for building dependencies)

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

   git clone https://github.com/GregCuautle/GCMicrolensing.git
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
2. Search existing issues on the `GitHub repository <https://github.com/GregCuautle/GCMicrolensing/issues>`_
3. Create a new issue with detailed error information

Development Installation
-----------------------

For developers who want to contribute to the project:

.. code-block:: bash

   git clone https://github.com/GregCuautle/GCMicrolensing.git
   cd GCMicrolensing
   pip install -e ".[dev]"
   pip install -r requirements-dev.txt

This installs additional development dependencies for testing and documentation building. 