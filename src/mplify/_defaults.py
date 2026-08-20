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

###########################################################################
###########################################################################
###########################################################################

"""Size presets for mplp().

The base defaults in `_defaults.py` (title/axis/tick font sizes, spine and
tick line widths, colorbar and scalebar text/line sizes) are tuned for
on-screen slides. That's too small to read on a poster from a few meters
away, and too large for a paper figure that will be printed at a few inches
wide and read up close.

Each preset here scales only the "meta-plotting" elements that need to grow
or shrink with the viewing distance/medium — font sizes and line widths —
so a plot keeps the same proportions, just legible wherever it ends up.
Data-plotting choices (colors, markers, line styles, positions, ...) are
untouched.

Use via mplp(size='poster'), or import SIZE_PRESETS directly to inspect/tweak.
"""

SIZE_PRESETS = {

    # xs: extra small — dense multi-panel figures, small insets, thumbnails
    'xs': dict(
        title_s=14,
        axlab_s=13,
        ticklab_s=11,
        lw=0.7,
        cbar_w=0.02,    # colorbar thickness scales with lw, else it reads as
                        # a hairline next to xs text and a starved sliver next to xxl text
        clabel_s=13,
        cticks_s=11,
        lines_kwargs={'lw': 1},
        scalebarkwargs={'fontsize': 10, 'lw': 2},
    ),

    # s: small — paper figures, printed at a few inches wide and read up close
    's': dict(
        title_s=17,
        axlab_s=15,
        ticklab_s=14,
        lw=0.85,
        cbar_w=0.025,
        clabel_s=15,
        cticks_s=14,
        lines_kwargs={'lw': 1.3},
        scalebarkwargs={'fontsize': 12, 'lw': 2.5},
    ),

    # m: medium — slides, general on-screen work (mplify's original defaults)
    'm': dict(
        title_s=20,
        axlab_s=18,
        ticklab_s=16,
        lw=1,
        cbar_w=0.03,
        clabel_s=18,
        cticks_s=16,
        lines_kwargs={'lw': 1.5},
        scalebarkwargs={'fontsize': 14, 'lw': 3},
    ),

    # l: large — posters, read from about a meter away
    'l': dict(
        title_s=26,
        axlab_s=23,
        ticklab_s=21,
        lw=1.3,
        cbar_w=0.04,
        clabel_s=23,
        cticks_s=21,
        lines_kwargs={'lw': 2},
        scalebarkwargs={'fontsize': 18, 'lw': 4},
    ),

    # xl: extra large — posters/banners read from several meters away
    'xl': dict(
        title_s=32,
        axlab_s=29,
        ticklab_s=26,
        lw=1.6,
        cbar_w=0.05,
        clabel_s=29,
        cticks_s=26,
        lines_kwargs={'lw': 2.4},
        scalebarkwargs={'fontsize': 22, 'lw': 5},
    ),

    # xxl: banner-sized — huge posters/wall displays read from far across a room
    'xxl': dict(
        title_s=38,
        axlab_s=34,
        ticklab_s=30,
        lw=1.9,
        cbar_w=0.06,
        clabel_s=34,
        cticks_s=30,
        lines_kwargs={'lw': 2.9},
        scalebarkwargs={'fontsize': 27, 'lw': 6},
    ),
}

# Semantic aliases, so you can call mplp(size='paper') instead of remembering
# which letter size maps to which output medium.
SIZE_PRESETS['paper'] = SIZE_PRESETS['s']    # small text, printed close-up
SIZE_PRESETS['slide'] = SIZE_PRESETS['m']    # mplify's original defaults
SIZE_PRESETS['poster'] = SIZE_PRESETS['l']   # large text, read from afar
