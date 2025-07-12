"""TestML module for microlensing calculations and utilities."""

import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import TripleLensing
from IPython.display import HTML
from matplotlib.animation import FuncAnimation, writers
from mpl_toolkits import axes_grid1
from mpl_toolkits.axes_grid1.inset_locator import inset_axes as iax

TRIL = TripleLensing.TripleLensing()

NLENS = 3
DEGREE = NLENS**2 + 1

M_PI = math.pi
EPS = 1.0e-5

VERBOSE = False
verbose = False


font = {
    "family": "Times New Roman",
    "color": "k",
    "weight": "normal",
    "size": 17,
}
legend_tick_size = 17

font2 = {
    "family": "Times New Roman",
    "weight": "normal",
    "size": 20,
}

colors0 = []
for name, hex in matplotlib.colors.cnames.items():
    # print(name, hex)
    colors0.append(name)


def read_lens_system_triple(fileName):
    """Read lens system parameters from a triple lens data file.

    Parameters
    ----------
    fileName : str
        Path to the data file containing lens system parameters.

    Returns
    -------
    dict
        Dictionary containing lens parameters with keys: t0, u0, tE, s2, q2,
        alpha, s3, q3, psi, rs, xsCenter, ysCenter.

    Notes
    -----
    Expected file format: First line is header, second line contains space-separated
    parameter values in the order: t0, u0, tE, s2, q2, alpha, s3, q3, psi, rs.
    """
    # ../data/lens_system_triple.dat
    # t0, u0, tE, s2, q2, alpha, s3, q3, psi, rs
    f = open(fileName, "r")
    _ = f.readline()
    line1 = f.readline()
    f.close()
    lpara = line1.split(" ")
    lpara = (float(i) for i in lpara)
    spara = "t0,u0,tE,s2,q2,alpha,s3,q3,psi,rs,xsCenter,ysCenter".split(",")
    params = {}
    for s, l in zip(spara, lpara):
        params[s] = l
    return params


def read_timratio(fileName):
    """Read time ratio data from a C++ generated file.

    Parameters
    ----------
    fileName : str
        Path to the data file.

    Returns
    -------
    tuple of float
        Time in HJD, x-coordinate of source center, y-coordinate of source center.

    Notes
    -----
    Expected format: Single line with space-separated values in order:
    time, xs, ys, magnification. Only the first three values are returned.
    """
    # reading cpp generated light curve
    # four value, time in HJD, 2nd, 3rd are the coordinate (xs, ys) of source center,
    # the 4th is the corresponding magnification
    # fprintf(
    #     ftrilkv,
    #     "%.15f %.15f %.15f %.15f ",
    #     t_array[j],
    #     y1_array[j],
    #     y2_array[j],
    #     mag_array[j]
    # );
    f = open(fileName, "r")
    line = f.readline()
    cols = line.split(" ")[:-1]
    f.close()
    cols = np.array([float(i) for i in cols])
    # print(cols)
    return cols[0], cols[1], cols[2]


def read_cpplkv(fileName, raws=4):
    """Read C++ generated light curve data.

    Parameters
    ----------
    fileName : str
        Path to the data file.
    raws : int, optional
        Number of values per data point. Default is 4.

    Returns
    -------
    tuple
        If raws=4: (times, xs, ys, mags)
        If raws=5: (times, xs, ys, mags, iffinite)

    Notes
    -----
    Expected format: Single line with space-separated values in groups of 'raws'.
    For raws=4: time, xs, ys, magnification
    For raws=5: time, xs, ys, magnification, finite_source_flag
    """
    # reading cpp generated light curve
    # four value, time in HJD, 2nd, 3rd are the coordinate (xs, ys) of source
    # center, the 4th is the corresponding magnification
    # fprintf(ftrilkv, "%.15f %.15f %.15f %.15f ",
    #     t_array[j],
    #     y1_array[j],
    #     y2_array[j],
    #     mag_array[j]
    # );
    f = open(fileName, "r")
    line = f.readline()
    cols = line.split(" ")[:-1]
    f.close()
    cols = np.array([float(i) for i in cols])
    # print(fileName)
    # print("len(cols): ",len(cols))
    times = cols[::raws]
    xs = cols[1::raws]
    ys = cols[2::raws]
    mags = cols[3::raws]
    if raws == 5:
        iffinite = cols[4::raws]
        return times, xs, ys, mags, iffinite.astype(int)
    else:
        return times, xs, ys, mags


def read_cpplkv_adap(fileName):
    """Read C++ generated adaptive light curve data.

    Parameters
    ----------
    fileName : str
        Path to the data file.

    Returns
    -------
    tuple of numpy.ndarray
        Arrays of times and corresponding magnifications.

    Notes
    -----
    Expected format: Two lines, first line contains times, second line contains
    corresponding magnifications, both space-separated.
    """
    # reading cpp generated light curve
    # two rows, the first is the time HJD, the second is the corresponding
    # magnification
    f = open(fileName, "r")
    line1 = f.readline()
    times = line1.split(" ")[:-1]
    line2 = f.readline()
    mags = line2.split(" ")[:-1]
    f.close()
    times = np.array([float(i) for i in times])
    mags = np.array([float(i) for i in mags])
    return times, mags


def read_cppmap1c(fileName):
    """Read C++ generated magnification map data (single column format).

    Parameters
    ----------
    fileName : str
        Path to the data file.

    Returns
    -------
    numpy.ndarray
        Array containing all values from the file.

    Notes
    -----
    Expected format: Single line with space-separated values in groups of three:
    xs, ys, magnification for each point.
    """
    # reading cpp generated magnification map
    # three value, the coordinate (xs, ys) of source center ,the 3rd is the
    # corresponding magnification
    f = open(fileName, "r")
    line = f.readline()
    f.close()
    cols = line.split(" ")[:-1]
    cols = np.array([float(i) for i in cols])
    # xs = cols[::3]
    # ys = cols[1::3]
    # mags = cols[2::3]
    return cols


def read_cppmap(fileName):
    """Read C++ generated magnification map data.

    Parameters
    ----------
    fileName : str
        Path to the data file.

    Returns
    -------
    tuple of numpy.ndarray
        Arrays of x-coordinates, y-coordinates, and magnifications.

    Notes
    -----
    Expected format: Single line with space-separated values in groups of three:
    xs, ys, magnification for each point.
    """
    # reading cpp generated magnification map
    # three value, the coordinate (xs, ys) of source center ,the 3rd is the
    # corresponding magnification
    f = open(fileName, "r")
    line = f.readline()
    f.close()
    cols = line.split(" ")[:-1]
    cols = np.array([float(i) for i in cols])
    xs = cols[::3]
    ys = cols[1::3]
    mags = cols[2::3]
    return xs, ys, mags


