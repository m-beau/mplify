"""
mplify: MatPlotLib Prettifier (make plots pretty)

Core module containing the mplify() function.
"""

import importlib
import warnings
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator
from pathlib import Path

import mplify.DEFAULT_PARAMS as _params
from mplify._utils import _isnumeric, _pprint_dic, _docstring_decorator
from mplify._ticks import get_labels_from_ticks, get_bestticks
from mplify._colorbar import add_colorbar
from mplify._scalebar import plot_scalebar

_params_path = Path(_params.__file__)
_params_mtime = _params_path.stat().st_mtime


def _live_params():
    """Return (default_mplify_params, SIZE_PRESETS), re-reading DEFAULT_PARAMS.py
    from disk when it changed since the last call. This is what lets edits to
    mplify's defaults take effect on your very next mplify() call, whether or
    not IPython's %autoreload is enabled.
    """
    global _params_mtime
    try:
        mtime = _params_path.stat().st_mtime
    except OSError:
        return _params.default_mplify_params, _params.SIZE_PRESETS
    if mtime != _params_mtime:
        try:
            importlib.reload(_params)
            _params_mtime = mtime
        except Exception as e:
            warnings.warn(
                f"mplify: failed to reload DEFAULT_PARAMS.py ({e}); "
                "using the previous defaults until it's fixed.")
    return _params.default_mplify_params, _params.SIZE_PRESETS


