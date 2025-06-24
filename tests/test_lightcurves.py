import types
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.modules.setdefault("TripleLensing", types.ModuleType("TripleLensing"))
module = types.ModuleType("TestML");
for name in ["get_crit_caus", "getphis_v3", "get_allimgs_with_mu", "testing"]:
    setattr(module, name, lambda *args, **kwargs: None)
sys.modules["TestML"] = module
import numpy as np
import math
import VBMicrolensing
from GCMicrolensing import OneL1S, TwoLens1S


def test_onel1s_light_curve():
    t0 = 0.0
    tE = 1.0
    rho = 0.01
    u0 = 0.1
    model = OneL1S(t0, tE, rho, [u0])

    vb = VBMicrolensing.VBMicrolensing()
    vb.RelTol = 1e-3
    vb.Tol = 1e-3
    vb.astrometry = True

    expected = np.array([
        vb.ESPLMag2(math.sqrt(u0 ** 2 + tau ** 2), rho)
        for tau in model.tau
    ])
    actual = np.array([
        model.VBM.ESPLMag2(math.sqrt(u0 ** 2 + tau ** 2), rho)
        for tau in model.tau
    ])

    np.testing.assert_allclose(actual, expected, rtol=1e-6)


def test_twolens1s_light_curve():
    t0 = 0.0
    tE = 1.0
    rho = 0.01
    u0 = 0.1
    q = 1.0
    s = 1.5
    alpha = 0.0

    model = TwoLens1S(t0, tE, rho, [u0], q, s, alpha)
    system = model.systems[0]

    vb = VBMicrolensing.VBMicrolensing()
    vb.RelTol = 1e-3
    vb.Tol = 1e-3
    vb.astrometry = True

    params = [math.log(s), math.log(q), u0, math.radians(alpha), math.log(rho), math.log(tE), t0]
    expected, *_ = vb.BinaryLightCurve(params, model.t)

    np.testing.assert_allclose(system['mag'], expected, rtol=1e-6)

