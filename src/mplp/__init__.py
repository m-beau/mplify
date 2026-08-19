"""mplp: MatPlotLib Prettifier (Make PLots Pretty)"""

from mplp._defaults import default_mplp_params
from mplp._core import mplp, save_mpl_fig
from mplp._utils import set_ax_size
from mplp._ticks import (
    get_bestticks,
    get_bestticks_from_array,
    get_labels_from_ticks,
    sci_notation,
)
from mplp._colors import (
    to_rgb,
    to_hex,
    to_hsv,
    get_cmap,
    get_bounded_cmap,
    get_ncolors_cmap,
    get_color_families,
    html_palette,
)
from mplp._colorbar import add_colorbar
from mplp._scalebar import plot_scalebar

__all__ = [
    # Core
    "mplp",
    "default_mplp_params",

    # Save / size
    "save_mpl_fig",
    "set_ax_size",

    # Ticks
    "get_bestticks",
    "get_bestticks_from_array",
    "get_labels_from_ticks",
    "sci_notation",

    # Colors
    "to_rgb",
    "to_hex",
    "to_hsv",
    "get_cmap",
    "get_bounded_cmap",
    "get_ncolors_cmap",
    "get_color_families",
    "html_palette",

    # Colorbar / scalebar
    "add_colorbar",
    "plot_scalebar",
]