def readTimeRarioData(fileName):
    """Read time ratio comparison data between VBBL and TripleLensing.

    Parameters
    ----------
    fileName : str
        Path to the data file.

    Returns
    -------
    tuple
        (rhos, timvbbls, timtrils) where:
        - rhos: List of source sizes
        - timvbbls: List of lists containing VBBL computation times
        - timtrils: List of lists containing TripleLensing computation times

    Notes
    -----
    Expected format: First line contains Nexp and Navg, second line contains
    all the data values in a specific arrangement for comparison.
    """
    f = open(fileName, "r")
    line = f.readline()
    cols = line.split(" ")[:-1]
    cols = np.array([float(i) for i in cols])
    Nexp = int(cols[0])
    Navg = int(cols[1])

    line = f.readline()
    cols = line.split(" ")[:-1]
    cols = np.array([float(i) for i in cols])
    f.close()

    print("Nexp, Navg, len(cols): ", Nexp, Navg, len(cols))

    # print(cols)
    # print("len(cols)",len(cols))

    rhos = []
    timvbbls = []
    timtrils = []
    for i in range(Nexp):
        timvbbls.append([])
        timtrils.append([])
        for j in range(Navg):
            # print("i*(3*Navg)+j*Navg+1: ", i*(3*Navg)+j*Navg+1)
            # print("i = %d, j = %d, idx = %d"%(i,j,i*(3*Navg)+j*3+1))
            timvbbls[i].append(cols[i * (3 * Navg) + j * 3 + 1])
            timtrils[i].append(cols[i * (3 * Navg) + j * 3 + 2])
        rhos.append(cols[i * (3 * Navg)])
    print(rhos)
    timvbbls = [np.array(i) for i in timvbbls]
    timtrils = [np.array(i) for i in timtrils]
    return rhos, timvbbls, timtrils


def read_saveTrack(fileName, static=0, step=200, finalstep=10):
    """Read and display saved track data from a file.

    Parameters
    ----------
    fileName : str
        Path to the track data file.
    static : int, optional
        If 1, display static tracks. If 0, display animated tracks. Default is 0.
    step : int, optional
        Step size for animation. Default is 200.
    finalstep : int, optional
        Final step for animation. Default is 10.

    Notes
    -----
    Expected file format: First line contains segment lengths, second line contains
    track data in groups of 4: x1, x2, phi, mu.
    """
    f = open(fileName, "r")
    line = f.readline()
    seglens = line.split(" ")[:-1]
    # 2,3,4,3
    segnum = len(seglens)
    # 4
    seglens = np.array([int(i) for i in seglens])
    cumseglens = [sum(seglens[: i + 1]) for i in range(segnum)]
    # 2, 5, 9, 12

    line = f.readline()
    cols = line.split(" ")[:-1]
    cols = np.array([float(i) for i in cols])
    f.close()
    # p->x1, p->x2, p->phi, p->mu
    x1s = cols[::4]
    x2s = cols[1::4]
    # phis = cols[2::4]  # Unused variable
    # mus = cols[3::4]   # Unused variable
    if static:
        show_connected_tracks_static(x1s, x2s, cumseglens)
    else:
        show_connected_tracks(x1s, x2s, cumseglens, step=step, finalstep=finalstep)

    plt.show()


first = 1
cnt = 0


