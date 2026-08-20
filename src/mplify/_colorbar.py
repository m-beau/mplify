"""Colorbar utilities."""

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from mplify._colors import get_bounded_cmap
from mplify._ticks import get_bestticks, get_labels_from_ticks


def add_colorbar(fig, ax, mappable=None, vmin=None, vmax=None,
                 width=0.01, height=0.5, cticks=None,
                 clabel=None, clabel_w='regular', clabel_s=20, cticks_s=16,
                 ctickslabels=None, cmap=None, center=None, pad=0.01,
                 clim=None, cbar_ax=None):
    """Add a colorbar to a figure, preserving the main axis size.

    Either provide a mappable (e.g. the return value of ax.imshow()) or
    provide vmin, vmax, and cmap to create one.

    Arguments:
        - fig, ax: matplotlib figure and axis
        - mappable: a ScalarMappable (e.g. from imshow, scatter). If None,
                    one is created from vmin/vmax/cmap.
        - vmin, vmax: data range for the colorbar
        - width, height: colorbar dimensions as fraction of axis size
        - cticks: tick positions on the colorbar
        - clabel: colorbar label text
        - clabel_w, clabel_s: label weight and size
        - cticks_s: tick label size
        - ctickslabels: custom tick labels
        - cmap: colormap name (required if mappable is None)
        - center: center value for diverging colormaps (uses get_bounded_cmap)
        - pad: padding between axis and colorbar as fraction of axis width
        - clim: explicit (min, max) limits for the colorbar axis
        - cbar_ax: pre-existing axis for the colorbar
    """
    # Validate vmin/vmax
    if vmin is not None or vmax is not None:
        if vmin is None or vmax is None:
            raise ValueError("You must provide both vmin and vmax.")
    if vmin is not None and vmax is not None:
        if vmin >= vmax:
            raise ValueError(f"vmin ({vmin}) must be less than vmax ({vmax}).")
        if cticks is None:
            cticks = get_bestticks(vmin, vmax, light=True)

    # Create mappable if not provided
    if mappable is None:
        if vmin is None or vmax is None:
            raise ValueError(
                "Without a mappable, you must provide vmin and vmax.")
        if cmap is None:
            raise ValueError(
                "Without a mappable, you must provide a colormap (e.g. 'viridis').")
        if center is not None:
            cmap = get_bounded_cmap(cmap, vmin, center, vmax)
        norm = plt.Normalize(vmin, vmax)
        mappable = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        mappable.set_array([])

    # Create colorbar axis anchored to the parent axes so it survives
    # tight_layout / constrained_layout adjustments.
    if cbar_ax is None:
        cbar_ax = inset_axes(
            ax,
            width=f"{width * 100}%",
            height=f"{height * 100}%",
            loc='lower right',
            bbox_to_anchor=(pad + width, 0, 1, 1),
            bbox_transform=ax.transAxes,
            borderpad=0,
        )

    fig.colorbar(mappable, cax=cbar_ax, ax=ax,
                 orientation='vertical', label=clabel, use_gridspec=True)

    # Format ticks and labels
    if ctickslabels is None:
        ctickslabels, _ = get_labels_from_ticks(cticks)
    elif len(ctickslabels) != len(cticks):
        raise ValueError(
            f"ctickslabels length ({len(ctickslabels)}) must match "
            f"cticks length ({len(cticks)}).")

    if clabel is not None:
        cbar_ax.yaxis.label.set_font_properties(
            mpl.font_manager.FontProperties(weight=clabel_w, size=clabel_s))
        cbar_ax.yaxis.label.set_rotation(-90)
        cbar_ax.yaxis.label.set_va('bottom')
        cbar_ax.yaxis.label.set_ha('center')
        cbar_ax.yaxis.labelpad = 5
    cbar_ax.yaxis.set_ticks(cticks)
    cbar_ax.yaxis.set_ticklabels(ctickslabels, ha='left')
    cbar_ax.yaxis.set_tick_params(pad=5, labelsize=cticks_s)
    cbar_ax.set_ylim(clim)

    return fig
