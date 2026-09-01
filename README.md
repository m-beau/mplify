# mplify

**MatPlotLib prettifier.** One function, `mplp()` (MPLP: MatPlotLib Prettify, or Make Plot Pretty), that turns a matplotlib plot into a great v1 figure ready for your slides, poster, or paper.

```python
import matplotlib.pyplot as plt
from mplify import mplp

plt.plot(x, y)
mplp() # applies to the last figure and axis
```

<p align="center">
  <img src="doc/img/01_hero.png" width="100%" alt="matplotlib defaults vs mplp()">
</p>

---

## The problem

Matplotlib is very highly customizable. That is the problem.

Say you want to rotate your x tick labels 30°, right-align them so they don't
collide with the axis, bump the axis label font, and drop the top and right
spines. Four small, obvious, universally wanted things. Here is matplotlib:

```python
ax.set_xticks(positions)
ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=16, fontweight='regular')
ax.set_xlabel('Condition', size=18, labelpad=0)
ax.set_ylabel('Response', size=18, labelpad=0)
ax.tick_params(axis='both', width=1, length=4, direction='out',
               bottom=True, left=True, top=False, right=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for sp in ('left', 'bottom'):
    ax.spines[sp].set_lw(1)
```

Five different APIs (`set_xticklabels`, `set_xlabel`, `tick_params`, `spines`), three different spellings of the same concept (`fontsize`, `size`, `fontweight`/`weight`), and potential order-related bugs: ticks and limits interact, so calling them in the wrong order silently gives you a different figure.

To achieve the desired result, the knobs exist, but they're scattered across a documentation surface large enough that most of us end up doing one of three things:

1. copy-pasting the same 15 lines of boilerplate into every script;
2. re-googling "matplotlib rotate xticklabels" for the 200th time;
3. asking an LLM, which returns 40 lines of code, half of it redundant, and all of it subtly different from the 40 lines it gave you last week.

## The solution

`mplp()` is one callable with a flat, self-explanatory argument list. Everything
above becomes:

```python
mplp(xticks=positions, xtickslabels=labels, xtickrot=30, xtickha='right', xlabel='Condition', ylabel='Response')
```

Three things make this work:

**Sensible defaults.** Call `mplp()` with no arguments and it applies a handcrafted default styling: larger font sizes, fatter spines, top and right spines gone, ticks pointing out, editable text in saved PDFs.

**Implicitly callable.** `mplp()` reads the current figure via `plt.gcf()`/`plt.gca()`, so you can simply call it at the end of your script, whether you're using matplotlib in explicit (object-oriented) or implicit (without declaring figures and axis, MATLAB-inherited) mode. But you can always feed `fig` and `ax` to mplp explicitly.

**One flat layer of arguments.** All the common figure tweaks are a self-explanatory keyword that can be remembered through checking the arguments of `mplp()`: `xtickrot`, `ticklab_s`, `hide_top_right`, `hlines`, `clabel`, `legend_loc`, `saveFig`. Anything you don't pass keeps mplify's default; anything you do pass takes precedence.