def show_connected_tracks(
    xs, ys, cumseglens, step=100, xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), finalstep=10
):
    """Display animated connected tracks with different colors for each segment.

    Parameters
    ----------
    xs : array-like
        X-coordinates of track points.
    ys : array-like
        Y-coordinates of track points.
    cumseglens : list
        Cumulative segment lengths defining track segments.
    step : int, optional
        Step size for animation. Default is 100.
    xlim : tuple, optional
        X-axis limits. Default is (-1.5, 1.5).
    ylim : tuple, optional
        Y-axis limits. Default is (-1.5, 1.5).
    finalstep : int, optional
        Final step for animation. Default is 10.

    Notes
    -----
    Creates an animated plot showing track segments in different colors,
    with the animation progressing through the track points.
    """
    connected_track_x = xs
    connected_track_y = ys
    lengthlist = [0] + cumseglens
    segnum = len(cumseglens)
    dc = len(colors0) // segnum
    # colors = colors0[::dc]
    # print(colors)

    Onetrack_length = len(connected_track_x)
    print(lengthlist)
    print("Total length: ", Onetrack_length)
    headx, heady, tailx, taily = [], [], [], []
    for j in range(len(lengthlist) - 1):
        headx.append(connected_track_x[lengthlist[j]])
        heady.append(connected_track_y[lengthlist[j]])
        tailx.append(connected_track_x[lengthlist[j + 1] - 1])
        taily.append(connected_track_y[lengthlist[j + 1] - 1])

    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.axis("equal")

    # connected_track_x, connected_track_y = Onetrack.toxylist()

    global cnt
    cnt = 0
    global first
    first = 0

    def update(i):
        global cnt
        global first
        plt.cla()
        for hx, hy, tx, ty, j in zip(headx, heady, tailx, taily, range(len(headx))):
            ax.text(hx - 0.01, hy, "{}".format(j), color="red")
            ax.text(tx + 0.01, ty, "{}".format(j), color="blue")
        ax.plot(headx, heady, "o", color="red", markersize=2)
        ax.plot(tailx, taily, "o", color="blue", markersize=2)
        ax.plot(
            connected_track_x[:i],
            connected_track_y[:i],
            ".",
            color="gray",
            markersize=2,
        )
        ax.plot(
            connected_track_x[i],
            connected_track_y[i],
            ".",
            color="green",
            markersize=8,
        )
        ax.text(
            0.8,
            1,
            "track_{},length_{}".format(cnt, lengthlist[cnt + 1] - lengthlist[cnt]),
        )
        if i >= lengthlist[cnt + 1]:
            if first:
                cnt += 1
                first = 0
            else:
                i >= lengthlist[cnt + 2]
                first = 1
        plt.draw()
        plt.xlim(xlim[0], xlim[1])
        plt.ylim(ylim[0], ylim[1])
        plt.pause(0.001)

    plt.ioff()
    s = np.arange(0, Onetrack_length, step)
    # print(
    #     "(Onetrack_length-s[-1]), step, (Onetrack_length-s[-1])//step",
    #     (Onetrack_length-s[-1]), step, (Onetrack_length-s[-1])//step
    # )
    # input()
    # s = np.concatenate([
    #     s,
    #     np.arange(s[-1],Onetrack_length,max(1, (Onetrack_length-s[-1])//10))
    # ])
    s = np.concatenate(
        [
            s,
            np.arange(s[-1], Onetrack_length, max(1, (Onetrack_length - s[-1]) // finalstep)),
        ]
    )
    try:
        s = np.concatenate([s, np.arange(s[-1], Onetrack_length, 1)])
    except Exception:
        pass
    ani = FuncAnimation(fig, update, frames=s, blit=False, interval=1000 / 2, save_count=300)
    print("Begin saving mp4")
    FFMpegWriter = writers["ffmpeg"]
    writer = FFMpegWriter(
        fps=5, metadata=dict(title="None", artist="None", comment="None"), bitrate=9600
    )
    mp4name = "./data/connected_track.mp4"
    ani.save(mp4name, writer=writer, dpi=240)
    print("Finished.")


def show_connected_tracks_static(
    xs, ys, cumseglens, step=100, xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), txt=1, inax=0
):
    """Display static connected tracks with different colors for each segment.

    Parameters
    ----------
    xs : array-like
        X-coordinates of track points.
    ys : array-like
        Y-coordinates of track points.
    cumseglens : list
        Cumulative segment lengths defining track segments.
    step : int, optional
        Step size (unused in static version). Default is 100.
    xlim : tuple, optional
        X-axis limits. Default is (-1.5, 1.5).
    ylim : tuple, optional
        Y-axis limits. Default is (-1.5, 1.5).
    txt : int, optional
        If 1, display head (H) and tail (T) labels. Default is 1.
    inax : int, optional
        If 1, create an inset axis. Default is 0.

    Notes
    -----
    Creates a static plot showing track segments in different colors,
    with optional head/tail labels and inset axis for detailed view.
    """
    connected_track_x = xs
    connected_track_y = ys
    lengthlist = [0] + cumseglens
    segnum = len(cumseglens)
    dc = len(colors0) // segnum
    colors = colors0[::dc]
    print(colors)

    Onetrack_length = len(connected_track_x)
    print(lengthlist)
    print("Total length: ", Onetrack_length)

    headx, heady, tailx, taily = [], [], [], []
    for j in range(len(lengthlist) - 1):
        headx.append(connected_track_x[lengthlist[j]])
        heady.append(connected_track_y[lengthlist[j]])
        tailx.append(connected_track_x[lengthlist[j + 1] - 1])
        taily.append(connected_track_y[lengthlist[j + 1] - 1])

    # plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(top=0.95, bottom=0.1, right=0.95, left=0.15, hspace=0, wspace=0)
    ax.tick_params(axis="both", labelsize=17, direction="in")

    # connected_track_x, connected_track_y = Onetrack.toxylist()

    global cnt
    cnt = 0
    global first
    first = 0
    # colors = ["blue", "green", "black", "red", "orange", "salmon", "lime"]

    scal = 3e-2
    scal = 3e-2
    for hx, hy, tx, ty, j in zip(headx, heady, tailx, taily, range(len(headx))):
        if txt:
            if (abs(hx - tx) < 1e-2) or (abs(hy - ty) < 1e-2):
                # input("KJLJKLJLJLJKJLJLK")
                ax.text(hx - 1.1 * scal, hy - 3 * scal, "H", color=colors[j], fontsize=27)
                ax.text(tx + 0.1 * scal, ty, "T", color=colors[j], fontsize=27)
            else:
                ax.text(hx - 1.1 * scal, hy - 3 * scal, "H", color=colors[j], fontsize=27)
                ax.text(tx + 0.1 * scal, ty, "T", color=colors[j], fontsize=27)
        ax.plot(hx, hy, "o", color=colors[j], markersize=4)
        ax.plot(tx, ty, "o", color=colors[j], markersize=4)
        # ax.plot(
        #     closed_tracks[j][0],
        #     closed_tracks[j][1],
        #     '.',
        #     color=colors[j],
        #     markersize=2
        # )
        ax.plot(
            connected_track_x[lengthlist[j] : lengthlist[j + 1]],
            connected_track_y[lengthlist[j] : lengthlist[j + 1]],
            ".",
            color=colors[j],
            markersize=2,
        )

    ax.set_xlabel(r"$x/ \theta_E $", fontsize=17, fontname="Times New Roman")
    ax.set_ylabel(r"$y/ \theta_E $", fontsize=17, fontname="Times New Roman")

    if inax:
        inset_axes = iax(
            ax,
            width="40%",  # width = 30% of parent_bbox
            height="40%",  # height : 1 inch
            loc=1,
        )  # 1 top right,
        for hx, hy, tx, ty, j in zip(headx, heady, tailx, taily, range(len(headx))):
            scal = 1e-3
            if txt:
                if (abs(hx - tx) < 1e-2) or (abs(hy - ty) < 1e-2):
                    inset_axes.text(hx - 1.1 * scal, hy, "H", color=colors[j], fontsize=27)
                    inset_axes.text(tx + 1.1 * scal, ty, "T", color=colors[j], fontsize=27)
                else:
                    inset_axes.text(hx - 1.1 * scal, hy, "H", color=colors[j], fontsize=27)
                    inset_axes.text(tx + 1.1 * scal, ty, "T", color=colors[j], fontsize=27)
            inset_axes.plot(hx, hy, "o", color=colors[j], markersize=4)
            inset_axes.plot(tx, ty, "o", color=colors[j], markersize=4)
            # inset_axes.plot(
            #     connected_track_x,
            #     connected_track_y,
            #     '.',
            #     color=colors[j],
            #     markersize=2
            # )
            inset_axes.plot(
                connected_track_x[lengthlist[j] : lengthlist[j + 1]],
                connected_track_y[lengthlist[j] : lengthlist[j + 1]],
                ".",
                color=colors[j],
                markersize=2,
            )

        inset_axes.tick_params(axis="both", labelsize=17, direction="in")

        # segm1
        # inset_axes.set_xlim(-0.4,-0.38)
        # inset_axes.set_ylim(1.155,1.175)

        # segm2 loc = 9
        # inset_axes.set_xlim(0.435,0.485)
        # inset_axes.set_ylim(-0.365,-0.315)

        # segm3
        inset_axes.set_xlim(-0.58, -0.55)
        inset_axes.set_ylim(0.835, 0.865)

    # plt.draw()
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(ylim[0], ylim[1])
    # print("???????? can you set xylim")
    ax.axis("equal")


def add_arrow(line, position=None, direction="right", size=15, color=None):
    """Add an arrow to a line plot.

    Parameters
    ----------
    line : matplotlib.lines.Line2D
        Line2D object to add arrow to.
    position : float, optional
        X-position of the arrow. If None, mean of xdata is taken.
    direction : {'left', 'right'}, optional
        Direction of the arrow. Default is 'right'.
    size : int, optional
        Size of the arrow in fontsize points. Default is 15.
    color : str, optional
        Color of the arrow. If None, line color is taken.

    Notes
    -----
    Based on solution from Stack Overflow for adding arrows to line plots.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == "right":
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate(
        "",
        xytext=(xdata[start_ind], ydata[start_ind]),
        xy=(xdata[end_ind], ydata[end_ind]),
        arrowprops=dict(arrowstyle="->", color=color),
        size=size,
    )


def draw_circle(ax, xsCenter, ysCenter, rs, color="b"):
    """Draw a filled circle on the given axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to draw the circle on.
    xsCenter : float
        X-coordinate of circle center.
    ysCenter : float
        Y-coordinate of circle center.
    rs : float
        Radius of the circle.
    color : str, optional
        Color of the circle. Default is 'b' (blue).

    Notes
    -----
    Creates a filled circle by generating points within the circle boundary
    and plotting them as a scatter plot.
    """
    xs = np.linspace(xsCenter - rs, xsCenter + rs, 100)
    ys = np.linspace(ysCenter - rs, ysCenter + rs, 100)
    r2 = rs**2
    X = []
    Y = []
    for x in xs:
        for y in ys:
            if (x - xsCenter) ** 2 + (y - ysCenter) ** 2 <= r2:
                X.append(x)
                Y.append(y)
    ax.scatter(X, Y, c=color)


def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot.

    Parameters
    ----------
    im : matplotlib.image.AxesImage
        Image object to add colorbar to.
    aspect : float, optional
        Aspect ratio of the colorbar. Default is 20.
    pad_fraction : float, optional
        Padding fraction for the colorbar. Default is 0.5.
    **kwargs
        Additional keyword arguments passed to colorbar.

    Returns
    -------
    matplotlib.colorbar.Colorbar
        The created colorbar object.
    """
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1.0 / aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


def cutsubimg4finiteSource(
    ImgSize,
    Rs,
    xlim,
    ylim,
    realimgsize,
    srcplaneIMG,
    srcplaneIMG_withoutlens,
    xlim0,
    xlim1,
    ylim0,
    ylim1,
):
    """Extract and process sub-images for finite source calculations.

    Parameters
    ----------
    ImgSize : tuple
        Size of the original image (width, height).
    Rs : float
        Source radius in pixels.
    xlim : tuple
        X-axis limits of the original image.
    ylim : tuple
        Y-axis limits of the original image.
    realimgsize : int
        Size of the real image grid.
    srcplaneIMG : numpy.ndarray
        Source plane image with lens.
    srcplaneIMG_withoutlens : numpy.ndarray
        Source plane image without lens.
    xlim0, xlim1 : float
        X-axis limits for the sub-image.
    ylim0, ylim1 : float
        Y-axis limits for the sub-image.

    Returns
    -------
    numpy.ndarray
        Magnification map for the finite source.

    Notes
    -----
    Creates a PSF kernel and applies it to extract magnification values
    for finite source calculations.
    """
    pixelRs = int(ImgSize[0] * Rs / (xlim[1] - xlim[0]))
    dx = (xlim1 - xlim0) / (realimgsize - 1)
    dy = (ylim1 - ylim0) / (realimgsize - 1)
    psf = np.zeros((2 * pixelRs + 1, 2 * pixelRs + 1))
    for i in range(1, 2 * pixelRs + 2):
        for j in range(1, 2 * pixelRs + 2):
            if ((i - pixelRs - 1) ** 2 + (j - pixelRs - 1) ** 2) <= pixelRs**2:
                psf[i - 1, j - 1] = 1
    print("psf: \n", psf.shape)
    muRayshoot = np.zeros((realimgsize, realimgsize))
    px = xlim0
    for i in range(realimgsize):
        py = ylim0
        for j in range(realimgsize):
            # pixelx = int((px - xlim[0])*(ImgSize[0]-1)/(xlim[1] - xlim[0]))
            # pixely = int((py - ylim[0])*(ImgSize[1]-1)/(ylim[1] - ylim[0]))
            pixelx = int((px - xlim[0]) * (ImgSize[0]) / (xlim[1] - xlim[0]))
            pixely = int((py - ylim[0]) * (ImgSize[1]) / (ylim[1] - ylim[0]))

            submap_wlens = srcplaneIMG[
                pixelx - pixelRs : pixelx + pixelRs + 1,
                pixely - pixelRs : pixely + pixelRs + 1,
            ]
            submap_wolens = srcplaneIMG_withoutlens[
                pixelx - pixelRs : pixelx + pixelRs + 1,
                pixely - pixelRs : pixely + pixelRs + 1,
            ]

            raynum_wlens = np.sum(submap_wlens * psf)
            raynum_wolens = np.sum(submap_wolens * psf)

            muRayshoot[j, i] = raynum_wlens / raynum_wolens
            py += dy
        px += dx
    return muRayshoot


def fmt(x, pos):
    """Format numbers in scientific notation for colorbar labels.

    Parameters
    ----------
    x : float
        Number to format.
    pos : int
        Position (unused, required by matplotlib).

    Returns
    -------
    str
        Formatted string in LaTeX scientific notation.

    Notes
    -----
    Based on Stack Overflow solution for scientific notation in colorbars.
    """
    a, b = "{:.2e}".format(x).split("e")
    b = int(b)
    return r"${} \times 10^{{{}}}$".format(a, b)


class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    """Custom formatter for controlling order of magnitude in colorbars.

    Parameters
    ----------
    order : int, optional
        Order of magnitude to use. Default is 0.
    fformat : str, optional
        Format string. Default is "%1.1f".
    offset : bool, optional
        Whether to use offset. Default is True.
    mathText : bool, optional
        Whether to use math text. Default is True.

    Notes
    -----
    Based on Stack Overflow solution for controlling scientific notation base.
    """

    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self, useOffset=offset, useMathText=mathText)

    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom

    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = r"$\mathdefault{%s}$" % self.format


