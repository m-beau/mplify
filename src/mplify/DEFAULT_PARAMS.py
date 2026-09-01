"""mplify's default styling parameters — EDIT THIS FILE to change mplify's
defaults across your project.

- default_mplp_params: the base style mplp() falls back to for any parameter
  you don't pass explicitly — fonts, spine/tick widths, colorbar, scalebar,
  legend, etc. It's also, in effect, the 'm' / 'slide' size preset below.

- SIZE_PRESETS: per-size overrides layered on top of default_mplp_params
  when you pass size=... to mplp() (e.g. mplp(size='poster')). Aliases
  'paper', 'slide' and 'poster' point at 's', 'm' and 'l' respectively.

mplp() re-reads this file from disk (checking its mtime) on every call, so
edits here take effect on your very next mplp() call — no kernel restart
and no need to have %autoreload enabled.
"""

from mplify._fonts import DEFAULT_FONT_FAMILY

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
    align_x_labels=True,
    align_y_labels=True,

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
    yscalebar_unit='μV',
    scalebarkwargs={
        'scalepad': 0.025,
        'fontsize': 14,
        'lw': 3,
        'loc': 'right',
        'offset_x': 0,
        'offset_y': 0,
    },
)

# Each preset scales only the "meta-plotting" elements that need to grow or
# shrink with the viewing distance/medium — font sizes and line widths — so
# a plot keeps the same proportions, just legible wherever it ends up.
# Data-plotting choices (colors, markers, line styles, positions, ...) stay
# untouched. Use via mplp(size='poster'), or import SIZE_PRESETS directly.
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
        cticks_s=9,
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
        cticks_s=12,
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
        cticks_s=14,
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
        cticks_s=17,
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
        cticks_s=24,
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