@_docstring_decorator(_pprint_dic(_params.default_mplify_params))
def mplify(fig=None,
           ax=None,
           figsize=None,
           axsize=None,
           size=None,
           adjust_ticks_from_size=True,

           xlim=None,
           ylim=None,
           xlabel=None,
           ylabel=None,
           xticks=None,
           yticks=None,
           xtickslabels=None,
           ytickslabels=None,
           reset_xticks=None,
           reset_yticks=None,

           xtickrot=None,
           ytickrot=None,
           xtickha=None,
           xtickva=None,
           ytickha=None,
           ytickva=None,
           xlabelpad=None,
           ylabelpad=None,

           axlab_w=None,
           axlab_s=None,
           ticklab_w=None,
           ticklab_s=None,
           ticks_direction=None,

           title=None,
           title_w=None,
           title_s=None,

           font_family=None,

           lw=None,
           hide_top_right=None,
           hide_axis=None,
           transparent_background=None,
           tight_layout=None,

           hspace=None,
           wspace=None,

           show_legend=None,
           hide_legend=None,
           legend_loc=None,

           saveFig=None,
           saveDir=None,
           figname=None,
           _format=None,

           colorbar=None,
           vmin=None, vmax=None,
           cmap=None,
           center=None,
           cticks=None,
           ctickslabels=None,
           clim=None,
           cbar_w=None,
           cbar_h=None,
           clabel=None,
           clabel_w=None,
           clabel_s=None,
           cticks_s=None,
           cbar_pad=None,

           hlines=None,
           vlines=None,
           lines_kwargs=None,
           prettify=True,
           align_x_labels=None,
           align_y_labels=None,

           xscalebar=None,
           yscalebar=None,
           xscalebar_unit=None,
           yscalebar_unit=None,
           scalebarkwargs=None,
           ):
    """
    Make plots pretty.

    Awesome utility to format matplotlib plots.
    Simply add mplify() at the end of any plotting script, feeding it with your fav parameters!

    If you set prettify=False, it will only apply the parameters you provide explicitly
    and leave the rest unchanged.

    In a breeze:
        - change the weight/size/alignment/rotation of the axis labels, ticks labels, title
        - edit the x, y and colorbar axis ticks and ticks labels
        - hide the spines (edges of your figure)
        - hide all the axis, labels etc in one go with hide_axis
        - save figures in any format
        - add or remove a legend
        - add a custom colorbar
        - apply tight_layout to fit your subplots properly

    How it works: grabs the currently active figure and axis (plt.gcf() and plt.gca()).
    Alternatively, pass a matplotlib figure and specific axes as arguments.

    size: scales font sizes, spine/tick line widths and colorbar thickness to fit the
        output medium, without touching data-plotting choices. One of (see
        mplify.DEFAULT_PARAMS.SIZE_PRESETS — edit that file to change these defaults):
        'xs', 's', 'm' (default), 'l', 'xl', 'xxl', or the aliases
        'paper' (-> 's'), 'slide' (-> 'm'), 'poster' (-> 'l').
        Any of title_s, axlab_s, ticklab_s, lw, cbar_w, clabel_s, cticks_s,
        lines_kwargs['lw'] and scalebarkwargs['fontsize'/'lw'] passed explicitly
        still take precedence.

    adjust_ticks_from_size: if True (default) and size is set, x/y ticks that
        weren't explicitly passed via xticks/yticks (and colorbar ticks not
        passed via cticks) are recomputed with mplify's smart tick spacing
        (get_bestticks) instead of matplotlib's own locator / add_colorbar's
        own default, sparsened further ('xl'/'xxl') so tick labels don't crowd
        each other at those sizes. Ignored when size is None, and skipped on
        non-linear (log/symlog/logit) axes, which keep their own locator. Set
        to False to always keep matplotlib's/add_colorbar's own tick placement
        regardless of size.
        Note that passing any size therefore does slightly more than rescale
        fonts: mplify(size='m') and mplify() differ in tick placement.

    align_x_labels / align_y_labels: if True (default) and prettify=True, call
        fig.align_xlabels / fig.align_ylabels so shared axis labels line up
        across subplots. Set to False to leave each label at its own position,
        e.g. when repositioning a single axis with axsize (aligning would pull
        its label towards the un-resized sibling subplots).

    Default Arguments:
        {0}
    """

    default_mplify_params, SIZE_PRESETS = _live_params()
    d = default_mplify_params
    # 'xl'/'xxl' get sparser auto-ticks than the rest (see Tick values below);
    # compared by identity so aliases (e.g. size='poster' -> SIZE_PRESETS['l'])
    # resolve correctly without string-matching alias names.
    size_is_sparse = False
    if size is not None:
        if size not in SIZE_PRESETS:
            raise ValueError(
                f"Unknown size {size!r}. Choose from {list(SIZE_PRESETS)}.")
        preset = SIZE_PRESETS[size]
        size_is_sparse = preset is SIZE_PRESETS['xl'] or preset is SIZE_PRESETS['xxl']
        d = {**d, **{k: v for k, v in preset.items()
                     if k not in ('lines_kwargs', 'scalebarkwargs')}}
        d['lines_kwargs'] = {**default_mplify_params['lines_kwargs'],
                             **preset.get('lines_kwargs', {})}
        d['scalebarkwargs'] = {**default_mplify_params['scalebarkwargs'],
                               **preset.get('scalebarkwargs', {})}

    if fig is None:
        fig = plt.gcf() if ax is None else ax.get_figure()
    if ax is None:
        ax = plt.gca()

    # --- Resolve defaults ---
    # When prettify=True, all style params get a value (from user, defaults, or axis state).
    # When prettify=False, only user-provided params take effect.

    if prettify:
        # Axis state defaults (read current plot state)
        if xlim is None: xlim = ax.get_xlim()
        if ylim is None: ylim = ax.get_ylim()
        if title is None: title = ax.get_title()
        if xlabel is None: xlabel = ax.get_xlabel()
        if ylabel is None: ylabel = ax.get_ylabel()

        # Style defaults (from default_mplify_params)
        if title_w is None: title_w = d['title_w']
        if title_s is None: title_s = d['title_s']
        if font_family is None: font_family = d['font_family']
        if axlab_w is None: axlab_w = d['axlab_w']
        if axlab_s is None: axlab_s = d['axlab_s']
        if xlabelpad is None: xlabelpad = d['xlabelpad']
        if ylabelpad is None: ylabelpad = d['ylabelpad']
        if ticklab_w is None: ticklab_w = d['ticklab_w']
        if ticklab_s is None: ticklab_s = d['ticklab_s']
        if ticks_direction is None: ticks_direction = d['ticks_direction']
        if xtickrot is None: xtickrot = d['xtickrot']
        if ytickrot is None: ytickrot = d['ytickrot']
        if xtickha is None: xtickha = d['xtickha']
        if xtickva is None: xtickva = d['xtickva']
        if ytickha is None: ytickha = d['ytickha']
        if ytickva is None: ytickva = d['ytickva']
        if lw is None: lw = d['lw']
        if hide_top_right is None: hide_top_right = d['hide_top_right']
        if hide_axis is None: hide_axis = d['hide_axis']
        if tight_layout is None: tight_layout = d['tight_layout']
        if align_x_labels is None: align_x_labels = d['align_x_labels']
        if align_y_labels is None: align_y_labels = d['align_y_labels']
        if show_legend is None: show_legend = d['show_legend']
        if hide_legend is None: hide_legend = d['hide_legend']
        if legend_loc is None: legend_loc = d['legend_loc']
        if saveFig is None: saveFig = d['saveFig']
        if saveDir is None: saveDir = d['saveDir']
        if figname is None: figname = d['figname']
        if _format is None: _format = d['_format']
        if colorbar is None: colorbar = d['colorbar']
        if cbar_w is None: cbar_w = d['cbar_w']
        if cbar_h is None: cbar_h = d['cbar_h']
        if clabel is None: clabel = d['clabel']
        if clabel_w is None: clabel_w = d['clabel_w']
        if clabel_s is None: clabel_s = d['clabel_s']
        if cticks_s is None: cticks_s = d['cticks_s']
        if cbar_pad is None: cbar_pad = d['cbar_pad']

    # Merge dict-type defaults (always applied — user overrides merge with defaults)
    lines_kwargs = {**d['lines_kwargs'], **(lines_kwargs or {})}
    scalebarkwargs = {**d['scalebarkwargs'], **(scalebarkwargs or {})}
    if xscalebar_unit is None: xscalebar_unit = d['xscalebar_unit']
    if yscalebar_unit is None: yscalebar_unit = d['yscalebar_unit']
    if font_family is None: font_family = d['font_family']

    # --- Apply settings ---

    hfont = {'fontname': font_family}

    # Figure / axis size
    if figsize is not None:
        fig.set_figwidth(figsize[0])
        fig.set_figheight(figsize[1])
    if axsize is not None:
        # Reposition this axis within the existing figure
        # without resizing the figure or affecting other axes
        fig_w, fig_h = fig.get_size_inches()
        frac_w = axsize[0] / fig_w
        frac_h = axsize[1] / fig_h
        cur_pos = ax.get_position()
        cx = (cur_pos.x0 + cur_pos.x1) / 2
        cy = (cur_pos.y0 + cur_pos.y1) / 2
        new_x0 = max(0, min(cx - frac_w / 2, 1 - frac_w))
        new_y0 = max(0, min(cy - frac_h / 2, 1 - frac_h))
        ax.set_position([new_x0, new_y0, frac_w, frac_h])

    # Hide/show axis
    if hide_axis is not None:
        ax.axis('off' if hide_axis else 'on')

    # Axis labels
    if ylabel is not None:
        ax.set_ylabel(ylabel, weight=axlab_w, size=axlab_s,
                      labelpad=ylabelpad, **hfont)
    if xlabel is not None:
        ax.set_xlabel(xlabel, weight=axlab_w, size=axlab_s,
                      labelpad=xlabelpad, **hfont)

    # Axis limits (set BEFORE altering ticks, since limits affect ticks)
    if xlim is not None: ax.set_xlim(xlim)
    if ylim is not None: ax.set_ylim(ylim)

    # Tick values
    # When size is set (and adjust_ticks_from_size=True), ticks the user didn't
    # pass explicitly are recomputed with get_bestticks instead of matplotlib's
    # own locator, so they land on the same nice round spacing as e.g. colorbar
    # ticks — sparser still for 'xl'/'xxl', where big tick labels need more room.
    # get_bestticks only makes sense on a linear scale — on a log/symlog/logit
    # axis it would replace matplotlib's decade ticks with linear round numbers
    # and blank out most of the labels, so those axes keep their own locator.
    adjust_ticks = prettify and size is not None and adjust_ticks_from_size

    if prettify and xticks is None:
        if reset_xticks:
            ax.xaxis.set_major_locator(AutoLocator())
        xticks = ax.get_xticks()
        if adjust_ticks and ax.get_xscale() == 'linear':
            x0, x1 = ax.get_xlim()
            if x0 != x1:
                try:
                    xticks = get_bestticks(x0, x1, light=size_is_sparse)
                except ValueError:
                    pass  # degenerate span: keep matplotlib's own ticks
    if xticks is not None: ax.set_xticks(xticks)

    if prettify and yticks is None:
        if reset_yticks:
            ax.yaxis.set_major_locator(AutoLocator())
        yticks = ax.get_yticks()
        if adjust_ticks and ax.get_yscale() == 'linear':
            y0, y1 = ax.get_ylim()
            if y0 != y1:
                try:
                    yticks = get_bestticks(y0, y1, light=size_is_sparse)
                except ValueError:
                    pass
    if yticks is not None: ax.set_yticks(yticks)

    # Tick labels
    fig.canvas.draw()  # force tick label generation

    # Check if axes use scientific notation (offset text like "1e6").
    # When they do, we style tick labels in-place to preserve the formatter
    # and offset text, rather than calling set_x/yticklabels which replaces
    # the formatter with FixedFormatter and destroys the offset.
    x_has_offset = bool(ax.xaxis.get_offset_text().get_text())
    y_has_offset = bool(ax.yaxis.get_offset_text().get_text())

    if xtickslabels is None and prettify and any(ax.get_xticklabels()):
        if x_has_offset:
            pass  # keep formatter intact, style below
        elif _isnumeric(ax.get_xticklabels()[0].get_text()):
            xtickslabels, _ = get_labels_from_ticks(xticks)
        else:
            xtickslabels = ax.get_xticklabels()
    if ytickslabels is None and prettify and any(ax.get_yticklabels()):
        if y_has_offset:
            pass  # keep formatter intact, style below
        elif _isnumeric(ax.get_yticklabels()[0].get_text()):
            ytickslabels, _ = get_labels_from_ticks(yticks)
        else:
            ytickslabels = ax.get_yticklabels()

    if xtickslabels is not None:
        if xticks is not None and len(xtickslabels) != len(xticks):
            raise ValueError(
                f'xtickslabels length ({len(xtickslabels)}) must match '
                f'xticks length ({len(xticks)}).')
        if xtickha is None: xtickha = ax.xaxis.get_ticklabels()[0].get_ha()
        if xtickva is None: xtickva = ax.xaxis.get_ticklabels()[0].get_va()
        ax.set_xticklabels(xtickslabels, fontsize=ticklab_s, fontweight=ticklab_w,
                           color=(0, 0, 0), rotation=xtickrot,
                           ha=xtickha, va=xtickva, **hfont)
    if ytickslabels is not None:
        if yticks is not None and len(ytickslabels) != len(yticks):
            raise ValueError(
                f'ytickslabels length ({len(ytickslabels)}) must match '
                f'yticks length ({len(yticks)}).')
        if ytickha is None: ytickha = ax.yaxis.get_ticklabels()[0].get_ha()
        if ytickva is None: ytickva = ax.yaxis.get_ticklabels()[0].get_va()
        ax.set_yticklabels(ytickslabels, fontsize=ticklab_s, fontweight=ticklab_w,
                           color=(0, 0, 0), rotation=ytickrot,
                           ha=ytickha, va=ytickva, **hfont)

    # When scientific notation is active, style tick labels in-place
    # (without replacing the formatter) and style the offset text to match
    for axis, has_offset, rot, ha, va in [
        (ax.xaxis, x_has_offset, xtickrot, xtickha, xtickva),
        (ax.yaxis, y_has_offset, ytickrot, ytickha, ytickva),
    ]:
        if has_offset and prettify:
            for label in axis.get_ticklabels():
                if ticklab_s is not None: label.set_fontsize(ticklab_s)
                if ticklab_w is not None: label.set_fontweight(ticklab_w)
                if font_family is not None: label.set_fontfamily(font_family)
                label.set_color((0, 0, 0))
                if rot is not None: label.set_rotation(rot)
                if ha is not None: label.set_ha(ha)
                if va is not None: label.set_va(va)
            offset = axis.get_offset_text()
            if ticklab_s is not None: offset.set_fontsize(ticklab_s)
            if font_family is not None: offset.set_fontfamily(font_family)

    # Reset limits (ticks may have shifted them)
    if xlim is not None: ax.set_xlim(xlim)
    if ylim is not None: ax.set_ylim(ylim)

    # Title
    if title is not None:
        ax.set_title(title, size=title_s, weight=title_w)

    # Ticks and spines
    if prettify:
        ax.tick_params(axis='both', bottom=1, left=1, top=0, right=0,
                       width=lw, length=4, direction=ticks_direction)
    elif lw is not None or ticks_direction is not None:
        ax.tick_params(axis='both', width=lw, direction=ticks_direction)

    spine_keys = list(ax.spines.keys())
    if lw is not None:
        lw_spine_keys = ['polar'] if 'polar' in spine_keys else ['left', 'bottom', 'top', 'right']
        for sp in lw_spine_keys:
            ax.spines[sp].set_lw(lw)

    if hide_top_right is not None:
        hide_spine_keys = ['polar'] if 'polar' in spine_keys else ['top', 'right']
        if hide_top_right and 'top' in hide_spine_keys:
            for sp in hide_spine_keys:
                ax.spines[sp].set_visible(False)
        else:
            for sp in hide_spine_keys:
                ax.spines[sp].set_visible(True)

    # Background transparency
    # Both patches must go: the axis patch alone leaves the figure patch
    # painted white underneath (and prettify sets it white explicitly below),
    # so a "transparent" figure would still save with a white background.
    if transparent_background is not None:
        ax.patch.set_alpha(0 if transparent_background else 1)
        fig.patch.set_alpha(0 if transparent_background else 1)

    # Horizontal and vertical reference lines
    if hlines is not None:
        if not hasattr(hlines, '__iter__'):
            raise TypeError('hlines must be an iterable.')
        for hline in hlines:
            ax.axhline(y=hline, **lines_kwargs)
    if vlines is not None:
        if not hasattr(vlines, '__iter__'):
            raise TypeError('vlines must be an iterable.')
        for vline in vlines:
            ax.axvline(x=vline, **lines_kwargs)

    # Layout
    if tight_layout:
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    if hspace is not None: fig.subplots_adjust(hspace=hspace)
    if wspace is not None: fig.subplots_adjust(wspace=wspace)
    if prettify:
        if align_y_labels:
            fig.align_ylabels(fig.axes)
        if align_x_labels:
            fig.align_xlabels(fig.axes)

    # Legend
    if show_legend and hide_legend:
        raise ValueError("Cannot both show and hide the legend.")
    if legend_loc is not None and len(legend_loc) not in (2, 4):
        raise ValueError(
            "legend_loc must be (x, y) or (x, y, width, height).")
    if show_legend:
        ax.legend(bbox_to_anchor=legend_loc, loc='lower left',
                  prop={'family': font_family, 'size': ticklab_s})
    elif hide_legend:
        ax.legend([], [], frameon=False)

    # Colorbar
    if colorbar:
        if vmin is None or vmax is None or cmap is None:
            raise ValueError(
                "colorbar=True requires vmin, vmax, and cmap.")
        # add_colorbar's own default (get_bestticks(..., light=True)) already
        # suits xs/s/m/l — leave cticks alone for those so behavior there is
        # unchanged. 'xl'/'xxl' need sparser still (the colorbar's vertical
        # space doesn't grow with font size), so thin that same default out
        # one more notch by doubling its step again. Only kicks in when the
        # caller hasn't set cticks themselves.
        if cticks is None and adjust_ticks and size_is_sparse and vmin < vmax:
            try:
                medium = get_bestticks(vmin, vmax, light=True)
                if len(medium) >= 2:
                    step = float(medium[1] - medium[0])
                    cticks = get_bestticks(vmin, vmax, step=step, light=True)
            except ValueError:
                pass  # degenerate range: let add_colorbar apply its own default
        cb_kwargs = dict(vmin=vmin, vmax=vmax, cmap=cmap)
        for k, v in [('width', cbar_w), ('height', cbar_h),
                      ('center', center),
                      ('cticks', cticks), ('clabel', clabel),
                      ('clabel_w', clabel_w), ('clabel_s', clabel_s),
                      ('cticks_s', cticks_s), ('ctickslabels', ctickslabels),
                      ('pad', cbar_pad), ('clim', clim)]:
            if v is not None:
                cb_kwargs[k] = v
        fig = add_colorbar(fig, ax, None, **cb_kwargs)

    if prettify and not transparent_background:
        fig.patch.set_facecolor('white')

    # Scalebar
    if xscalebar is not None or yscalebar is not None:
        plot_scalebar(ax, xscalebar, yscalebar,
                      xscalebar_unit, yscalebar_unit,
                      **scalebarkwargs)

    # Save
    if saveFig:
        if figname is None and title is not None:
            figname = title
        save_mpl_fig(fig, figname, saveDir, _format, dpi=500,
                     transparent=bool(transparent_background))

    return fig, ax