# # https://stackoverflow.com/questions/17458580/embedding-small-plots-inside-subplots-in-matplotlib
# def add_subplot_axes(ax,rect,axisbg='w'):
#     fig = plt.gcf()
#     box = ax.get_position()
#     width = box.width
#     height = box.height
#     inax_position  = ax.transAxes.transform(rect[0:2])
#     transFigure = fig.transFigure.inverted()
#     infig_position = transFigure.transform(inax_position)
#     x = infig_position[0]
#     y = infig_position[1]
#     width *= rect[2]
#     height *= rect[3]  # <= Typo was here
#     subax = fig.add_axes([x,y,width,height],facecolor=axisbg)
#     x_labelsize = subax.get_xticklabels()[0].get_size()
#     y_labelsize = subax.get_yticklabels()[0].get_size()
#     x_labelsize *= rect[2]**0.5
#     y_labelsize *= rect[3]**0.5
#     subax.xaxis.set_tick_params(labelsize=x_labelsize)
#     subax.yaxis.set_tick_params(labelsize=y_labelsize)
#     return subax


def readFile(
    fileName,
    column1,
    column2,
    expected_elem_each_row=4,
):  # column number starts from 0
    """Read data from a file and extract two columns.

    Parameters
    ----------
    fileName : str
        Path to the data file.
    column1 : int
        Index of the first column to extract (0-based).
    column2 : int
        Index of the second column to extract (0-based).
    expected_elem_each_row : int, optional
        Expected number of elements per row. Default is 4.

    Returns
    -------
    tuple of list
        Two lists containing the extracted column data (x0, y0).
    """
    x0 = []
    y0 = []
    f = open(fileName, "r")
    for line in f:
        tempString = line.strip()
        if (tempString[0] == "#" or tempString[0] == "") or len(
            line.split()
        ) != expected_elem_each_row:
            continue
        line = line.split()
        x = np.float(line[column1])
        y = np.float(line[column2])
        x0.append(x)
        y0.append(y)
    f.close()
    return x0, y0


