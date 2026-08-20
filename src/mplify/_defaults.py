"""Default parameters for mplify and font detection."""

import matplotlib as mpl
import matplotlib.font_manager as fm

# Make matplotlib saved figures text editable
mpl.rcParams["svg.fonttype"] = 'none'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42


def _resolve_font_family():
    """Return Arial if available, otherwise the closest sans-serif alternative."""
    available = {f.name for f in fm.fontManager.ttflist}
    for font in ('Arial', 'Helvetica', 'Liberation Sans', 'DejaVu Sans'):
        if font in available:
            return font
    return 'sans-serif'


DEFAULT_FONT_FAMILY = _resolve_font_family()

default_mplp_params = dict(
    # font
    font_family=DEFAULT_FONT_FAMILY,

    # title
    title_w='regular',
    title_s=20,

    # axis labels
    axlab_w='regular',
    axlab_s=18,

    # tick labels
    ticklab_w='regular',
    ticklab_s=16,
    ticks_direction='out',
    xlabelpad=0,
    ylabelpad=0,

    # tick rotation and alignment
    xtickrot=0,
    ytickrot=0,
    xtickha='center',
    xtickva='top',
    ytickha='right',
    ytickva='center',

    # spines and layout
    lw=1,
    hide_top_right=True,
    hide_axis=False,
    tight_layout=False,

    # legend
    show_legend=False,
    hide_legend=False,
    legend_loc=(1, 1),

    # figure saving
    saveFig=False,
    saveDir='~/Downloads',
    figname='figure',
    _format='pdf',

    # colorbar
    colorbar=False,
    cbar_w=0.03,
    cbar_h=0.4,
    clabel=None,
    clabel_w='regular',
    clabel_s=18,
    cticks_s=16,
    cbar_pad=0.01,

    # horizontal and vertical lines
    hlines=None,
    vlines=None,
    lines_kwargs={'lw': 1.5, 'ls': '--', 'color': 'k', 'zorder': -1000},

    # scalebar
    xscalebar=None,
    yscalebar=None,
    xscalebar_unit='ms',
    yscalebar_unit='\u03BCV',
    scalebarkwargs={
        'scalepad': 0.025,
        'fontsize': 14,
        'lw': 3,
        'loc': 'right',
        'offset_x': 0,
        'offset_y': 0,
    },
)
