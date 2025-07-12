GCMicrolensing Documentation
============================

Tools for simulating gravitational microlensing events with single, binary, and triple lens systems.

.. image:: https://img.shields.io/pypi/v/GCMicrolensing.svg
   :target: https://pypi.org/project/GCMicrolensing/
   :alt: PyPI version

.. image:: https://github.com/GregCuautle/SURP25/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/GregCuautle/SURP25/actions/workflows/ci.yml
   :alt: CI status

.. image:: https://readthedocs.org/projects/gcmicrolensing/badge/?version=latest
   :target: https://gcmicrolensing.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/pyversions/GCMicrolensing.svg
   :target: https://pypi.org/project/GCMicrolensing/
   :alt: Python versions

Overview
--------

GCMicrolensing is a Python package for simulating gravitational microlensing events. It provides comprehensive tools for modeling single lens, binary lens, and triple lens systems with both photometric (light curve) and astrometric (centroid shift) calculations.

Key Features
-----------

* **Single Lens Systems (1L1S)**: Point source and extended source light curves
* **Binary Lens Systems (2L1S)**: Complex caustic structures and light curves
* **Triple Lens Systems (3L1S)**: Advanced multi-lens simulations
* **Astrometric Calculations**: Centroid shift predictions
* **Interactive Animations**: Visualize lensing events in real-time
* **Multiple Backends**: VBMicrolensing and TripleLensing support

Quick Start
-----------

Install the package:

.. code-block:: bash

   pip install GCMicrolensing

Basic usage:

.. code-block:: python

   from GCMicrolensing.models import OneL1S

   # Create a single lens model
   model = OneL1S(t0=2450000, tE=20, rho=0.001, u0_list=[0.1, 0.5, 1.0])

   # Plot the light curve
   model.plot_light_curve()

   # Create an animation
   animation = model.animate()

Installation
-----------

.. toctree::
   :maxdepth: 2
   :caption: Installation

   installation

API Reference
------------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/models

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
