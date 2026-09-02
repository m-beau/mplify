"""Color utilities built on top of matplotlib.colors."""

import matplotlib as mpl
import matplotlib.colors
import numpy as np


def to_rgb(color):
    """Convert any matplotlib color specification to (r, g, b) tuple (0-1 range).

    Accepts: named colors ('red', 'tab:blue'), hex strings ('#ff0000'),
    single-letter codes ('r'), and RGB tuples.
    """
    return mpl.colors.to_rgb(color)


def to_hex(color):
    """Convert any matplotlib color specification to hex string.

    Accepts: named colors, hex strings, single-letter codes,
    and RGB tuples (0-1 or 0-255 range).
    """
    if not isinstance(color, str):
        color = tuple(color)
        if any(c > 1 for c in color):
            color = tuple(c / 255 for c in color)
    return mpl.colors.to_hex(color)


def to_hsv(color):
    """Convert any matplotlib color specification to HSV tuple."""
    if isinstance(color, str):
        color = mpl.colors.to_rgb(color)
    return mpl.colors.rgb_to_hsv(color)


def get_cmap(cmap_str):
    """Get a matplotlib colormap by name."""
    return mpl.colormaps[cmap_str]


def get_bounded_cmap(cmap_str, vmin, center, vmax, colorseq='linear'):
    """Create a colormap bounded around a center value.

    Useful for diverging data where the center isn't at the midpoint
    of the value range.

    Arguments:
        - cmap_str: name of a matplotlib colormap
        - vmin, vmax: data range bounds
        - center: center value for the colormap
        - colorseq: 'linear' or 'nonlinear' reindexing
    """
    if not vmin <= center <= vmax:
        raise ValueError(f'Must have vmin <= center <= vmax, got {vmin}, {center}, {vmax}')
    cmap = get_cmap(cmap_str)

    vrange = max(vmax - center, center - vmin)
    if vrange == 0:
        vrange = 1
    if colorseq == 'linear':
        vrange_sym = [-vrange, vrange]
        cmin = (vmin - vrange_sym[0]) / (vrange_sym[1] - vrange_sym[0])
        cmax = (vmax - vrange_sym[0]) / (vrange_sym[1] - vrange_sym[0])
        colors_reindex = np.linspace(cmin, cmax, 256)
    elif colorseq == 'nonlinear':
        topratio = (vmax - center) / vrange
        bottomratio = abs(vmin - center) / vrange
        colors_reindex = np.append(
            np.linspace(0, 0.5, int(256 * bottomratio / 2)),
            np.linspace(0.5, 1, int(256 * topratio / 2)),
        )
    else:
        raise ValueError(f"colorseq must be 'linear' or 'nonlinear', got {colorseq!r}")
    return mpl.colors.ListedColormap(cmap(colors_reindex))


def get_ncolors_cmap(n, cmap_str="tab10", plot=False):
    """Return n colors homogeneously distributed from a colormap.

    Arguments:
        - n: number of colors
        - cmap_str: name of a matplotlib colormap
        - plot: if True, display the palette as HTML (Jupyter notebooks)
    """
    n = int(n)
    cmap = get_cmap(cmap_str)
    ids = np.linspace(0, 1, n)
    colors = cmap(ids)[:, :-1].tolist()
    if plot:
        html_palette(colors)
    return colors


def get_color_families(ncolors, nfamilies, cmapstr=None, gap_between_families=4):
    """Return nfamilies groups of ncolors perceptually close colors.

    Within each family, colors are neighbours on a perceptually sequential colormap.
    Between families, gap_between_families colors are skipped.

    Arguments:
        - ncolors: colors per family
        - nfamilies: number of families
        - cmapstr: colormap name (if None, uses matplotlib CSS colors sorted by HSV)
        - gap_between_families: spacing between families (higher = more distinct families)
    """
    if cmapstr is None:
        colors_all = _get_mpl_css_colors(sort=True, aslist=True)[15:-10]
        indices = np.linspace(0, len(colors_all) - 1,
                              (ncolors + gap_between_families) * nfamilies).astype(np.int64)
        colors = np.array(colors_all)[indices].tolist()
    else:
        colors = get_ncolors_cmap((ncolors + gap_between_families // 2) * nfamilies,
                                  cmapstr, plot=False)
    highsat_colors = [c for c in colors if to_hsv(c)[1] > 0.4]
    seed_ids = np.linspace(0, len(highsat_colors) - ncolors, nfamilies).astype(np.int64)
    return [[highsat_colors[si + i] for i in range(ncolors)] for si in seed_ids]


def html_palette(colors, maxwidth=20, as_str=False, show=True):
    """Display colors as an SVG palette (works in Jupyter notebooks).

    Arguments:
        - colors: list of colors (RGB tuples, hex strings, or named colors)
        - maxwidth: maximum colors per row
        - as_str: if True, return raw SVG string instead of IPython HTML object
        - show: if True, display the palette immediately
    """
    s = 55
    n = min(len(colors), maxwidth)
    col_rows = [colors[i * maxwidth:i * maxwidth + maxwidth]
                for i in range(len(colors) // maxwidth + 1)]
    col_rows = [c for c in col_rows if any(c)]
    h = len(col_rows)
    palette = f'<svg width="{n * s}" height="{s * h}">'
    for r, row_colors in enumerate(col_rows):
        for i, c in enumerate(row_colors):
            c_hex = c if isinstance(c, str) else to_hex(c)
            palette += (
                f'<rect x="{i * s}" y="{r * s}" width="{s}" height="{s}" '
                f'style="fill:{c_hex};stroke-width:2;stroke:rgb(255,255,255)"/>'
            )
    palette += '</svg>'
    if not as_str:
        try:
            from IPython.display import display, HTML as IPyHTML
        except ImportError as e:
            raise ImportError(
                "html_palette() needs IPython to render inline. Either install "
                "it (pip install ipython) or pass as_str=True to get the raw "
                "SVG string back instead.") from e
        palette = IPyHTML(palette)
        if show:
            display(palette)
    return palette


def _get_mpl_css_colors(sort=True, aslist=False):
    """Get matplotlib CSS4 colors, optionally sorted by HSV."""
    colors = mpl.colors.CSS4_COLORS
    if sort:
        by_hsv = sorted(
            (tuple(mpl.colors.rgb_to_hsv(mpl.colors.to_rgb(color))), name)
            for name, color in colors.items()
        )
        colors = {name: colors[name] for hsv, name in by_hsv}
    if aslist:
        colors = list(colors.values())
    return colors
