"""High level models for simulating microlensing events.

This module provides simple classes for single-, double-, and triple-lens
microlensing scenarios.  The focus is on producing light curves, centroid
shifts and animated visualisations for teaching or exploratory analyses.

The implementations rely heavily on the `VBMicrolensing` and
`TripleLensing` packages for the low level calculations of image positions
and magnifications.

For backwards compatibility, this module re-exports all the classes from
their new dedicated modules.
"""

# Re-export classes from their dedicated modules for backwards compatibility
from .oneL1S import OneL1S
from .threeL1S import ThreeLens1S, ThreeLens1SVBM
from .twoL1S import TwoLens1S

__all__ = ["OneL1S", "TwoLens1S", "ThreeLens1S", "ThreeLens1SVBM"]
