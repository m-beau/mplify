"""mplify: MatPlotLib you will Prettify"""

from mplify._defaults import default_mplp_params, SIZE_PRESETS
from mplify._core import mplp, save_mpl_fig
from mplify._utils import set_ax_size
from mplify._ticks import (
    get_bestticks,
    get_bestticks_from_array,
    get_labels_from_ticks,
    sci_notation,
)
from mplify._colors import (
    to_rgb,
    to_hex,
    to_hsv,
    get_cmap,
    get_bounded_cmap,
    get_ncolors_cmap,
    get_color_families,
    html_palette,
)
from mplify._colorbar import add_colorbar
from mplify._scalebar import plot_scalebar

__all__ = [
    # Core
    "mplp",
    "default_mplp_params",
    "SIZE_PRESETS",

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