def FS_vs_VBBL():
    """Compare finite source (FS) and VBBL magnification and timing maps.

    Loads data from files, computes and displays relative errors and timing ratios
    between FS and VBBL methods using matplotlib plots.
    """
    ImgSize = 100
    x_min = -0.75
    x_max = 0.75
    y_max = 0.75
    y_min = -0.75
    print("loading mu.dat ...")
    line2list = []
    f = open("./data/fmuFS.dat", "r")
    for i in range(ImgSize):
        line2 = f.readline()
        line2list += line2.split(" ")[:-1]
    f.close()
    muFS = np.array([float(i) for i in line2list])
    muFS = muFS.reshape((ImgSize, ImgSize))

    line2list = []
    f = open("./data/fmuVBBL.dat", "r")
    for i in range(ImgSize):
        line2 = f.readline()
        line2list += line2.split(" ")[:-1]
    f.close()
    muVBBL = np.array([float(i) for i in line2list])
    muVBBL = muVBBL.reshape((ImgSize, ImgSize))

    line2list = []
    f = open("./data/fdtFS.dat", "r")
    for i in range(ImgSize):
        line2 = f.readline()
        line2list += line2.split(" ")[:-1]
    f.close()
    dtFS = np.array([float(i) for i in line2list])
    dtFS = dtFS.reshape((ImgSize, ImgSize))

    line2list = []
    f = open("./data/fdtVBBL.dat", "r")
    for i in range(ImgSize):
        line2 = f.readline()
        line2list += line2.split(" ")[:-1]
    f.close()
    dtVBBL = np.array([float(i) for i in line2list])
    dtVBBL = dtVBBL.reshape((ImgSize, ImgSize))

    cmap = "seismic"
    plt.figure(figsize=(18, 7))
    plt.subplot(231)
    plt.imshow(muVBBL, cmap=cmap, extent=[x_min, x_max, y_min, y_max])
    plt.title("Mu VBBL", fontdict=font)
    plt.colorbar()

    plt.subplot(232)
    plt.imshow((muFS - muVBBL) / muVBBL, cmap=cmap, extent=[x_min, x_max, y_min, y_max])
    plt.title("Rel err", fontdict=font)
    plt.colorbar()

    plt.subplot(233)
    plt.imshow(dtFS / dtVBBL, cmap=cmap, extent=[x_min, x_max, y_min, y_max])
    plt.title("Time new/VBBL", fontdict=font)
    plt.colorbar()

    print(
        " total time VBBL: {}, new method: {}, total time ratio: {} ".format(
            np.sum(dtVBBL), np.sum(dtFS), np.sum(dtFS) / np.sum(dtVBBL)
        )
    )

    timeratio = (dtFS / dtVBBL).reshape(-1, 1)
    plt.subplot(212)
    plt.hist(timeratio, bins=np.arange(min(timeratio), max(timeratio), 0.5))
    plt.show()


def plt_lightkv():
    """Load and return light curve data from 'mu.dat'.

    Returns
    -------
    tuple
        (pxs, full_line, head) where pxs is the x-axis, full_line is the y-data,
        and head contains header values from the file.
    """
    f = open("mu.dat", "r")
    head = f.readline().strip().split(" ")
    head = [float(i) for i in head]
    full_line = f.readline().strip().split(" ")
    full_line = [float(i) for i in full_line]
    pxs = np.linspace(head[0], head[1], int(head[2]))
    f.close()
    return pxs, full_line, head


def plotcritcaus():
    """Plot critical lines, caustics, lens, and image positions from data files."""
    print("Tracks function")
    fig, ax = plt.subplots(figsize=(8, 8))
    title = (
        "Critical lines (blue), caustics (red)\n "
        "source and lens (black), images (green) of "
        "triple lenses system\n yellow are the images "
        "of source centre"
    )
    plt.suptitle(title)
    x, y = readFile("./data/caustics.dat", 0, 1, expected_elem_each_row=2)
    ax.plot(x, y, "o", color="red", markersize=1)
    x, y = readFile("./data/critical_curves.dat", 0, 1, expected_elem_each_row=2)
    ax.plot(x, y, "o", color="blue", markersize=1)
    lensx, lensy = readFile("./data/lens_system.dat", 1, 2, expected_elem_each_row=3)
    lensm, _ = readFile("./data/lens_system.dat", 0, 2, expected_elem_each_row=3)
    for i in range(len(lensm) - 1):
        plt.plot(lensx[1 + i], lensy[1 + i], "o", color="k", markersize=5 * lensm[i + 1])
        plt.text(lensx[1 + i], lensy[1 + i], "lens{}".format(i + 1))
    print("plot pureImgPoints.dat")
    x, y = readFile("./data/pureImgPoints.dat", 0, 1, expected_elem_each_row=2)
    ax.plot(x, y, ".", color="green", markersize=3)
    f = open("./data/lens_system.dat", "r")
    full_line = f.readline()
    f.close()
    line = full_line.split()
    xs = np.float(line[0])
    ys = np.float(line[1])
    rs = np.float(line[2])
    print("xs, ys, rs in py", xs, ys, rs)
    nphi = 150
    phi = np.linspace(0.0, 2 * np.pi, nphi)
    x = xs + rs * np.cos(phi)
    y = ys + rs * np.sin(phi)
    ax.plot(x, y)
    plt.text(xs, ys, "src")
    plt.axis("equal")
    plt.show()


