# twoL1S.py
"""Binary-lens microlensing model implementation."""

import math

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import VBMicrolensing
from IPython.display import HTML
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D


class TwoLens1S:
    """Binary-lens, single-source (2L1S) model.

    Examples
    --------
    >>> model = TwoLens1S(t0=0.0, tE=20.0, rho=0.01,
    ...                  u0_list=[0.1], q=0.1, s=1.5, alpha=45)
    >>> model.plot_light_curve()
    """

    def __init__(self, t0, tE, rho, u0_list, q, s, alpha, t_lc=None):
        """Create a binary-lens system.

        Parameters
        ----------
        t0 : float
            Time of closest approach.
        tE : float
            Einstein crossing time.
        rho : float
            Source radius in units of the Einstein radius.
        u0_list : list of float
            Impact parameters of the source trajectory.
        q : float
            Lens mass ratio ``m2/m1``.
        s : float
            Separation between the lenses in Einstein radii.
        alpha : float
            Angle of the source trajectory in degrees.
        t_lc : array_like, optional
            Custom times for light curve calculation. If None, uses default tau range.
        """
        self.t0 = t0
        self.tE = tE
        self.rho = rho
        self.u0_list = u0_list
        self.q = q
        self.s = s
        self.alpha = alpha
        self.tau = np.linspace(-4, 4, 1000)
        self.t = self.t0 + self.tau * self.tE
        self.theta = np.radians(self.alpha)

        if t_lc is not None:
            self.t_lc = np.array(t_lc)
            self.tau_lc = (self.t_lc - self.t0) / self.tE
        else:
            self.tau = np.linspace(-4, 4, 100)
            self.t_lc = self.t0 + self.tau * self.tE
            self.tau_lc = self.tau

        self.tau_hr = np.linspace(-4, 4, 1000)
        self.t_hr = self.t0 + self.tau_hr * self.tE

        self.VBM = VBMicrolensing.VBMicrolensing()
        self.VBM.RelTol = 1e-3
        self.VBM.Tol = 1e-3
        self.VBM.astrometry = True
        self.colors = [plt.colormaps["BuPu"](i) for i in np.linspace(1.0, 0.4, len(u0_list))]
        self.systems = self._prepare_systems()

    def _prepare_systems(self):
        """Precompute source trajectories and magnifications."""
        systems = []

        def polygon_area(x, y):
            return 0.5 * np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

        for u0, color in zip(self.u0_list, self.colors):
            x_src = self.tau * np.cos(self.theta) - u0 * np.sin(
                self.theta
            )  # for animation (lower resolution)
            y_src = self.tau * np.sin(self.theta) + u0 * np.cos(self.theta)

            cent_x = []
            cent_y = []

            for x_s, y_s in zip(x_src, y_src):
                images = self.VBM.ImageContours(self.s, self.q, x_s, y_s, self.rho)

                image_fluxes = []
                image_cx = []
                image_cy = []

                for img in images:
                    x = np.array(img[0])
                    y = np.array(img[1])
                    flux = polygon_area(x, y)

                    if flux > 0:
                        cx = np.mean(x)
                        cy = np.mean(y)
                        image_fluxes.append(flux)
                        image_cx.append(cx)
                        image_cy.append(cy)

                total_flux = np.sum(image_fluxes)

                if total_flux > 0:
                    cx_weighted = np.sum(np.array(image_cx) * image_fluxes) / total_flux
                    cy_weighted = np.sum(np.array(image_cy) * image_fluxes) / total_flux
                else:
                    cx_weighted = np.nan
                    cy_weighted = np.nan

                cent_x.append(cx_weighted)
                cent_y.append(cy_weighted)

            x_src_hr = self.tau_hr * np.cos(self.theta) - u0 * np.sin(
                self.theta
            )  # for centroid shift, higher resolution
            y_src_hr = self.tau_hr * np.sin(self.theta) + u0 * np.cos(self.theta)

            cent_x_hr = []
            cent_y_hr = []

            for x_s, y_s in zip(x_src_hr, y_src_hr):
                images = self.VBM.ImageContours(self.s, self.q, x_s, y_s, self.rho)

                image_fluxes, image_cx, image_cy = [], [], []

                for img in images:
                    x = np.array(img[0])
                    y = np.array(img[1])
                    flux = polygon_area(x, y)

                    if flux > 0:
                        cx = np.mean(x)
                        cy = np.mean(y)
                        image_fluxes.append(flux)
                        image_cx.append(cx)
                        image_cy.append(cy)

                total_flux = np.sum(image_fluxes)

                if total_flux > 0:
                    cx_weighted = np.sum(np.array(image_cx) * image_fluxes) / total_flux
                    cy_weighted = np.sum(np.array(image_cy) * image_fluxes) / total_flux
                else:
                    cx_weighted = np.nan
                    cy_weighted = np.nan

                cent_x_hr.append(cx_weighted)
                cent_y_hr.append(cy_weighted)

            # Compute centroid at light curve times (t_lc / tau_lc)
            x_src_lc = self.tau_lc * np.cos(self.theta) - u0 * np.sin(self.theta)
            y_src_lc = self.tau_lc * np.sin(self.theta) + u0 * np.cos(self.theta)

            cent_x_lc = []
            cent_y_lc = []

            for x_s, y_s in zip(x_src_lc, y_src_lc):
                images = self.VBM.ImageContours(self.s, self.q, x_s, y_s, self.rho)

                image_fluxes, image_cx, image_cy = [], [], []

                for img in images:
                    x = np.array(img[0])
                    y = np.array(img[1])
                    flux = polygon_area(x, y)

                    if flux > 0:
                        cx = np.mean(x)
                        cy = np.mean(y)
                        image_fluxes.append(flux)
                        image_cx.append(cx)
                        image_cy.append(cy)

                total_flux = np.sum(image_fluxes)

                if total_flux > 0:
                    cx_weighted = np.sum(np.array(image_cx) * image_fluxes) / total_flux
                    cy_weighted = np.sum(np.array(image_cy) * image_fluxes) / total_flux
                else:
                    cx_weighted = np.nan
                    cy_weighted = np.nan

                cent_x_lc.append(cx_weighted)
                cent_y_lc.append(cy_weighted)

            mag, *_ = self.VBM.BinaryLightCurve(
                [
                    math.log(self.s),
                    math.log(self.q),
                    u0,
                    self.theta,
                    math.log(self.rho),
                    math.log(self.tE),
                    self.t0,
                ],
                self.t_lc,
            )

            systems.append(
                {
                    "u0": u0,
                    "color": color,
                    "mag": mag,
                    "x_src": x_src,
                    "y_src": y_src,
                    "cent_x": np.array(cent_x),
                    "cent_y": np.array(cent_y),
                    "x_src_hr": x_src_hr,
                    "y_src_hr": y_src_hr,
                    "cent_x_hr": np.array(cent_x_hr),
                    "cent_y_hr": np.array(cent_y_hr),
                    "x_src_lc": x_src_lc,
                    "y_src_lc": y_src_lc,
                    "cent_x_lc": np.array(cent_x_lc),
                    "cent_y_lc": np.array(cent_y_lc),
                }
            )

        return systems

    def plot_caustic_critical_curves(self):
        """Plot caustics and critical curves for the binary lens."""
        caustics = self.VBM.Caustics(self.s, self.q)
        criticalcurves = self.VBM.Criticalcurves(self.s, self.q)

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
        q_handle = Line2D([0], [0], color="k", linestyle="None", label=rf"$q$ = {self.q}")
        s_handle = Line2D([0], [0], color="k", linestyle="None", label=rf"$s$ = {self.s}")

        plt.figure(figsize=(6, 6))

        for cau in caustics:
            plt.plot(cau[0], cau[1], "r", lw=1.2)
        for crit in criticalcurves:
            plt.plot(crit[0], crit[1], "k--", lw=0.8)

        x1 = -self.s * self.q / (1 + self.q)
        x2 = self.s / (1 + self.q)
        plt.plot([x1, x2], [0, 0], "ko")

        for system in self.systems:
            plt.plot(system["x_src"], system["y_src"], "--", color=system["color"], alpha=0.6)

        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        plt.xlabel(r"$\theta_x$ ($\theta_E$)")
        plt.ylabel(r"$\theta_y$ ($\theta_E$)")
        plt.title("2L1S Lensing Event")
        plt.gca().set_aspect("equal")
        plt.grid(True)
        plt.legend(
            handles=[
                lens_handle,
                caustic_handle,
                crit_curve_handle,
                q_handle,
                s_handle,
            ],
            loc="upper right",
            prop={"size": 8},
        )
        plt.tight_layout()
        plt.show()

    def plot_light_curve(self):
        """Plot the binary-lens light curve."""
        plt.figure(figsize=(6, 4))

        for system in self.systems:
            plt.plot(
                self.tau_lc,
                system["mag"],
                color=system["color"],
                label=rf"$u_0$ = {system['u0']}",
            )

        plt.xlabel(r"Time ($\tau$)")
        plt.ylabel("Magnification")
        plt.title("Light Curve")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_centroid_trajectory(self):
        """Plot the centroid shift trajectory."""
        plt.figure(figsize=(6, 6))
        for system in self.systems:
            delta_x = system["cent_x_hr"] - system["x_src_hr"]
            delta_y = system["cent_y_hr"] - system["y_src_hr"]
            plt.plot(delta_x, delta_y, color=system["color"], label=rf"$u_0$ = {system['u0']}")
        plt.xlabel(r"$\delta \Theta_1$")
        plt.ylabel(r"$\delta \Theta_2$")
        plt.gca().set_aspect("equal")
        plt.title("Centroid Trajectory")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_centroid_shift(self):
        """Plot the centroid shift magnitude over time."""
        plt.figure(figsize=(6, 4))
        for system in self.systems:
            delta_x = system["cent_x_hr"] - system["x_src_hr"]
            delta_y = system["cent_y_hr"] - system["y_src_hr"]
            delta_theta = np.sqrt(delta_x**2 + delta_y**2)
            plt.plot(
                self.tau_hr, delta_theta, color=system["color"], label=rf"$u_0$ = {system['u0']}"
            )

        plt.xlabel(r"Time ($\tau$)")
        plt.ylabel(r"$|\delta \vec{\Theta}|$")
        plt.title(r"Centroid Shift over Time ($\tau$)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def animate(self):
        """Return an animation showing the event evolution.

        Returns
        -------
        IPython.display.HTML
            HTML representation of the animation for use in notebooks.
        """
        caustics = self.VBM.Caustics(self.s, self.q)
        criticalcurves = self.VBM.Criticalcurves(self.s, self.q)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.subplots_adjust(wspace=0.4)

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
        q_handle = Line2D([0], [0], color="k", linestyle="None", label=rf"$q$ = {self.q}")
        s_handle = Line2D([0], [0], color="k", linestyle="None", label=rf"$s$ = {self.s}")

        ax1.set_xlim(-2, 2)
        ax1.set_ylim(-2, 2)
        ax1.set_xlabel(r"$\theta_x$ ($\theta_E$)")
        ax1.set_ylabel(r"$\theta_y$ ($\theta_E$)")
        ax1.set_title("2L1S Microlensing Event")
        ax1.set_aspect("equal")
        ax1.grid(True)

        for cau in caustics:
            ax1.plot(cau[0], cau[1], "r", lw=1.2)
        for crit in criticalcurves:
            ax1.plot(crit[0], crit[1], "k--", lw=0.8)

        ax1.plot([-self.s * self.q / (1 + self.q), self.s / (1 + self.q)], [0, 0], "ko")

        ax1.legend(
            handles=[
                lens_handle,
                caustic_handle,
                crit_curve_handle,
                q_handle,
                s_handle,
            ],
            loc="upper right",
            prop={"size": 8},
        )

        source_dots = []
        for system in self.systems:
            ax1.plot(system["x_src"], system["y_src"], "--", color=system["color"], alpha=0.4)
            (src_dot,) = ax1.plot([], [], "*", color=system["color"], markersize=10)
            # cen_dot, = ax1.plot(
            #     [], [], 'x', color=system['color'], markersize=6,
            #     label=f"$u_0$ = {system['u0']}"
            # )
            source_dots.append(src_dot)
            # centroid_dots.append(cen_dot)
        ax1.legend(loc="lower right")

        ax2.set_xlim(self.tau_lc[0], self.tau_lc[-1])
        all_mag = np.concatenate([s["mag"] for s in self.systems])
        ax2.set_ylim(min(all_mag) * 0.95, max(all_mag) * 1.05)
        ax2.set_xlabel(r"Time ($\tau$)")
        ax2.set_ylabel("Magnification")
        ax2.set_title("Light Curve")

        tracer_dots = []
        for system in self.systems:
            ax2.plot(
                self.tau_lc,
                system["mag"],
                color=system["color"],
                label=f"$u_0$ = {system['u0']}",
            )
            (dot,) = ax2.plot([], [], "o", color=system["color"], markersize=6)
            tracer_dots.append(dot)
        ax2.legend()

        image_dots = []
        for system in self.systems:
            system_dots = []
            for _ in range(5):
                (img_dot,) = ax1.plot([], [], ".", color=system["color"], alpha=0.6, markersize=4)
                system_dots.append(img_dot)
            image_dots.append(system_dots)

        def update(i):
            artists = []
            for j, system in enumerate(self.systems):
                x_src = system["x_src"][i]
                y_src = system["y_src"][i]

                source_dots[j].set_data([x_src], [y_src])
                tracer_dots[j].set_data([self.tau_lc[i]], [system["mag"][i]])
                artists.extend([source_dots[j], tracer_dots[j]])

                images = self.VBM.ImageContours(self.s, self.q, x_src, y_src, self.rho)

                for k, img_dot in enumerate(image_dots[j]):
                    if k < len(images):
                        img_dot.set_data(images[k][0], images[k][1])
                        img_dot.set_alpha(0.6)
                    else:
                        img_dot.set_data([], [])
                        img_dot.set_alpha(0)
                    artists.append(img_dot)

            return artists

        ani = animation.FuncAnimation(fig, update, frames=len(self.t), interval=50, blit=True)
        plt.close(fig)
        return HTML(ani.to_jshtml())

    def show_all(self):
        """Display a grid of animations and plots."""
        fig = plt.figure(figsize=(9, 9), constrained_layout=True)
        gs = GridSpec(2, 2, figure=fig)

        # --- Top Left: Lensing Animation ---
        ax1 = fig.add_subplot(gs[0, 0])
        caustics = self.VBM.Caustics(self.s, self.q)
        criticalcurves = self.VBM.Criticalcurves(self.s, self.q)

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
        q_handle = Line2D([0], [0], color="k", linestyle="None", label=rf"$q$ = {self.q}")
        s_handle = Line2D([0], [0], color="k", linestyle="None", label=rf"$s$ = {self.s}")

        ax1.set_xlim(-2, 2)
        ax1.set_ylim(-2, 2)
        ax1.set_aspect("equal")
        ax1.grid(True)
        ax1.set_title("2L1S Lensing Event")
        for cau in caustics:
            ax1.plot(cau[0], cau[1], "r", lw=1.2)
        for crit in criticalcurves:
            ax1.plot(crit[0], crit[1], "k--", lw=0.8)
        x1 = -self.s * self.q / (1 + self.q)
        x2 = self.s / (1 + self.q)
        ax1.plot([x1, x2], [0, 0], "ko")
        ax1.set_ylabel(r"Y ($\theta_E$)")
        ax1.set_xlabel(r"X ($\theta_E$)")
        ax1.legend(
            handles=[
                lens_handle,
                caustic_handle,
                crit_curve_handle,
                q_handle,
                s_handle,
            ],
            loc="upper right",
            prop={"size": 8},
        )

        source_dots, tracer_dots, image_dots = [], [], []
        for system in self.systems:
            ax1.plot(system["x_src"], system["y_src"], "--", color=system["color"], alpha=0.4)
            (src_dot,) = ax1.plot([], [], "*", color=system["color"], markersize=10)
            source_dots.append(src_dot)

            dots = []
            for _ in range(5):
                (dot,) = ax1.plot([], [], ".", color=system["color"], alpha=0.6, markersize=4)
                dots.append(dot)
            image_dots.append(dots)

        # --- Top Right: Light Curve ---
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_xlim(self.tau_lc[0], self.tau_lc[-1])
        all_mag = np.concatenate([s["mag"] for s in self.systems])
        ax2.set_ylim(min(all_mag) * 0.95, max(all_mag) * 1.05)
        ax2.set_ylabel("Magnification")
        ax2.set_title("Light Curve")
        ax2.set_xlabel(r"Time ($\tau$)")

        for system in self.systems:
            ax2.plot(
                self.tau_lc,
                system["mag"],
                color=system["color"],
                label=rf"$u_0$ = {system['u0']}",
            )
            (dot,) = ax2.plot([], [], "o", color=system["color"], markersize=6)
            tracer_dots.append(dot)
            ax2.legend(prop={"size": 8})

        # --- Bottom Left: Centroid Trajectory ---
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.set_box_aspect(1)

        for system in self.systems:
            dx = system["cent_x_hr"] - system["x_src_hr"]
            dy = system["cent_y_hr"] - system["y_src_hr"]
            ax3.plot(dx, dy, color=system["color"], label=rf"$\rho$ = {self.rho}")
        # ax3.set_xlim(-1, 1)
        # ax3.set_ylim(-1, 1)
        ax3.set_title("Centroid Shift Trajectory")
        ax3.set_xlabel(r"$\delta \Theta_1$")
        ax3.set_ylabel(r"$\delta \Theta_2$")
        ax3.grid(True)
        ax3.set_aspect("equal")
        ax3.legend(prop={"size": 8})

        # --- Bottom Right: Centroid Shift vs Tau ---
        ax4 = fig.add_subplot(gs[1, 1])
        for system in self.systems:
            dx = system["cent_x_hr"] - system["x_src_hr"]
            dy = system["cent_y_hr"] - system["y_src_hr"]
            dtheta = np.sqrt(dx**2 + dy**2)
            ax4.plot(self.tau_hr, dtheta, color=system["color"])
        ax4.set_xlabel(r"Time ($\tau$)")
        ax4.set_ylabel(r"$|\delta \vec{\Theta}|$")
        ax4.set_title(r"Centroid Shift over Time ($\tau$)")
        ax4.grid(True)

        # fig.subplots_adjust(hspace=0.2, wspace=0.2)

        # --- Animate function ---
        def update(i):
            artists = []
            for j, system in enumerate(self.systems):
                x_s = system["x_src"][i]
                y_s = system["y_src"][i]
                source_dots[j].set_data([x_s], [y_s])
                tracer_dots[j].set_data([self.tau_lc[i]], [system["mag"][i]])
                artists.extend([source_dots[j], tracer_dots[j]])

                images = self.VBM.ImageContours(self.s, self.q, x_s, y_s, self.rho)
                for k, dot in enumerate(image_dots[j]):
                    if k < len(images):
                        dot.set_data(images[k][0], images[k][1])
                        dot.set_alpha(0.6)
                    else:
                        dot.set_data([], [])
                        dot.set_alpha(0)
                    artists.append(dot)
            return artists

        ani = animation.FuncAnimation(fig, update, frames=len(self.t), interval=50, blit=True)
        plt.close(fig)
        return HTML(ani.to_jshtml())
