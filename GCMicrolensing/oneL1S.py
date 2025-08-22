# oneL1S.py
"""Single-lens microlensing model implementation."""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import VBMicrolensing
from matplotlib.gridspec import GridSpec


class OneL1S:
    """Simple single-lens single-source (1L1S) model.

    Parameters
    ----------
    t0 : float
        Time of closest approach.
    tE : float
        Einstein crossing time.
    rho : float
        Source size in units of the Einstein radius.
    u0_list : list of float
        Impact parameters to evaluate.

    Examples
    --------
    >>> model = OneL1S(t0=0.0, tE=20.0, rho=0.01, u0_list=[0.1])
    >>> model.plot_light_curve()
    """

    def __init__(self, t0, tE, rho, u0_list):

        self.t0 = t0
        self.tE = tE
        self.rho = rho
        self.u0_list = u0_list
        self.tau = np.linspace(-4, 4, 200)
        self.t = self.t0 + self.tau * self.tE
        self.tau_hr = np.linspace(-4, 4, 1000)
        self.t_hr = self.t0 + self.tau_hr * self.tE

        self.VBM = VBMicrolensing.VBMicrolensing()
        self.VBM.RelTol = 1e-3
        self.VBM.Tol = 1e-3
        self.VBM.astrometry = True

        self.colors = [plt.colormaps["BuPu"](i) for i in np.linspace(1.0, 0.4, len(u0_list))]
        self.systems = self._prepare_systems_single()

    def _prepare_systems_single(self):
        """Precompute source trajectories and centroids for single lens."""
        systems = []
        for u0, color in zip(self.u0_list, self.colors):
            # source track (high-res)
            x_src_hr = self.tau_hr
            y_src_hr = np.full_like(self.tau_hr, u0)
            u = np.sqrt(x_src_hr**2 + y_src_hr**2)
            theta = np.arctan2(y_src_hr, x_src_hr)

            # analytic 1L1S images (in θ_E units)
            sqrt_term = np.sqrt(u**2 + 4.0)
            r_plus = 0.5 * (u + sqrt_term)
            r_minus = 0.5 * (u - sqrt_term)

            # magnifications of each image
            A_tot = (u**2 + 2.0) / (u * sqrt_term)
            A_plus = 0.5 * (A_tot + 1.0)
            A_minus = 0.5 * (A_tot - 1.0)

            # flux-weighted centroid radius along the same angle θ
            r_cent = (A_plus * r_plus + A_minus * r_minus) / (A_plus + A_minus)

            # vector centroid (relative to lens at origin)
            cent_x_hr = r_cent * np.cos(theta)
            cent_y_hr = r_cent * np.sin(theta)

            systems.append(
                {
                    "u0": u0,
                    "color": color,
                    "x_src_hr": x_src_hr,
                    "y_src_hr": y_src_hr,
                    "cent_x_hr": cent_x_hr,
                    "cent_y_hr": cent_y_hr,
                }
            )
        return systems

    def plot_light_curve_on_ax(self, ax):
        """Plot magnification curve on an existing axis.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Axis instance to plot on.
        """
        cmap_es = plt.colormaps["BuPu"]
        colors_es = [cmap_es(i) for i in np.linspace(0.5, 1.0, len(self.u0_list))]
        cmap_ps = plt.colormaps["binary"]
        colors_ps = [cmap_ps(i) for i in np.linspace(0.5, 1.0, len(self.u0_list))]

        for idx, u0 in enumerate(self.u0_list):
            color_es = colors_es[idx]
            color_ps = colors_ps[idx]
            u = np.sqrt(u0**2 + self.tau**2)
            pspl_mag = [self.VBM.PSPLMag(ui) for ui in u]
            espl_mag = [self.VBM.ESPLMag2(ui, self.rho) for ui in u]

            ax.plot(self.tau, espl_mag, "-", color=color_es, label=f"ESPL $u_0$ = {u0}")
            ax.plot(
                self.tau,
                pspl_mag,
                "--",
                color=color_ps,
                label=f"PSPL $u_0$ = {u0}",
                alpha=0.7,
            )

        ax.set_xlabel(r"Time ($\tau$)")
        ax.set_ylabel("Magnification")
        ax.set_title("Single-Lens Magnification")
        ax.grid(True)
        ax.legend()

    def plot_centroid_shift_on_ax(self, ax):
        """Plot centroid shift versus time on ``ax``.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Axis to draw the centroid shift curve on.
        """
        cmap_cs = plt.colormaps["BuPu"]
        colors_cs = [cmap_cs(i) for i in np.linspace(0.5, 1.0, len(self.u0_list))]

        for idx, u0 in enumerate(self.u0_list):
            color_cs = colors_cs[idx]
            u = np.sqrt(u0**2 + self.tau**2)
            centroid_shift = [self.VBM.astrox1 - ui for ui in u]
            ax.plot(self.tau, centroid_shift, color=color_cs, label=f"$u_0$ = {u0}")

        ax.set_xlabel(r"Time ($\tau$)")
        ax.set_ylabel(r"Centroid Shift ($\Delta \theta$)")
        ax.set_title("Astrometric Centroid Shift")
        ax.grid(True)
        ax.legend()

    def plot_light_curve(self):
        """Display the light curve in a new figure."""
        fig, ax = plt.subplots(figsize=(8, 4))
        self.plot_light_curve_on_ax(ax)
        plt.show()

    def plot_centroid_shift(self):
        """Display the centroid shift curve in a new figure."""
        fig, ax = plt.subplots(figsize=(8, 4))
        self.plot_centroid_shift_on_ax(ax)
        plt.show()

    def animate(self, save_gif=None):
        """Return a HTML animation of the event.

        Parameters
        ----------
        save_gif : str, optional
            If provided, save the animation as a GIF file with this filename.
            Example: save_gif="microlensing_animation.gif"
        """
        ani = self._create_animation(figsize=(6, 6), layout="single", save_gif=save_gif)
        self.last_animation = ani
        return ani

    def show_all(self, save_gif=None):
        """Return an animation with light curve and centroid shift.

        Parameters
        ----------
        save_gif : str, optional
            If provided, save the animation as a GIF file with this filename.
            Example: save_gif="microlensing_full_animation.gif"
        """
        return self._create_animation(figsize=(14, 6), layout="grid", save_gif=save_gif)

    def _create_animation(self, figsize=(6, 6), layout="single", save_gif=None):
        """Construct an animation of the microlensing event.

        Parameters
        ----------
        figsize : tuple of float, optional
            Size of the matplotlib figure in inches. Defaults to ``(6, 6)``.
        layout : {{'single', 'grid'}}, optional
            ``'grid'`` will also display the light curve and centroid shift
            during the animation. Defaults to ``'single'``.
        save_gif : str, optional
            If provided, save the animation as a GIF file with this filename.

        Returns
        -------
        matplotlib.animation.FuncAnimation
            Animation object for the microlensing event.
        """
        tau = self.tau
        n = len(self.t)
        colors = [plt.colormaps["BuPu"](i) for i in np.linspace(0.5, 1.0, len(self.u0_list))]

        systems = []
        for u0, color in zip(self.u0_list, colors):
            x_source = tau
            y_source = np.full_like(tau, u0)
            u = np.sqrt(x_source**2 + y_source**2)
            espl_mag = [self.VBM.ESPLMag2(ui, self.rho) for ui in u]
            systems.append(
                {
                    "u0": u0,
                    "x": x_source,
                    "y": y_source,
                    "mag": espl_mag,
                    "color": color,
                }
            )

        if layout == "grid":
            fig = plt.figure(figsize=figsize)
            gs = GridSpec(2, 2, width_ratios=[1, 1])
            ax_anim = fig.add_subplot(gs[:, 0])
            ax_light = fig.add_subplot(gs[0, 1])
            ax_centroid = fig.add_subplot(gs[1, 1])
            self.plot_light_curve_on_ax(ax_light)
            self.plot_centroid_shift_on_ax(ax_centroid)
        else:
            fig, ax_anim = plt.subplots(figsize=figsize)

        ax_anim.set_xlim(-2, 2)
        ax_anim.set_ylim(-2, 2)
        ax_anim.set_xlabel(r"X ($\theta_E$)")
        ax_anim.set_ylabel(r"Y ($\theta_E$)")
        ax_anim.set_title("Single-Lens Microlensing Events")
        ax_anim.grid(True)
        ax_anim.set_aspect("equal")
        ax_anim.plot([0], [0], "ko", label="Lens")
        einstein_ring = plt.Circle(
            (0, 0), 1, color="green", fill=False, linestyle="--", linewidth=1.5
        )
        ax_anim.add_patch(einstein_ring)

        source_dots, img_dots, trails_1, trails_2, trail_data = [], [], [], [], []

        for system in systems:
            (s_dot,) = ax_anim.plot(
                [], [], "*", color=system["color"], label=f"$u_0$ = {system['u0']}"
            )
            i_dot = ax_anim.scatter([], [], color=system["color"], s=20)
            t1 = ax_anim.scatter([], [], color=system["color"], alpha=0.3)
            t2 = ax_anim.scatter([], [], color=system["color"], alpha=0.3)
            source_dots.append(s_dot)
            img_dots.append(i_dot)
            trails_1.append(t1)
            trails_2.append(t2)
            trail_data.append({"x1": [], "y1": [], "s1": [], "x2": [], "y2": [], "s2": []})

        ax_anim.legend(loc="lower left")

        def update(frame):
            for i, system in enumerate(systems):
                x_s = system["x"][frame]
                y_s = system["y"][frame]
                u = np.sqrt(x_s**2 + y_s**2)
                theta = np.arctan2(y_s, x_s)
                r_plus = (u + np.sqrt(u**2 + 4)) / 2
                r_minus = (u - np.sqrt(u**2 + 4)) / 2

                x1 = r_plus * np.cos(theta)
                y1 = r_plus * np.sin(theta)
                x2 = r_minus * np.cos(theta)
                y2 = r_minus * np.sin(theta)

                source_dots[i].set_data([x_s], [y_s])
                img_dots[i].set_offsets([[x1, y1], [x2, y2]])
                mag = system["mag"][frame]
                size = 20 * mag
                img_dots[i].set_sizes([size, size])

                trail_data[i]["x1"].append(x1)
                trail_data[i]["y1"].append(y1)
                trail_data[i]["s1"].append(size)
                trail_data[i]["x2"].append(x2)
                trail_data[i]["y2"].append(y2)
                trail_data[i]["s2"].append(size)

                trails_1[i].set_offsets(np.column_stack([trail_data[i]["x1"], trail_data[i]["y1"]]))
                trails_1[i].set_sizes(trail_data[i]["s1"])
                trails_2[i].set_offsets(np.column_stack([trail_data[i]["x2"], trail_data[i]["y2"]]))
                trails_2[i].set_sizes(trail_data[i]["s2"])

            return source_dots + img_dots + trails_1 + trails_2

        ani = animation.FuncAnimation(fig, update, frames=len(self.tau), interval=50, blit=True)
        plt.tight_layout()
        if save_gif:
            ani.save(save_gif, writer="pillow")
        plt.close(fig)
        self.last_animation = ani
        return ani
