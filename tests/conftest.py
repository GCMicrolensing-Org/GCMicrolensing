"""
Pytest configuration for GCMicrolensing tests.

This file configures pytest to use non-interactive matplotlib backend
for CI environments and provides common fixtures.
"""

import pytest
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for CI

@pytest.fixture(autouse=True)
def setup_matplotlib():
    """Automatically set up matplotlib for non-interactive testing."""
    import matplotlib.pyplot as plt
    plt.ioff()  # Turn off interactive mode
    yield
    plt.close('all')  # Clean up all figures after each test 