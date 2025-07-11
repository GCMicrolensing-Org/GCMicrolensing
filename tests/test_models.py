import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for CI
import matplotlib.pyplot as plt

from GCMicrolensing.models import OneL1S, TwoLens1S, ThreeLens1SVBM, ThreeLens1S

def test_onel1s_instantiation_and_light_curve():
    """Test OneL1S model instantiation and light curve plotting."""
    model = OneL1S(t0=2450000, tE=20, rho=0.001, u0_list=[0.1, 0.5])
    
    # Test instantiation
    assert model.t0 == 2450000
    assert model.tE == 20
    assert model.rho == 0.001
    assert len(model.u0_list) == 2
    
    # Test light curve plotting (should not block)
    model.plot_light_curve()
    plt.close('all')  # Close all figures

def test_twolens1s_instantiation_and_light_curve():
    """Test TwoLens1S model instantiation and light curve plotting."""
    model = TwoLens1S(t0=2450000, tE=20, rho=0.001, u0_list=[0.1], q=0.5, s=1.2, alpha=45)
    
    # Test instantiation
    assert model.t0 == 2450000
    assert model.tE == 20
    assert model.rho == 0.001
    assert model.q == 0.5
    assert model.s == 1.2
    assert model.alpha == 45
    
    # Test light curve plotting (should not block)
    model.plot_light_curve()
    plt.close('all')  # Close all figures

def test_threelens1svbm_instantiation_and_light_curve():
    """Test ThreeLens1SVBM model instantiation and light curve plotting."""
    model = ThreeLens1SVBM(t0=2450000, tE=20, rho=0.001, u0_list=[0.1], 
                          q2=0.3, q3=0.1, s12=1.2, s23=0.8, alpha=45, psi=30)
    
    # Test instantiation
    assert model.t0 == 2450000
    assert model.tE == 20
    assert model.rho == 0.001
    assert model.q2 == 0.3
    assert model.q3 == 0.1
    assert model.s12 == 1.2
    assert model.s23 == 0.8
    assert model.alpha == 45
    assert model.psi == 30
    
    # Test light curve plotting (should not block)
    model.plot_light_curve()
    plt.close('all')  # Close all figures

def test_threelens1s_instantiation_and_light_curve():
    """Test ThreeLens1S model instantiation and light curve plotting."""
    model = ThreeLens1S(t0=2450000, tE=20, rho=0.001, u0_list=[0.1],
                       q2=0.3, q3=0.1, s2=1.2, s3=0.8, alpha_deg=45, psi_deg=30,
                       rs=0.001, secnum=8, basenum=4, num_points=100)
    
    # Test instantiation
    assert model.t0 == 2450000
    assert model.tE == 20
    assert model.rho == 0.001
    assert model.q2 == 0.3
    assert model.q3 == 0.1
    assert model.s2 == 1.2
    assert model.s3 == 0.8
    assert model.alpha_deg == 45
    assert model.psi_deg == 30
    
    # Test light curve plotting (should not block)
    model.plot_light_curve()
    plt.close('all')  # Close all figures 