def plot_critcaus_srcimgs(
    mlens,
    zlens,
    xsCenter,
    ysCenter,
    rs,
    nphi=2000,
    NPS=4000,
    secnum=360,
    basenum=5,
    scale=10,
    pltfalseimg=True,
    title=False,
    srctext=False,
    xy=(0.3, 0.9),
    inst=False,
    xylim=(-0.1, 0.1, -0.1, 0.1),
    wh="32%",
    sci=False,
    cl="blue",
    axeq=1,
):
    """Plot critical curves, caustics, and image positions for a triple lens system.

    Parameters
    ----------
    mlens : list
        Lens masses.
    zlens : list
        Lens positions.
    xsCenter, ysCenter : float
        Source center coordinates.
    rs : float
        Source radius.
    ...
    (other parameters control plotting details)
    """
    # non-uniform phis
    z = [[zlens[0], zlens[1]], [zlens[2], zlens[3]], [zlens[4], zlens[5]]]
    nlens = len(mlens)
    if isinstance(axeq, int):
        fig, ax = plt.subplots(figsize=(8, 8))
    else:
        ax = axeq
    ax.tick_params(axis="both", labelsize=legend_tick_size, direction="in")
    critical, caustics = get_crit_caus(mlens, z, nlens, NPS=NPS)
    causticsx = np.array([xy[0] for xy in caustics])
    causticsy = np.array([xy[1] for xy in caustics])
    criticalx = [xy[0] for xy in critical]
    criticaly = [xy[1] for xy in critical]
    ax.plot(causticsx, causticsy, "-", color="red", markersize=1)
    ax.plot(criticalx, criticaly, "--", color="k", markersize=1)
    Phis = getphis_v3(
        mlens,
        z,
        xsCenter,
        ysCenter,
        rs,
        nphi,
        causticsx,
        causticsy,
        secnum=secnum,
        basenum=basenum,
        scale=scale,
    )
    Phis = Phis[0]
    imgXS, imgYS, XS, YS, falseimgXS, falseimgYS = get_allimgs_v2(
        mlens, z, xsCenter, ysCenter, rs, nlens, Phis
    )
    ax.plot([xy[0] for xy in z], [xy[1] for xy in z], ".", color="k", markersize=15)
    ax.plot(XS, YS, ".", color="k", markersize=1)
    ax.plot(imgXS, imgYS, ".", color=cl, markersize=1)
    if pltfalseimg:
        ax.plot(falseimgXS, falseimgYS, ".", color="gray", markersize=1, alpha=0.5)
    if srctext:
        for xy, m, i in zip(z, mlens, range(nlens)):
            ax.text(xy[0], xy[1], "m{}@{:.1e}".format(i + 1, m), fontdict=font)
    if sci == 1:
        ax.annotate(
            "(${:.1e}$, ${:.1e}$)".format(xsCenter, ysCenter),
            xy=xy,
            xycoords="axes fraction",
            fontsize=17,
            horizontalalignment="right",
            verticalalignment="bottom",
        )
    elif sci == 0:
        ax.annotate(
            "(${}$, ${}$)".format(xsCenter, ysCenter),
            xy=xy,
            xycoords="axes fraction",
            fontsize=17,
            horizontalalignment="right",
            verticalalignment="bottom",
        )
    ax.set_xlabel(r"$x/ \theta_E $", fontsize=17, fontname="Times New Roman")
    ax.set_ylabel(r"$y/ \theta_E $", fontsize=17, fontname="Times New Roman")
    if axeq:
        ax.set_aspect("equal")
    else:
        ax.set_xlim(-1.1, 1.6)
        ax.set_ylim(-1.3, 1.4)
    if title:
        plt.suptitle(
            """
    The three plus signs: the lens positions; The black circle: finite source
    The red solid and dashed curve: the caustics and critical curves.
    The cyan curves: true image trajectories; the blue curves: false image trajectories
    """,
            fontdict=font2,
        )
    if 0:
        plt.savefig("./data/topo_{}_{}_rs{}.png".format(xsCenter, ysCenter, rs), dpi=300)


def gamma_to_u(gamma):
    """Convert gamma to u for lensing calculations.

    Parameters
    ----------
    gamma : float
        Gamma value.

    Returns
    -------
    float
        Corresponding u value.
    """
    return 3.0 * gamma / (2.0 + gamma)


def u_to_gamma(u):
    """Convert u to gamma for lensing calculations.

    Parameters
    ----------
    u : float
        u value.

    Returns
    -------
    float
        Corresponding gamma value.
    """
    return (2.0 * u) / (3.0 - u)


def pltlkv(ts, mus, params=None, label=None):
    """Plot log-magnification light curve with optional parameters annotation.

    Parameters
    ----------
    ts : array-like
        Time values.
    mus : array-like
        Magnification values.
    params : list, optional
        Model parameters to annotate.
    label : str, optional
        Label for the curve.

    Returns
    -------
    tuple
        (main, gs) where main is the main axis and gs is the gridspec.
    """
    plt.figure(figsize=(13, 7), dpi=100)
    gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])
    plt.subplots_adjust(top=0.95, bottom=0.1, right=0.95, left=0.15, hspace=0, wspace=0)
    main = plt.subplot(gs[0])
    main.plot(ts, np.log10(mus), color="r", linewidth=2, label=label)
    main.set_ylabel(r"log($\mu$)", fontdict=font)
    main.set_xlabel("HJD - 2450000", fontdict=font)
    main.tick_params(axis="both", labelsize=legend_tick_size, direction="in")
    if params:
        msg = r"""
            $t_0$ = {}
            $u_0$ = {}
            $t_E$ = {} d
            $s_2$ = {}
            $q_2$ = {}
            $s_3$ = {}
            $q_3$ = {}
            $\alpha$ = {}
            $\psi$ = {}
            $\rho$ = {:.1e}
            """.format(
            params[0],
            params[1],
            params[2],
            params[3],
            params[4],
            params[6],
            params[7],
            params[5],
            params[8],
            params[9],
        )
        main.text(0.0, 0.4, msg, transform=main.transAxes, fontdict=font)
    return main, gs


def get_crit_caus(mlens, z, NLENS, NPS=200):
    """Compute critical curves and caustics for a triple lens system.

    Parameters
    ----------
    mlens : list
        Lens masses.
    z : list
        Lens positions as [[x1, y1], [x2, y2], [x3, y3]].
    NLENS : int
        Number of lenses.
    NPS : int, optional
        Number of points for calculation. Default is 200.

    Returns
    -------
    tuple
        (critical, caustics) as lists of [x, y] points.
    """
    zlens = [i[0] for i in z] + [i[1] for i in z]
    resxy = TRIL.outputCriticalTriple_list(mlens, zlens, NLENS, NPS)
    critical = []
    caustics = []
    numcrit = int(resxy[0])
    for i in range(numcrit):
        critical.append([resxy[2 * i + 1], resxy[2 * i + 2]])
    offset = 2 * numcrit + 1
    numcaus = int(resxy[offset])
    for i in range(numcaus):
        caustics.append([resxy[offset + 2 * i + 1], resxy[offset + 2 * i + 2]])
    return critical, caustics


def sol_len_equ_cpp(mlens, z, xsCenter, ysCenter, NLENS):
    """Solve the lens equation for a given source position using C++ backend.

    Parameters
    ----------
    mlens : list
        Lens masses.
    z : list
        Lens positions as [[x1, y1], ...].
    xsCenter, ysCenter : float
        Source center coordinates.
    NLENS : int
        Number of lenses.

    Returns
    -------
    list
        List of image positions as [x, y] pairs.
    """
    zlens = [i[0] for i in z] + [i[1] for i in z]
    resxy = TRIL.solv_lens_equation(mlens, zlens, xsCenter, ysCenter, NLENS)
    res = [[0, 0] for i in range(DEGREE)]
    for i in range(DEGREE):
        res[i][0] = resxy[i]
        res[i][1] = resxy[i + DEGREE]
    return res


