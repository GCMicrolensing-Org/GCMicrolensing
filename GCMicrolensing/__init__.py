# GCMicrolensing/__init__.py

__version__ = '0.1.0'  # Start with a simple version number, update as you go!

"""High level interface for the :mod:`GCMicrolensing` package.

The package bundles simple classes for creating synthetic microlensing
light curves and centroid shifts.  It is intended for educational and
exploratory scientific use.
"""

from .models import OneL1S, TwoLens1S, ThreeLens1SVBM, ThreeLens1S 
