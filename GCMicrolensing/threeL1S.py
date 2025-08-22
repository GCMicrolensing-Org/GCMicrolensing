# threeL1S.py
"""Triple-lens microlensing model implementations."""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import VBMicrolensing
from IPython.display import HTML
from matplotlib.lines import Line2D

from .TestML import get_allimgs_with_mu, get_crit_caus, getphis_v3, testing
from .triplelens import TripleLensing


class ThreeLens1SVBM:
    """Triple-lens, single-source model using VBMicrolensing.

    Examples
    --------
    >>> model = ThreeLens1SVBM(t0=0.0, tE=20.0, rho=0.01, u0_list=[0.1],
    ...                        q2=0.1, q3=0.1, s12=1.2, s23=1.0,
    ...                        alpha=45.0, psi=30.0)
    >>> model.plot_light_curve()
    """

    def __init__(self, t0, tE, rho, u0_list, q2, q3, s12, s23, alpha, psi):
        """Initialise the VBMicrolensing triple-lens model.

        Parameters
        ----------
        t0 : float
            Time of closest approach.
        tE : float
            Einstein crossing time.
        rho : float
            Source size in Einstein radii.
        u0_list : list of float
            Impact parameters to compute.
        q2 : float
            Mass ratio of lens 2 relative to lens 1.
        q3 : float
            Mass ratio of lens 3 relative to lens 1.
        s12 : float
            Separation between lens 1 and 2 in Einstein radii.
        s23 : float
            Separation between lens 2 and 3 in Einstein radii.
        alpha : float
            Source trajectory angle in degrees.
        psi : float
            Angle between the second and third lens in degrees.
        """
        self.t0 = t0
        self.tE = tE
        self.rho = rho
        self.u0_list = u0_list
        self.q2 = q2
        self.q3 = q3
        self.s12 = s12
        self.s23 = s23
        self.alpha = alpha
        self.tau = np.linspace(-2, 2, 100)
        self.t = self.t0 + self.tau * self.tE
        self.theta = np.radians(self.alpha)
        self.psi = psi
        self.phi = np.radians(self.psi)

        self.VBM = VBMicrolensing.VBMicrolensing()
        self.VBM.RelTol = 1e-3
        self.VBM.Tol = 1e-3
        self.VBM.astrometry = True
        self.VBM.SetMethod(self.VBM.Method.Nopoly)

        # Initialize TripleLensing for image position calculations
        self.TRIL = TripleLensing.TripleLensing()

        self.colors = [plt.colormaps["BuPu"](i) for i in np.linspace(1.0, 0.4, len(u0_list))]
        self.systems = self._prepare_systems()

    def _prepare_systems(self):
        """Assemble source trajectories and magnifications."""
        systems = []
        for u0, color in zip(self.u0_list, self.colors):
            param_vec = [
                np.log(self.s12),
                np.log(self.q2),
                u0,
                self.alpha,
                np.log(self.rho),
                np.log(self.tE),
                self.t0,
                np.log(self.s23),
                np.log(self.q3),
                self.phi,
            ]

            mag, *_ = self.VBM.TripleLightCurve(param_vec, self.t)

            x_src = self.tau * np.cos(self.theta) - u0 * np.sin(self.theta)
            y_src = self.tau * np.sin(self.theta) + u0 * np.cos(self.theta)

            systems.append({"u0": u0, "color": color, "mag": mag, "x_src": x_src, "y_src": y_src})

        return systems

    def _setting_parameters(self):
        """Initialise the lens geometry in the VBM solver."""
        param = [
            np.log(self.s12),
            np.log(self.q2),
            self.u0_list[0],
            self.alpha,
            np.log(self.rho),
            np.log(self.tE),
            self.t0,
            np.log(self.s23),
            np.log(self.q3),
            self.phi,
        ]
        _ = self.VBM.TripleLightCurve(param, self.t)

    def _compute_lens_positions(self):
        """Return Cartesian positions of the three lenses."""
        x1, y1 = 0, 0
        x2, y2 = x1 + self.s12, y1
        x3 = self.s23 * np.cos(self.phi)
        y3 = self.s23 * np.sin(self.phi)
        return [(x1, y1), (x2, y2), (x3, y3)]

    def _calculate_image_positions(self, xs, ys):
        """Solve the lens equation for a given source position.

        Parameters
        ----------
        xs, ys : float
            Coordinates of the source in units of the Einstein radius.

        Returns
        -------
        list[complex]
            Complex coordinates of the image positions.
        """
        mlens = [1 - self.q2 - self.q3, self.q2, self.q3]
        zlens = self._compute_lens_positions()
        zlens_cpp_format = [coord for pair in zlens for coord in pair]
        nlens = len(mlens)

        zrxy_flat = self.TRIL.solv_lens_equation(mlens, zlens_cpp_format, xs, ys, nlens)
        degree = nlens * nlens + 1
        real_parts = zrxy_flat[:degree]
        imag_parts = zrxy_flat[degree : 2 * degree]

        return [complex(re, im) for re, im in zip(real_parts, imag_parts)]

    def _true_solution(self, z_image, xs, ys, so_leps=1e-10):
        """Check if ``z_image`` solves the lens equation.

        Parameters
        ----------
        z_image : complex
            Candidate image coordinate.
        xs, ys : float
            Source coordinates.
        so_leps : float, optional
            Numerical tolerance for the solution test.

        Returns
        -------
        bool
            ``True`` if the lens equation is satisfied.
        """
        mlens = [1 - self.q2 - self.q3, self.q2, self.q3]
        zlens = [complex(x, y) for x, y in self._compute_lens_positions()]
        zs = complex(xs, ys)
        dzs = zs - z_image
        for m, zl in zip(mlens, zlens):
            dzs += m / np.conj(z_image - zl)
        return abs(dzs) < so_leps

    def plot_caustic_critical_curves(self):
        """Visualise caustics and critical curves."""
        self._setting_parameters()
        caustics = self.VBM.Multicaustics()
        criticalcurves = self.VBM.Multicriticalcurves()

        plt.figure(figsize=(6, 6))
        lens_handle = Line2D(
            [0],
            [0],
            marker="o",
            color="k",
            linestyle="None",
            label="Lens",
            markersize=6,
        )
        caustic_handle = Line2D([0], [0], color="r", lw=1.2, label="Caustic")
        crit_curve_handle = Line2D(
            [0], [0], color="k", linestyle="--", lw=0.8, label="Critical Curve"
        )

        for cau in caustics:
            plt.plot(cau[0], cau[1], "r", lw=1.2)
        for crit in criticalcurves:
            plt.plot(crit[0], crit[1], "k--", lw=0.8)

        for system in self.systems:
            plt.plot(system["x_src"], system["y_src"], "--", color=system["color"], alpha=0.6)

        lens_positions = self._compute_lens_positions()
        for x, y in lens_positions:
            plt.plot(x, y, "ko", label="Lens")

        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        plt.xlabel(r"$\theta_x$ ($\theta_E$)")
        plt.ylabel(r"$\theta_y$ ($\theta_E$)")
        plt.title("3L1S Lensing Event")
        plt.gca().set_aspect("equal")
        plt.legend(handles=[lens_handle, caustic_handle, crit_curve_handle], loc="upper right")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_light_curve(self):
        """Plot the triple-lens light curve."""
        plt.figure(figsize=(6, 4))
        for system in self.systems:
            plt.plot(
                self.tau,
                system["mag"],
                color=system["color"],
                label=rf"$u_0$ = {system['u0']}",
            )
        plt.xlabel(r"Time ($\tau$)")
        plt.ylabel("Magnification")
        plt.title("Triple Lens Light Curve")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_different_q3_lc(self, q3_values, reference_q3=None, colormap="RdPu"):
        """Compare light curves for multiple ``q3`` values.

        Parameters
        ----------
        q3_values : sequence of float
            Values of the third mass fraction to compute light curves for.
        reference_q3 : float, optional
            Value used as a baseline when plotting residuals. If ``None`` the
            first entry of ``q3_values`` is used.
        colormap : str, optional
            Name of a matplotlib colormap for the different curves.
        """
        colors = [plt.colormaps[colormap](i) for i in np.linspace(0.5, 1, len(q3_values))]

        plt.figure(figsize=(8, 6))
        gs = plt.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.05)
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1], sharex=ax1)

        ref_q3 = reference_q3 if reference_q3 is not None else q3_values[0]
        ref_param = [
            np.log(self.s12),
            np.log(self.q2),
            self.u0_list[0],
            self.alpha,
            np.log(self.rho),
            np.log(self.tE),
            self.t0,
            np.log(self.s23),
            np.log(ref_q3),
            self.phi,
        ]
        ref_mag, *_ = self.VBM.TripleLightCurve(ref_param, self.t)

        for idx, q3 in enumerate(q3_values):
            color = colors[idx]
            param_vec = [
                np.log(self.s12),
                np.log(self.q2),
                self.u0_list[0],
                self.alpha,
                np.log(self.rho),
                np.log(self.tE),
                self.t0,
                np.log(self.s23),
                np.log(q3),
                self.phi,
            ]
            mag, *_ = self.VBM.TripleLightCurve(param_vec, self.t)

            label = rf"$q_3$ = {q3:.2e}"
            ax1.plot(self.tau, mag, label=label, color=color)
            residual = np.array(ref_mag) - np.array(mag)
            ax2.plot(self.tau, residual, color=color)

        ax1.set_ylabel("Magnification")
        ax1.set_title("Light Curve for Varying $q_3$")
        ax1.grid(True)
        ax1.legend()

        ax2.set_xlabel(r"Time ($\tau$)")
        ax2.set_ylabel("Residuals")
        ax2.axhline(0, color="gray", lw=0.5, ls="--")
        ax2.grid(True)

        plt.tight_layout()
        plt.show()