def getphis_v3(
    mlens,
    z,
    xsCenter,
    ysCenter,
    rs,
    nphi,
    causticsx,
    causticsy,
    secnum=24,
    basenum=50,
    scale=10,
    psf=[0.7, 1, 0.7],
):
    """Compute non-uniform sampling angles (phis) for a source circle.

    Parameters
    ----------
    mlens : list
        Lens masses.
    z : list
        Lens positions.
    xsCenter, ysCenter : float
        Source center coordinates.
    rs : float
        Source radius.
    nphi : int
        Number of phis to sample.
    causticsx, causticsy : array-like
        Caustic curve x and y coordinates.
    secnum, basenum, scale, psf : optional
        Parameters controlling sampling.

    Returns
    -------
    tuple
        (PHI, distype, ...) where PHI is the array of angles.
    """
    # get phis non-uniformly
    distype = None  # away, almost, crossing
    dis = (causticsx - xsCenter) ** 2 + (causticsy - ysCenter) ** 2
    mindis = np.min(dis)
    mindixidx = np.argmin(dis)
    if mindis >= 4 * rs**2:
        if VERBOSE or verbose:
            print("away from caustics")
        distype = "away"
        nphi = max(nphi, 32)
        mindis_ang = myatan(causticsx[mindixidx] - xsCenter, causticsy[mindixidx] - ysCenter)
        phi0 = mindis_ang + M_PI
        PHI = np.linspace(phi0, 2.0 * M_PI + phi0, nphi, endpoint=True)
        return PHI, distype, phi0, nphi
    elif mindis >= rs**2:
        if VERBOSE or verbose:
            print("almost caustic crossing")
        distype = "almost"
        nphi = max(nphi, 32)
        qnphi = int(nphi / 4 + 0.5)
        scale = 1
        mindis_ang = myatan(causticsx[mindixidx] - xsCenter, causticsy[mindixidx] - ysCenter)
        PHI1 = np.linspace(mindis_ang - M_PI, mindis_ang - M_PI / 3, scale * qnphi, endpoint=False)
        PHI2 = np.linspace(
            mindis_ang - M_PI / 3,
            mindis_ang + M_PI / 3,
            4 * scale * qnphi,
            endpoint=False,
        )
        PHI3 = np.linspace(mindis_ang + M_PI / 3, mindis_ang + M_PI, scale * qnphi, endpoint=True)
        return np.concatenate([PHI1, PHI2, PHI3]), distype, mindis_ang, qnphi
    else:
        if VERBOSE or verbose:
            print("caustic crossing")
        distype = "crossing"
        PHI = np.linspace(0, 2.0 * M_PI, secnum, endpoint=False)
        XS = xsCenter + rs * np.cos(PHI)
        YS = ysCenter + rs * np.sin(PHI)
        mus = []
        for xs, ys in zip(XS, YS):
            mus.append(muPoint(mlens, z, xs, ys, NLENS))
        npmus = np.array(mus)
        ratiomin = 1
        maxmuidx = int((ratiomin * np.argmin(npmus) + (1 - ratiomin) * np.argmax(npmus)))
        npmus = np.convolve(npmus / np.min(npmus), psf, "same")
        npmus = npmus.astype(int) + 1
        secnumlist = list(range(maxmuidx, secnum)) + list(range(maxmuidx))
        offset = (np.array(range(secnum)) < maxmuidx) * 2 * M_PI
        dphi = 2 * M_PI / secnum / 2
        for i in secnumlist:
            if i == secnumlist[0]:
                PHI1 = np.linspace(
                    offset[i] + PHI[i] - dphi,
                    offset[i] + PHI[i] + dphi,
                    npmus[i] * basenum,
                    endpoint=False,
                )
            elif i == secnumlist[-1]:
                PHI2 = np.linspace(
                    offset[i] + PHI[i] - dphi,
                    offset[i] + PHI[i] + dphi,
                    npmus[i] * basenum,
                    endpoint=True,
                )
                PHI1 = np.concatenate([PHI1, PHI2])
            else:
                PHI2 = np.linspace(
                    offset[i] + PHI[i] - dphi,
                    offset[i] + PHI[i] + dphi,
                    npmus[i] * basenum,
                    endpoint=False,
                )
                PHI1 = np.concatenate([PHI1, PHI2])
        if VERBOSE:
            print("len PHI1: ", len(PHI1))
        PHI1 -= 2 * M_PI
        if PHI1[0] + 2 * M_PI > PHI1[-1]:
            PHI1 = np.concatenate(
                [PHI1[:-1], np.linspace(PHI1[-1], PHI1[0] + 2 * M_PI, 4, endpoint=True)]
            )
        return PHI1, distype, npmus, secnum, PHI, ratiomin, basenum


def get_allimgs_v2(mlens, z, xsCenter, ysCenter, rs, NLENS, Phis):
    """Compute all image positions for a set of source positions (non-uniform phis).

    Parameters
    ----------
    mlens : list
        Lens masses.
    z : list
        Lens positions.
    xsCenter, ysCenter : float
        Source center coordinates.
    rs : float
        Source radius.
    NLENS : int
        Number of lenses.
    Phis : array-like
        Angles to sample.

    Returns
    -------
    tuple
        (imgXS, imgYS, XS, YS, falseimgXS, falseimgYS)
    """
    XS = []
    YS = []
    imgXS = []
    imgYS = []
    falseimgXS = []
    falseimgYS = []
    for phi in Phis:
        xs = xsCenter + rs * math.cos(phi)
        ys = ysCenter + rs * math.sin(phi)
        XS.append(xs)
        YS.append(ys)
        res = sol_len_equ_cpp(mlens, z, xs, ys, NLENS)
        for i in range(DEGREE):
            flag = trueSolution(mlens, z, xs, ys, res[i], cal_ang=False)
            if flag[0]:
                imgXS.append(res[i][0])
                imgYS.append(res[i][1])
            else:
                falseimgXS.append(res[i][0])
                falseimgYS.append(res[i][1])
    return imgXS, imgYS, XS, YS, falseimgXS, falseimgYS


def myatan(x, y):
    """Return angle in [0, 2*pi] for given x, y coordinates."""
    if x >= 0 and y == 0:
        return 0
    if x == 0 and y > 0:
        return M_PI / 2
    if x == 0 and y < 0:
        return 3 * M_PI / 2
    if y == 0 and x < 0:
        return M_PI
    ang = np.arctan(y / x)
    if ang > 0:
        if y > 0:
            return ang
        else:
            return M_PI + ang
    else:
        if y < 0:
            return 2 * M_PI + ang
        else:
            return M_PI + ang


def checkLensEqu(mlens, zlens_list, xs, ys, z):
    """Check the lens equation for a given image position.

    Returns the absolute difference between the source position and the position
    computed from the lens equation using the provided image position.
    """
    zlens = []
    for i in range(len(zlens_list)):
        zlens.append(complex(zlens_list[i][0], zlens_list[i][1]))
    z = complex(z[0], z[1])  # solution to be checked
    zs = complex(xs, ys)
    dzs = zs - z
    for i in range(len(mlens)):
        dzs += mlens[i] / conj(z - zlens[i])
    return abs(dzs)