def save_mpl_fig(fig, figname, saveDir, _format='pdf', dpi=500, transparent=False):
    """Save a matplotlib figure with editable text.

    Arguments:
        - fig: matplotlib figure
        - figname: output file name (without extension)
        - saveDir: output directory path
        - _format: file format ('pdf', 'png', 'svg', etc.)
        - dpi: resolution in dots per inch
        - transparent: if True, save with a transparent background
    """
    # Temporarily set params for high-quality output
    dpi_orig = mpl.rcParams['figure.dpi']
    fonttype1 = mpl.rcParams['pdf.fonttype']
    fonttype2 = mpl.rcParams['ps.fonttype']

    mpl.rcParams['figure.dpi'] = dpi
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42

    try:
        if saveDir is None:
            saveDir = '~/Downloads'
        saveDir = Path(saveDir).expanduser()
        if not saveDir.exists():
            if not saveDir.parent.exists():
                raise FileNotFoundError(
                    f"Cannot create {saveDir}: parent directory "
                    f"{saveDir.parent} does not exist.")
            saveDir.mkdir()
        p = saveDir / f"{figname}.{_format}"
        fig.savefig(p, dpi=dpi, bbox_inches='tight', transparent=transparent)
    finally:
        # Restore original parameters even if saving fails
        mpl.rcParams['figure.dpi'] = dpi_orig
        mpl.rcParams['pdf.fonttype'] = fonttype1
        mpl.rcParams['ps.fonttype'] = fonttype2