And it stays out of your way: `mplp()` edits the axis you hand it and nothing else — no style sheet to install, no `rcParams` rewritten mid-script, no surprises in the next figure. (The one exception is deliberate: importing mplify sets `pdf`/`ps`/`svg` font types to keep text editable in saved vector files. See [Saving](#saving).)

---

## Install

```bash
pip install mplify        # or: uv add mplify
```

From source:

```bash
git clone https://github.com/m-beau/mplify.git
cd mplify && uv sync
```

Requires Python ≥ 3.10, matplotlib, numpy.

---

## Tour

Left panel is matplotlib's default in every figure below. Right panel is one
`mplp()` call. Full runnable versions of all of these live in
[`quickstart.ipynb`](quickstart.ipynb).

### Limits, ticks and labels, in the right order

`mplp` applies limits before ticks (and re-applies them after), so you never have
to remember which call comes first.

```python
mplp(xlim=(0, 8), ylim=(-0.5, 1),
     xticks=[0, 2, 4, 6, 8], yticks=[-0.5, 0, 0.5, 1],
     xlabel='Time (s)', ylabel='Amplitude (a.u.)')
```

![limits and ticks](doc/img/02_axes.png)

### Tick labels: text, rotation, alignment

```python
mplp(xticks=range(4), xtickslabels=categories, xtickrot=30, xtickha='right')
```

![rotated tick labels](doc/img/03_ticklabels.png)

### Reference lines

```python
mplp(hlines=[0], vlines=[np.pi, 2*np.pi],
     lines_kwargs={'lw': 2, 'ls': ':', 'color': 'grey'})
```

![reference lines](doc/img/04_lines.png)

### Good-looking colorbars

`plt.colorbar()` steals space from the parent axes, so a row of subplots ends up
with panels of different widths (and one of them mysteriously narrower than its
neighbours). mplify's colorbar is an inset anchored to the axis: the data area
keeps the exact size you gave it.

```python
mplp(colorbar=True, vmin=-3, vmax=3, cmap='RdBu_r',
     clabel='Z-score', cticks=[-2, 0, 2])
```

![colorbar](doc/img/05_colorbar.png)

### Exotic colormaps

If your data span −2 to 5, `cmap='RdBu_r'` puts white at **1.5**. Half your
"blue" values are positive numbers. `center=0` re-anchors the colormap so white
means zero, without clipping the range.

```python
ax.imshow(data, vmin=-2, vmax=5, cmap=get_bounded_cmap('RdBu_r', -2, 0, 5))
mplp(colorbar=True, cmap='RdBu_r', vmin=-2, center=0, vmax=5)
```

![bounded colormap](doc/img/06_bounded_cmap.png)

### Scalebars instead of axes

For traces where the absolute values are meaningless but the scale isn't —
ephys, imaging, anything with a time base.

```python
mplp(hide_axis=True,
     xscalebar=5, yscalebar=200,
     xscalebar_unit=' ms', yscalebar_unit=' μV')
```

![scalebar](doc/img/07_scalebar.png)

### `size=` — one figure, three media

The most common figure reformatting need: scaling a figure's "metadata" with respect to its data for different media. `size` rescales fonts, spine widths, tick widths, colorbar thickness and scalebar text for the viewing distance..

```python
mplp(size='paper')    # or 'slide' (default), 'poster'
mplp(size='xs')       # or 's', 'm', 'l', 'xl', 'xxl'
```

![size presets](doc/img/08_sizes.png)

### Bonus: color families for nested designs

Genotype × dose, region × condition, subject × session. One hue per group, one
shade within it — so the structure of the design is visible without reading the
legend.

```python
families = get_color_families(ncolors=3, nfamilies=3, cmapstr='viridis')
```

![color families](doc/img/12_color_families.png)

Plus the usual conveniences:

```python
get_ncolors_cmap(8, 'viridis')      # N evenly spaced colors from any colormap
to_hex((70, 130, 180))              # accepts 0-1 or 0-255, hex, names, 'r'
html_palette(colors)                # preview swatches inline in a notebook
```

![palettes](doc/img/10_palettes.png)

### Everything at once

```python
mplp(xlabel='Feature 1', ylabel='Feature 2',
     colorbar=True, vmin=c.min(), vmax=c.max(), cmap='magma', clabel='F1 + F2',
     hlines=[y.mean()], vlines=[x.mean()],
     lines_kwargs={'lw': 1, 'ls': '--', 'color': 'grey', 'zorder': -1})
```

![everything](doc/img/09_everything.png)

Four lines. Just to bring the point home, here is the raw matplotlib code that would be needed to produces the exact same panel (i.e. that an LLM would provide):

```python
### Raw matplotlib code - much more verbose..!
import numpy as np
from matplotlib.font_manager import FontProperties
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# labels, title, fonts
ax.set_xlabel('Feature 1', size=18, weight='regular', labelpad=0, fontname='Arial')
ax.set_ylabel('Feature 2', size=18, weight='regular', labelpad=0, fontname='Arial')
ax.set_title('by hand', size=20, weight='regular')

# tick labels — set_ticks() first, or matplotlib warns and may mislabel them
fig.canvas.draw()
xticks, yticks = ax.get_xticks(), ax.get_yticks()
ax.set_xticks(xticks)
ax.set_xticklabels([f'{t:g}' for t in xticks], fontsize=16, fontweight='regular',
                   color=(0, 0, 0), rotation=0, ha='center', va='top', fontname='Arial')
ax.set_yticks(yticks)
ax.set_yticklabels([f'{t:g}' for t in yticks], fontsize=16, fontweight='regular',
                   color=(0, 0, 0), rotation=0, ha='right', va='center', fontname='Arial')
ax.set_xlim(xlim); ax.set_ylim(ylim)   # ticks just widened your limits. put them back

# spines and ticks
ax.tick_params(axis='both', bottom=1, left=1, top=0, right=0,
               width=1, length=4, direction='out')
for sp in ('left', 'bottom'):
    ax.spines[sp].set_lw(1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# reference lines
ax.axhline(y=y.mean(), lw=1, ls='--', color='grey', zorder=-1)
ax.axvline(x=x.mean(), lw=1, ls='--', color='grey', zorder=-1)

# a colorbar that doesn't steal width from the axis
cax = inset_axes(ax, width='3%', height='40%', loc='lower right',
                 bbox_to_anchor=(0.04, 0, 1, 1), bbox_transform=ax.transAxes,
                 borderpad=0)
sm = plt.cm.ScalarMappable(cmap='magma', norm=plt.Normalize(c.min(), c.max()))
sm.set_array([])
fig.colorbar(sm, cax=cax, ax=ax, orientation='vertical', label='F1 + F2')
cticks = np.arange(20, 141, 20)
cax.yaxis.set_ticks(cticks)
cax.yaxis.set_ticklabels([f'{t:g}' for t in cticks], ha='left')
cax.yaxis.set_tick_params(pad=5, labelsize=16)
cax.yaxis.label.set_font_properties(FontProperties(weight='regular', size=18))
cax.yaxis.label.set_rotation(-90)
cax.yaxis.label.set_va('bottom')
cax.yaxis.label.set_ha('center')
cax.yaxis.labelpad = 5

# line up labels across subplots, white figure background
fig.align_xlabels(fig.axes)
fig.align_ylabels(fig.axes)
fig.patch.set_facecolor('white')
```

**41 lines, three imports, six APIs, two footguns** (`set_ticklabels` before
`set_ticks` warns and can silently mislabel your axis; setting ticks quietly
widens your limits, so you have to restore them afterwards).

### `prettify=False` — surgical mode

Sometimes you've already got a figure you like and you want to change exactly one
thing. `prettify=False` applies *only* what you pass and leaves everything else
alone.

```python
mplp(prettify=False, hide_top_right=True)
```

![prettify false](doc/img/11_prettify.png)

---

## Cheat sheet

|  | Argument |
|---|---|
| Figure / axis size (inches) | `figsize=(w, h)`, `axsize=(w, h)` |
| Scale text for medium | `size='paper' / 'slide' / 'poster'` (also `xs`–`xxl`) |
| Limits | `xlim`, `ylim` |
| Tick positions | `xticks`, `yticks`, `reset_xticks`, `reset_yticks` |
| Tick label text | `xtickslabels`, `ytickslabels` |
| Tick label rotation / alignment | `xtickrot`, `ytickrot`, `xtickha`, `xtickva`, `ytickha`, `ytickva` |
| Font sizes | `title_s`, `axlab_s`, `ticklab_s`, `clabel_s`, `cticks_s` |
| Font weights | `title_w`, `axlab_w`, `ticklab_w`, `clabel_w` |
| Font family | `font_family` |
| Labels / title | `xlabel`, `ylabel`, `title`, `xlabelpad`, `ylabelpad` |
| Spines | `lw`, `hide_top_right`, `hide_axis` |
| Tick direction | `ticks_direction='in' / 'out'` |
| Legend | `show_legend`, `hide_legend`, `legend_loc=(x, y)` |
| Colorbar | `colorbar=True`, `vmin`, `vmax`, `cmap`, `center`, `clabel`, `cticks`, `ctickslabels`, `cbar_w`, `cbar_h`, `cbar_pad`, `clim` |
| Reference lines | `hlines`, `vlines`, `lines_kwargs` |
| Scalebars | `xscalebar`, `yscalebar`, `xscalebar_unit`, `yscalebar_unit`, `scalebarkwargs` |
| Subplot spacing | `hspace`, `wspace`, `tight_layout` |
| Label alignment across subplots | `align_x_labels`, `align_y_labels` |
| Transparent background | `transparent_background=True` |
| Save | `saveFig=True`, `saveDir`, `figname`, `_format` |
| Change only what I pass | `prettify=False` |

### Helpers exported alongside `mplp`

| Function | Does |
|---|---|
| `get_bestticks(start, end, step=None, light=False)` | Ticks on round numbers (1 / 5 / 10 steps) |
| `get_bestticks_from_array(arr, ...)` | Same, from data |
| `get_labels_from_ticks(ticks)` | Consistently formatted tick label strings |
| `sci_notation(1.23e6, 2)` | `1.23·10⁶` as mathtext |
| `get_cmap`, `get_bounded_cmap`, `get_ncolors_cmap`, `get_color_families` | Colormaps and palettes |
| `to_rgb`, `to_hex`, `to_hsv`, `html_palette` | Color conversion and preview |
| `add_colorbar(fig, ax, ...)` | The size-preserving colorbar, standalone |
| `plot_scalebar(ax, ...)` | Scalebars, standalone |
| `set_ax_size(ax, w, h)` | Exact axis dimensions in inches |
| `save_mpl_fig(fig, name, dir, fmt)` | Save with Type-42 (editable) text |

---

## Saving

```python
mplp(saveFig=True, saveDir='./figures', figname='fig2b', _format='pdf')
```

Saves at 500 dpi with `pdf.fonttype = 42`, i.e. **text stays text**. You can open the PDF in Illustrator/Inkscape and fix your typo without
re-running the analysis (You will. There is always a label to fix.)

---

## Changing the defaults

mplify's defaults live in one hand-editable file,
[`src/mplify/DEFAULT_PARAMS.py`](src/mplify/DEFAULT_PARAMS.py): `default_mplp_params` for the base style, `SIZE_PRESETS` for the paper/slide/poster xs/s/m/l/xl/xxl defaults.

Edit it and your next `mplp()` call picks the change up immediately — the file is re-read from disk whenever its mtime changes. No kernel restart or `%autoreload` needed.

```python
from mplify import default_mplp_params, SIZE_PRESETS  # snapshots, for inspection
```

---

## Not a style sheet, not a wrapper

- **Not a style sheet.** Style sheets set global `rcParams` across all figures; they can't rotate specific tick labels or put a colorbar on a specific axis. mplify operates per-axis, at call time, after your data is plotted.
- **Not a plotting wrapper.** mplify never draws your data. You keep `ax.plot`, `ax.imshow`, seaborn, whatever you already use (if it's built on top of matplotlib, of course).

---

## Development

```bash
uv sync                            # editable install into .venv
uv run python doc/make_figures.py  # regenerate the README figures into doc img/
```

The full gallery is [`quickstart.ipynb`](quickstart.ipynb) — open it in your editor of choice and point the kernel at `.venv`.

## Related

[NeuroPyxels](https://github.com/m-beau/NeuroPyxels) — Neuropixels data analysis, where this codebase slowly grew up since 2016.