def trueSolution(mlens, zlens_list, xs, ys, z, cal_ang=True):
    """Check if a solution is a true image and compute magnification and Jacobian.

    Returns a list [flag, mu, lambda1, lambda2, thetaJ].
    """
    zlens = []
    for i in range(len(zlens_list)):
        zlens.append(complex(zlens_list[i][0], zlens_list[i][1]))
    z = complex(z[0], z[1])
    flag = 0
    Jxx = 1.0
    Jyy = 0.0
    Jxy = 0.0
    sum2 = 0.0
    sq = 0.0
    TINY = 1.0e-20
    lambda1, lambda2, thetaJ = 0, 0, 0
    mu = -1.0e10
    zs = complex(xs, ys)
    dzs = zs - z
    for i in range(len(mlens)):
        dzs += mlens[i] / conj(z - zlens[i])
    if abs(dzs) < EPS:
        flag = 1
        x = z.real
        y = z.imag
        for i in range(NLENS):
            dx = x - zlens[i].real
            dy = y - zlens[i].imag
            r2_1 = dx * dx + dy * dy + TINY
            Jxx += mlens[i] * (dx * dx - dy * dy) / (r2_1 * r2_1)
            Jxy += 2.0 * mlens[i] * dx * dy / (r2_1 * r2_1)
        Jyy = 2.0 - Jxx
        Jyx = Jxy
        mu = 1.0 / (Jxx * Jyy - Jxy * Jyx)
        if cal_ang:
            sum2 = (Jxx + Jyy) / 2.0
            sq = math.sqrt(sum2 * sum2 - 1.0 / mu)
            lambda1 = sum2 + sq
            lambda2 = sum2 - sq
            thetaJ = 0.5 * math.atan(2.0 * Jxy / (Jyy - Jxx + TINY))
            if thetaJ < 0.0:
                thetaJ += math.pi / 2.0
    return [flag, mu, lambda1, lambda2, thetaJ]


def muPoint(mlens, z, xsCenter, ysCenter, NLENS):
    """Compute the total magnification for a given source position."""
    res = sol_len_equ_cpp(mlens, z, xsCenter, ysCenter, NLENS)
    mu = 0
    for i in range(DEGREE):
        flag = trueSolution(mlens, z, xsCenter, ysCenter, res[i], cal_ang=False)
        if flag[0]:
            mu += abs(flag[1])
    return mu


def conj(z):
    """Return the complex conjugate of a complex number z."""
    return complex(z.real, -z.imag)


def testing(
    ax,
    mlens,
    zlens,
    xsCenter,
    ysCenter,
    rs,
    nphi=2000,
    NPS=4000,
    secnum=360,
    basenum=5,
    scale=10,
    cl="blue",
    plot_false=True,
    full_trajectory=None,
):
    """Plot a microlensing configuration with critical curves, caustics, and images."""
    z = [[zlens[0], zlens[1]], [zlens[2], zlens[3]], [zlens[4], zlens[5]]]
    nlens = len(mlens)
    critical, caustics = get_crit_caus(mlens, z, nlens, NPS=NPS)
    crit_x = [pt[0] for pt in critical]
    crit_y = [pt[1] for pt in critical]
    caus_x = [pt[0] for pt in caustics]
    caus_y = [pt[1] for pt in caustics]
    Phis = getphis_v3(
        mlens,
        z,
        xsCenter,
        ysCenter,
        rs,
        nphi,
        caus_x,
        caus_y,
        secnum=secnum,
        basenum=basenum,
        scale=scale,
    )[0]
    imgXS, imgYS, XS, YS, falseimgXS, falseimgYS = get_allimgs_v2(
        mlens, z, xsCenter, ysCenter, rs, nlens, Phis
    )
    ax.plot(crit_x, crit_y, "--", color="black", lw=1.2, label="Critical Curve")
    ax.plot(caus_x, caus_y, "-", color="red", lw=1.2, label="Caustic")
    ax.scatter(XS, YS, color="orange", marker="*", s=10, label="Source", zorder=3)
    ax.scatter(imgXS, imgYS, color=cl, s=10, label="Images", zorder=4)
    if plot_false:
        ax.scatter(falseimgXS, falseimgYS, color="gray", s=10, alpha=0.3, label="False Images")
    lens_x = [zlens[i] for i in range(0, len(zlens), 2)]
    lens_y = [zlens[i + 1] for i in range(0, len(zlens), 2)]
    ax.scatter(lens_x, lens_y, color="black", s=40, label="Lenses", zorder=5)
    if full_trajectory is not None:
        traj_x, traj_y = full_trajectory
        ax.plot(traj_x, traj_y, "--", color="orange", lw=0.8, label="Source Trajectory")
    ax.set_xlabel(r"$\\theta_E$", fontsize=14)
    ax.set_ylabel(r"$\\theta_E$", fontsize=14)
    ax.set_aspect("equal")
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), fontsize=8, loc="upper left")


def get_allimgs_with_mu(mlens, z, xsCenter, ysCenter, rs, NLENS, Phis):
    """Compute all image positions and magnifications for a set of source positions."""
    XS, YS = [], []
    imgXS, imgYS, imgMUs = [], [], []
    falseimgXS, falseimgYS = [], []
    for phi in Phis:
        xs = xsCenter + rs * math.cos(phi)
        ys = ysCenter + rs * math.sin(phi)
        XS.append(xs)
        YS.append(ys)
        res = sol_len_equ_cpp(mlens, z, xs, ys, NLENS)
        for i in range(DEGREE):
            flag = trueSolution(mlens, z, xs, ys, res[i], cal_ang=False)
            if flag[0]:
                imgXS.append(res[i][0])
                imgYS.append(res[i][1])
                imgMUs.append(abs(flag[1]))  # take abs(magnification)
            else:
                falseimgXS.append(res[i][0])
                falseimgYS.append(res[i][1])
    return imgXS, imgYS, imgMUs, XS, YS, falseimgXS, falseimgYS


class ThreeLens1STripleLens:
    """Class for simulating triple-lens single-source microlensing events."""

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
        """Initialize the triple-lens model parameters."""
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
        self.TRIL = TripleLensing.TripleLensing()
        self.colors = [plt.colormaps["BuPu"](i) for i in np.linspace(1.0, 0.4, len(u0_list))]
        self.systems = self._prepare_systems()

    def get_lens_geometry(self):
        """Return lens masses and positions for the triple-lens system."""
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
        """Prepare source trajectories and centroid shifts for each u0 value."""
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

    def plot_centroid_trajectory(self):
        """Plot centroid shift trajectories for all u0 values."""
        plt.figure(figsize=(6, 6))
        for system in self.systems:
            dx = system["cent_x"] - system["y1s"]
            dy = system["cent_y"] - system["y2s"]
            plt.plot(dx, dy, color=system["color"], label=rf"$u_0$ = {system['u0']}")
        plt.xlabel(r"$\\delta x/\\theta_E$")
        plt.ylabel(r"$\\delta y/\\theta_E$")
        plt.title("Centroid Shift Trajectories")
        plt.gca().set_aspect("equal")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_shift_vs_time(self):
        """Plot centroid shift magnitude as a function of time for all u0 values."""
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
        plt.xlabel(r"$\\tau$")
        plt.ylabel(r"$|\\delta \\vec{\\Theta}|$")
        plt.title("Centroid Shift vs Time")
        plt.legend()
        plt.grid(True)
        plt.show()

    def animate(self):
        """Return an animation of the triple-lens event as HTML."""
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

        ani = FuncAnimation(fig, update, frames=self.num_points, blit=False)
        plt.close(fig)
        return HTML(ani.to_jshtml())
