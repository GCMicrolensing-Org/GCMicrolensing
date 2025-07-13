[![PyPI version](https://img.shields.io/pypi/v/GCMicrolensing.svg)](https://pypi.org/project/GCMicrolensing/)
[![CI](https://github.com/GCMicrolensing-Org/GCMicrolensing/actions/workflows/ci.yml/badge.svg)](https://github.com/GCMicrolensing-Org/GCMicrolensing/actions/workflows/ci.yml)
[![Read the Docs](https://readthedocs.org/projects/gcmicrolensing/badge/?version=latest)](https://gcmicrolensing.readthedocs.io/en/latest/?badge=latest)

# GCMicrolensing

Tools for simulating gravitational microlensing events with single, binary, and triple lens systems. This package is under active development.

## Installation

### Prerequisites

This package requires a custom version of `TripleLensing` with modifications by Gregory Costa Cuautle. The installation process depends on how you obtained this package:

#### Option 1: From Source (Recommended)
If you cloned this repository, the custom `TripleLensing` is included and will be installed automatically:

```bash
git clone https://github.com/GCMicrolensing-Org/GCMicrolensing.git
cd GCMicrolensing
pip install -e .
```

#### Option 2: Manual Installation
If you're installing from a distribution that doesn't include `TripleLensing`, you'll need to install it manually:

```bash
# First install GCMicrolensing
pip install GCMicrolensing

# Then install the custom TripleLensing (instructions to be provided)
# This requires the custom version with Greg's modifications
```

## Usage

```python
from GCMicrolensing.models import OneL1S, TwoLens1S, ThreeLens1S

# Create a single lens model
model = OneL1S(t0=2450000, tE=20, rho=0.001, u0_list=[0.1, 0.5, 1.0])
model.plot_light_curve()
```

## Dependencies

- **TripleLensing**: Custom version with modifications by Gregory Costa Cuautle
- **VBMicrolensing**: For binary lens calculations
- **Standard scientific Python stack**: numpy, matplotlib, scipy, astropy, etc.

## Documentation

See the `docs/` directory for detailed documentation.
This project uses a regular Python packaging workflow. To install the
package and its minimal runtime dependencies, execute::

    pip install .

The local `TripleLensing` library will be built and installed
automatically as part of this process.

For development a more feature rich environment can be created using the
`environment.yml` file.
