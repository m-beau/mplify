"""Scalebar utilities for matplotlib axes."""

import numpy as np


def plot_scalebar(ax, xscalebar=None, yscalebar=None,
                  x_unit="ms", y_unit="\u03BCV",
                  scalepad=0.025, fontsize=14, lw=3,
                  loc='right', offset_x=0, offset_y=0):
    """Add x and/or y scalebar to a matplotlib axis.

    Arguments:
        - ax: matplotlib axis
        - xscalebar: length of x scalebar in data units (None to skip)
        - yscalebar: length of y scalebar in data units (None to skip)
        - x_unit: unit label for x scalebar
        - y_unit: unit label for y scalebar
        - scalepad: padding between scalebar and label, as fraction of axis height
        - fontsize: scalebar label font size
        - lw: scalebar line width
        - loc: 'left' or 'right'
        - offset_x: horizontal offset as fraction of axis width
        - offset_y: vertical offset as fraction of axis height
    """
    if xscalebar is None and yscalebar is None:
        raise ValueError("Provide at least one of xscalebar or yscalebar.")
    if loc not in ('left', 'right'):
        raise ValueError(f"loc must be 'left' or 'right', got {loc!r}")

    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    axw, axh = np.diff(xlim)[0], np.diff(ylim)[0]
    bbox = ax.get_window_extent().transformed(
        ax.get_figure().dpi_scale_trans.inverted())
    axw_inch, axh_inch = bbox.width, bbox.height

    vpad = scalepad * axh
    hpad = scalepad * axw * (axh_inch / axw_inch)

    offset_x = float(offset_x * axw)
    offset_y = float(offset_y * axh)
    if loc == 'right':
        offset_x = offset_x - 0.1
    else:
        offset_x = offset_x + 0.1
    offset_y = offset_y + 0.1

    # x scalebar
    if xscalebar is not None:
        xscale_y = [ylim[0], ylim[0]]
        if yscalebar is None:
            text_pos_sign = 1
            xscale_va = "bottom"
        else:
            text_pos_sign = -1
            xscale_va = "top"
        if loc == 'right':
            xscale_x = [xlim[1] - xscalebar, xlim[1]]
        else:
            xscale_x = [xlim[0], xlim[0] + xscalebar]

        xscale_x = [x + offset_x for x in xscale_x]
        xscale_y = [y + offset_y for y in xscale_y]

        ax.plot(xscale_x, xscale_y, c='k', lw=lw)
        ax.text(xscale_x[0] + np.diff(xscale_x)[0] / 2,
                xscale_y[0] + vpad * text_pos_sign,
                f"{xscalebar}{x_unit}",
                ha="center", va=xscale_va, fontsize=fontsize)

    # y scalebar
    if yscalebar is not None:
        yscale_y = [ylim[0], ylim[0] + yscalebar]
        if xscalebar is None:
            if loc == 'right':
                text_pos_sign = -1
                yscale_ha = "right"
            else:
                text_pos_sign = 1
                yscale_ha = "left"
        else:
            if loc == 'right':
                text_pos_sign = 1
                yscale_ha = "left"
            else:
                text_pos_sign = -1
                yscale_ha = "right"
        if loc == 'right':
            yscale_x = [xlim[1], xlim[1]]
        else:
            yscale_x = [xlim[0], xlim[0]]

        yscale_x = [x + offset_x for x in yscale_x]
        yscale_y = [y + offset_y for y in yscale_y]

        ax.plot(yscale_x, yscale_y, c='k', lw=lw)
        ax.text(yscale_x[0] + hpad * text_pos_sign,
                yscale_y[0] + np.diff(yscale_y)[0] / 2,
                f"{yscalebar}{y_unit}",
                ha=yscale_ha, va="center", fontsize=fontsize)