class ThreeLens1S:
    """Triple-lens model using a direct solver.

    Examples
    --------
    >>> model = ThreeLens1S(t0=0.0, tE=20.0, rho=0.01, u0_list=[0.1],
    ...                     q2=0.1, q3=0.1, s2=1.2, s3=1.0,
    ...                     alpha_deg=45.0, psi_deg=30.0,
    ...                     rs=0.01, secnum=10, basenum=50, num_points=100)
    >>> model.plot_light_curve()
    """

    def __init__(
        self,
        t0,
        tE,
        rho,
        u0_list,
        q2,
        q3,
        s2,
        s3,
        alpha_deg,
        psi_deg,
        rs,
        secnum,
        basenum,
        num_points,
    ):
        """Initialise the direct triple-lens solver.

        Parameters
        ----------
        t0 : float
            Time of closest approach.
        tE : float
            Einstein crossing time.
        rho : float
            Source radius in Einstein units.
        u0_list : list of float
            Impact parameters for which to compute trajectories.
        q2 : float
            Mass ratio of lens 2 relative to lens 1.
        q3 : float
            Mass ratio of lens 3 relative to lens 1.
        s2 : float
            Separation of lens 2 from lens 1 in Einstein radii.
        s3 : float
            Separation of lens 3 from lens 1 in Einstein radii.
        alpha_deg : float
            Source trajectory angle in degrees.
        psi_deg : float
            Orientation angle of the third lens in degrees.
        rs : float
            Source radius used by the solver.
        secnum : int
            Number of annuli used in contour integration.
        basenum : int
            Number of base points used in integration.
        num_points : int
            Number of time samples for the source trajectory.
        """
        self.t0 = t0
        self.tE = tE
        self.rho = rho
        self.u0_list = u0_list
        self.q2 = q2
        self.q3 = q3
        self.s2 = s2
        self.s3 = s3
        self.alpha_deg = alpha_deg
        self.psi_deg = psi_deg
        self.rs = rs
        self.secnum = secnum
        self.basenum = basenum
        self.num_points = num_points

        self.alpha_rad = np.radians(alpha_deg)
        self.psi_rad = np.radians(psi_deg)
        self.tau = np.linspace(-2, 2, num_points)
        self.t = self.t0 + self.tau * self.tE

        # Initialize TripleLensing for calculations
        self.TRIL = TripleLensing.TripleLensing()
        self.colors = [plt.colormaps["BuPu"](i) for i in np.linspace(1.0, 0.4, len(u0_list))]
        self.systems = self._prepare_systems()

        import VBMicrolensing

        self.VBM = VBMicrolensing.VBMicrolensing()
        self.VBM.RelTol = 1e-3
        self.VBM.Tol = 1e-3
        self.VBM.astrometry = True
        self.VBM.SetMethod(self.VBM.Method.Nopoly)

    def get_lens_geometry(self):
        """Return mass fractions and lens coordinates.

        Returns
        -------
        tuple of list
            ``(mlens, zlens)`` where ``mlens`` are the mass fractions and
            ``zlens`` contains the ``x`` and ``y`` coordinates of each lens.
        """
        m1 = 1 / (1 + self.q2 + self.q3)
        m2 = self.q2 * m1
        m3 = self.q3 * m1
        mlens = [m1, m2, m3]
        x1, y1 = 0.0, 0.0
        x2, y2 = self.s2, 0.0
        x3 = self.s3 * np.cos(self.psi_rad)
        y3 = self.s3 * np.sin(self.psi_rad)
        zlens = [x1, y1, x2, y2, x3, y3]
        return mlens, zlens

    def _prepare_systems(self):
        """Generate trajectories and centroid shifts for each ``u0``."""
        systems = []
        mlens, zlens = self.get_lens_geometry()
        z = [[zlens[0], zlens[1]], [zlens[2], zlens[3]], [zlens[4], zlens[5]]]
        critical, caustics = get_crit_caus(mlens, z, len(mlens))
        caus_x = np.array([pt[0] for pt in caustics])
        caus_y = np.array([pt[1] for pt in caustics])

        for idx, u0 in enumerate(self.u0_list):
            y1s = u0 * np.sin(self.alpha_rad) + self.tau * np.cos(self.alpha_rad)
            y2s = u0 * np.cos(self.alpha_rad) - self.tau * np.sin(self.alpha_rad)

            cent_x, cent_y = [], []
            for i in range(self.num_points):
                Phis = getphis_v3(
                    mlens,
                    z,
                    y1s[i],
                    y2s[i],
                    self.rs,
                    2000,
                    caus_x,
                    caus_y,
                    secnum=self.secnum,
                    basenum=self.basenum,
                    scale=10,
                )[0]
                imgXS, imgYS, imgMUs, *_ = get_allimgs_with_mu(
                    mlens, z, y1s[i], y2s[i], self.rs, len(mlens), Phis
                )

                if len(imgMUs) == 0 or sum(imgMUs) == 0:
                    cent_x.append(np.nan)
                    cent_y.append(np.nan)
                else:
                    cx = np.sum(np.array(imgMUs) * np.array(imgXS)) / np.sum(imgMUs)
                    cy = np.sum(np.array(imgMUs) * np.array(imgYS)) / np.sum(imgMUs)
                    cent_x.append(cx)
                    cent_y.append(cy)

            systems.append(
                {
                    "u0": u0,
                    "color": self.colors[idx],
                    "y1s": y1s,
                    "y2s": y2s,
                    "cent_x": np.array(cent_x),
                    "cent_y": np.array(cent_y),
                    "mlens": mlens,
                    "zlens": zlens,
                }
            )

        return systems

    def _prepare_highres_centroid(self):
        """Generate high-resolution centroid data."""
        systems = []
        mlens, zlens = self.get_lens_geometry()
        z = [[zlens[0], zlens[1]], [zlens[2], zlens[3]], [zlens[4], zlens[5]]]
        critical, caustics = get_crit_caus(mlens, z, len(mlens))
        caus_x = np.array([pt[0] for pt in caustics])
        caus_y = np.array([pt[1] for pt in caustics])

        highres_tau = np.linspace(-2, 2, 5 * self.num_points)

        for idx, u0 in enumerate(self.u0_list):
            y1s = u0 * np.sin(self.alpha_rad) + highres_tau * np.cos(self.alpha_rad)
            y2s = u0 * np.cos(self.alpha_rad) - highres_tau * np.sin(self.alpha_rad)

            cent_x, cent_y = [], []
            for i in range(len(highres_tau)):
                Phis = getphis_v3(
                    mlens,
                    z,
                    y1s[i],
                    y2s[i],
                    self.rs,
                    2000,
                    caus_x,
                    caus_y,
                    secnum=self.secnum,
                    basenum=self.basenum,
                    scale=10,
                )[0]
                imgXS, imgYS, imgMUs, *_ = get_allimgs_with_mu(
                    mlens, z, y1s[i], y2s[i], self.rs, len(mlens), Phis
                )

                if len(imgMUs) == 0 or sum(imgMUs) == 0:
                    cent_x.append(np.nan)
                    cent_y.append(np.nan)
                else:
                    cx = np.sum(np.array(imgMUs) * np.array(imgXS)) / np.sum(imgMUs)
                    cy = np.sum(np.array(imgMUs) * np.array(imgYS)) / np.sum(imgMUs)
                    cent_x.append(cx)
                    cent_y.append(cy)

            systems.append(
                {
                    "u0": u0,
                    "color": self.colors[idx],
                    "y1s": y1s,
                    "y2s": y2s,
                    "cent_x": np.array(cent_x),
                    "cent_y": np.array(cent_y),
                }
            )

        return systems

    def plot_caustics_and_critical(self):
        """Plot VBM caustics and critical curves."""
        param = [
            np.log(self.s2),
            np.log(self.q2),
            self.u0_list[0],
            self.alpha_deg,
            np.log(self.rho),
            np.log(self.tE),
            self.t0,
            np.log(self.s3),
            np.log(self.q3),
            self.psi_rad,
        ]
        _ = self.VBM.TripleLightCurve(param, self.t)  # sets internal lens geometry

        caustics = self.VBM.Multicaustics()
        criticalcurves = self.VBM.Multicriticalcurves()

        plt.figure(figsize=(6, 6))
        for c in caustics:
            plt.plot(c[0], c[1], "r", lw=1.2)
        for crit in criticalcurves:
            plt.plot(crit[0], crit[1], "k--", lw=0.8)

        lens_pos = self.get_lens_geometry()[1]
        for i in range(0, 6, 2):
            plt.plot(lens_pos[i], lens_pos[i + 1], "ko")

        plt.title("Caustics and Critical Curves (VBM)")
        plt.gca().set_aspect("equal")
        plt.grid(True)
        plt.show()

    def plot_light_curve(self):
        """Plot the light curve computed via VBM."""
        plt.figure(figsize=(6, 4))
        for u0, color in zip(self.u0_list, self.colors):
            param = [
                np.log(self.s2),
                np.log(self.q2),
                u0,
                self.alpha_deg,
                np.log(self.rho),
                np.log(self.tE),
                self.t0,
                np.log(self.s3),
                np.log(self.q3),
                self.psi_rad,
            ]
            mag, *_ = self.VBM.TripleLightCurve(param, self.t)
            plt.plot(self.tau, mag, color=color, label=rf"$u_0$ = {u0}")
        plt.xlabel(r"$\tau$")
        plt.ylabel("Magnification")
        plt.title("Triple Lens Light Curve (VBM)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_centroid_trajectory(self):
        """Plot centroid trajectories for all sources."""
        plt.figure(figsize=(6, 6))
        for system in self.systems:
            dx = system["cent_x"] - system["y1s"]
            dy = system["cent_y"] - system["y2s"]
            plt.plot(dx, dy, color=system["color"], label=rf"$u_0$ = {system['u0']}")
        plt.xlabel(r"$\theta_x$ ($\theta_E$)")
        plt.ylabel(r"$\theta_y$ ($\theta_E$)")
        plt.title("Centroid Shift Trajectories")
        plt.gca().set_aspect("equal")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_shift_vs_time(self):
        """Plot centroid shift amplitude for each source over time."""
        plt.figure(figsize=(8, 5))
        for system in self.systems:
            dx = system["cent_x"] - system["y1s"]
            dy = system["cent_y"] - system["y2s"]
            dtheta = np.sqrt(dx**2 + dy**2)
            plt.plot(
                self.tau,
                dtheta,
                label=rf"$u_0$ = {system['u0']}",
                color=system["color"],
            )
        plt.xlabel(r"$\tau$")
        plt.ylabel(r"$|\delta \vec{\Theta}|$")
        plt.title("Centroid Shift vs Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    def animate(self):
        """Create an animation using the direct solver.

        Returns
        -------
        IPython.display.HTML
            HTML representation of the animation for use in notebooks.
        """
        fig, ax = plt.subplots(figsize=(6, 6))

        def update(i):
            ax.cla()
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_aspect("equal")
            ax.set_title("Triple Lens Event Animation")
            for system in self.systems:
                testing(
                    ax,
                    system["mlens"],
                    system["zlens"],
                    system["y1s"][i],
                    system["y2s"][i],
                    self.rs,
                    secnum=self.secnum,
                    basenum=self.basenum,
                    full_trajectory=(system["y1s"], system["y2s"]),
                    cl=system["color"],
                )
            return (ax,)

        ani = animation.FuncAnimation(fig, update, frames=self.num_points, blit=False)
        plt.close(fig)
        self.last_animation = ani
        return HTML(ani.to_jshtml())

    def animate_combined(self):
        """Animation overlaying caustics and source motion.

        Returns
        -------
        IPython.display.HTML
            HTML representation of the animation for use in notebooks.
        """
        # First, prepare the caustics and critical curves once using VBM
        param = [
            np.log(self.s2),
            np.log(self.q2),
            self.u0_list[0],
            self.alpha_deg,
            np.log(self.rho),
            np.log(self.tE),
            self.t0,
            np.log(self.s3),
            np.log(self.q3),
            self.psi_rad,
        ]
        _ = self.VBM.TripleLightCurve(param, self.t)  # set lens geometry
        caustics = self.VBM.Multicaustics()
        criticalcurves = self.VBM.Multicriticalcurves()

        fig, ax = plt.subplots(figsize=(6, 6))

        def update(i):
            ax.cla()
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_aspect("equal")
            ax.set_title("Triple Lens Microlensing Event")

            # Plot VBM caustics and criticals
            for c in caustics:
                ax.plot(c[0], c[1], "r", lw=1.2)
            for crit in criticalcurves:
                ax.plot(crit[0], crit[1], "k--", lw=0.8)

            for system in self.systems:
                # Plot the full source trajectory
                ax.plot(system["y1s"], system["y2s"], "--", color=system["color"], alpha=0.5)

                # Plot source position at frame i
                ax.plot(system["y1s"][i], system["y2s"][i], "o", color=system["color"])

                # Plot the lens positions
                zlens = system["zlens"]
                ax.plot(zlens[0], zlens[1], "ko")
                ax.plot(zlens[2], zlens[3], "ko")
                ax.plot(zlens[4], zlens[5], "ko")

                # Optional: Plot image positions (using TripleLensing)
                imgXS, imgYS, imgMUs, *_ = get_allimgs_with_mu(
                    system["mlens"],
                    [[zlens[0], zlens[1]], [zlens[2], zlens[3]], [zlens[4], zlens[5]]],
                    system["y1s"][i],
                    system["y2s"][i],
                    self.rs,
                    len(system["mlens"]),
                    getphis_v3(
                        system["mlens"],
                        [
                            [zlens[0], zlens[1]],
                            [zlens[2], zlens[3]],
                            [zlens[4], zlens[5]],
                        ],
                        system["y1s"][i],
                        system["y2s"][i],
                        self.rs,
                        2000,
                        np.array([pt[0] for pt in caustics[0]]),  # Just using 1st loop
                        np.array([pt[1] for pt in caustics[0]]),
                        secnum=self.secnum,
                        basenum=self.basenum,
                        scale=10,
                    )[0],
                )

                if len(imgXS) > 0:
                    ax.scatter(
                        imgXS,
                        imgYS,
                        s=30,
                        edgecolors="black",
                        facecolors="none",
                        label="Images",
                    )

            return (ax,)

        ani = animation.FuncAnimation(fig, update, frames=self.num_points, blit=False)
        plt.close(fig)
        self.last_animation = ani
        return HTML(ani.to_jshtml())
