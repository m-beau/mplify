"""Generate the PNGs used in README.md.

Run from the repo root:
    uv run python doc/make_figures.py

Every figure here is also a cell in quickstart.ipynb — this script just
renders them to doc/img/ at a fixed dpi so the README looks the same
everywhere.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from mplify import (mplp, get_bounded_cmap,
                    get_ncolors_cmap, get_color_families)

OUT = __import__('pathlib').Path(__file__).parent / 'img'
OUT.mkdir(parents=True, exist_ok=True)
DPI = 160


def save(fig, name):
    p = OUT / f'{name}.png'
    fig.savefig(p, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'  wrote {p}')


x = np.linspace(0, 10, 200)
y = np.sin(x) * np.exp(-x / 5)


# ---------------------------------------------------------------- 1. hero
def fig_hero():
    """3 panels: raw matplotlib, bare mplp(), then mplp() with arguments.

    The third panel is saved by mplp itself (saveFig/saveDir/figname/_format),
    so this figure is also a live test of the saving path.
    """
    y2 = 0.8 * np.sin(x - 0.7) * np.exp(-x / 8)
    fig, axes = plt.subplots(1, 3, figsize=(15, 3.6))
    for ax in axes:
        ax.plot(x, y, lw=2, color='#3B6EA5', label='data')
        ax.plot(x, y2, lw=2, color='#C4553B', label='model')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude (a.u.)')
    axes[0].legend()
    axes[0].set_title('matplotlib defaults')

    mplp(ax=axes[1], title='mplp()')

    mplp(ax=axes[2],
         xlim=(0, 3 * np.pi), ylim=(-0.55, 0.85),
         xticks=[0, np.pi, 2 * np.pi, 3 * np.pi],
         xtickslabels=['0', 'π', '2π', '3π'],
         xtickrot=45, xtickha='right',
         yticks=[-0.4, 0, 0.4, 0.8],
         xlabel='Phase', ylabel='Amplitude (a.u.)', title='mplp(**kwargs)',
         hlines=[0], lines_kwargs={'lw': 1.5, 'ls': ':', 'color': 'grey'},
         show_legend=True, legend_loc=(0.6, 0.62),
         ticks_direction='in', lw=2, ticklab_s=15,
         hspace=0.1, wspace=0.35,
         saveFig=True, saveDir=str(OUT), figname='01_hero', _format='png')
    plt.close(fig)
    print(f"  wrote {OUT / '01_hero.png'}")


# ------------------------------------------------------- 2. axes / ticks
def fig_axes():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    for ax in axes:
        ax.plot(x, y, lw=2, color='#3B6EA5')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude (a.u.)')
    axes[0].set_title('matplotlib defaults')
    mplp(ax=axes[1],
         xlim=(0, 8), ylim=(-0.5, 1),
         xticks=[0, 2, 4, 6, 8], yticks=[-0.5, 0, 0.5, 1],
         xlabel='Time (s)', ylabel='Amplitude (a.u.)',
         title='limits + ticks, one call',
         tight_layout=True)
    save(fig, '02_axes')


# ----------------------------------------------- 3. rotated tick labels
def fig_ticklabels():
    categories = ['Condition A', 'Condition B', 'Condition C', 'Control']
    values = [3.2, 4.8, 2.1, 5.5]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    for ax in axes:
        ax.bar(range(len(values)), values, color='#3B6EA5')
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels(categories)
        ax.set_ylabel('Response')
    axes[0].set_title('matplotlib defaults')
    mplp(ax=axes[1],
         xticks=range(len(values)), xtickslabels=categories,
         xtickrot=30, xtickha='right',
         ylabel='Response', title='rotate + realign labels',
         tight_layout=True)
    save(fig, '03_ticklabels')


# ----------------------------------------------------- 4. reference lines
def fig_lines():
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    for ax in axes:
        ax.plot(x, y, lw=2, color='#3B6EA5')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    axes[0].axhline(y=0, lw=1.5, ls='--', color='k')
    axes[0].axvline(x=np.pi, lw=1.5, ls='--', color='k')
    axes[0].axvline(x=2 * np.pi, lw=1.5, ls='--', color='k')
    axes[0].set_title('matplotlib defaults')
    mplp(ax=axes[1],
         hlines=[0], vlines=[np.pi, 2 * np.pi],
         lines_kwargs={'lw': 2, 'ls': ':', 'color': 'grey'},
         xlabel='x', ylabel='y', title='hlines / vlines',
         tight_layout=True)
    save(fig, '04_lines')


# ---------------------------------------------------------- 5. colorbar
def fig_colorbar():
    data = np.random.default_rng(42).normal(size=(20, 30))
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    for ax in axes:
        im = ax.imshow(data, aspect='auto', cmap='RdBu_r', vmin=-3, vmax=3)
        ax.set_xlabel('Feature')
        ax.set_ylabel('Sample')
    plt.colorbar(axes[0].images[0], ax=axes[0])
    axes[0].set_title('matplotlib defaults')
    mplp(ax=axes[1],
         colorbar=True, vmin=-3, vmax=3, cmap='RdBu_r',
         clabel='Z-score', cticks=[-2, 0, 2], cbar_pad=0.02,
         xticks=[0, 10, 20], yticks=[0, 5, 10, 15],
         xlabel='Feature', ylabel='Sample',
         title='colorbar that keeps the axis size')
    save(fig, '05_colorbar')


# ------------------------------------------------- 6. bounded colormap
def fig_bounded():
    data_asym = np.tile(np.arange(-2, 6)[:, None], (1, 10))

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    # left: plain RdBu_r over [-2, 5] — white lands at 1.5, so half the
    # 'negative-looking' blues are actually positive numbers
    axes[0].imshow(data_asym, aspect='auto', cmap='RdBu_r', vmin=-2, vmax=5)
    plt.colorbar(axes[0].images[0], ax=axes[0])
    axes[0].set_title('matplotlib defaults\nwhite sits at 1.5')
    axes[0].set_xticks([]); axes[0].set_yticks([])

    # right: same range, but the colormap is re-anchored so white == 0
    axes[1].imshow(data_asym, aspect='auto', vmin=-2, vmax=5,
                   cmap=get_bounded_cmap('RdBu_r', -2, 0, 5))
    mplp(ax=axes[1],
         title='center=0\nwhite sits at 0',
         colorbar=True, cmap='RdBu_r', vmin=-2, center=0, vmax=5,
         cbar_h=0.8, cticks=[-2, 0, 2, 4],
         xticks=[], yticks=[])
    save(fig, '06_bounded_cmap')


# --------------------------------------------------------- 7. scalebars
def fig_scalebar():
    rng = np.random.default_rng(42)
    fs, duration, n_channels = 30_000, 0.05, 4
    t = np.arange(0, duration, 1 / fs) * 1000
    traces = rng.normal(0, 30, (n_channels, len(t)))
    spike_t = int(0.02 * fs)
    spike_wave = -200 * np.exp(-((np.arange(30) - 10) ** 2) / 8)
    for ch in range(n_channels):
        traces[ch, spike_t:spike_t + 30] += spike_wave * (1 - 0.2 * ch)
    offsets = np.arange(n_channels) * 400

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    for ax in axes:
        for ch in range(n_channels):
            ax.plot(t, traces[ch] + offsets[ch], color='k', lw=0.5)
    axes[0].set_title('matplotlib defaults')
    axes[0].set_xlabel('Time (ms)')
    axes[0].set_ylabel('Voltage (μV)')
    mplp(ax=axes[1],
         hide_axis=True,
         xscalebar=5, yscalebar=200,
         xscalebar_unit=' ms', yscalebar_unit=' μV',
         scalebarkwargs={'loc': 'right', 'fontsize': 12, 'lw': 4},
         title='axes → scalebars', tight_layout=True)
    save(fig, '07_scalebar')


# ------------------------------------------------------- 8. size presets
def fig_sizes():
    rng = np.random.default_rng(7)
    n = 150
    xd = rng.normal(50, 15, n)
    yd = 0.6 * xd + rng.normal(0, 8, n)
    c = xd + yd
    # Each medium gets the axis size it would really have: a paper panel is
    # small and read up close, a poster panel is big and read from afar.
    # size= scales the text/lines to match, so all three read the same.
    sizes = [('paper', (1.7, 1.4)), ('slide', (2.5, 2.0)), ('poster', (3.4, 2.7))]
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.5))
    for ax, (size, axsize) in zip(axes, sizes):
        ax.scatter(xd, yd, c=c, cmap='magma', s=25, alpha=0.8)
        mplp(ax=ax, size=size, axsize=axsize, wspace=1.0,
             align_x_labels=False, align_y_labels=False,
             xlabel='Feature 1', ylabel='Feature 2',
             xticks=[20, 40, 60, 80], yticks=[0, 20, 40, 60],
             title=f"size='{size}'",
             colorbar=True, vmin=c.min(), vmax=c.max(), cticks=[40, 80, 120],
             cmap='magma', clabel='F1 + F2')
    save(fig, '08_sizes')


# ---------------------------------------------------- 9. kitchen sink
def fig_everything():
    rng = np.random.default_rng(7)
    n = 150
    xd = rng.normal(50, 15, n)
    yd = 0.6 * xd + rng.normal(0, 8, n)
    c = xd + yd
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax in axes:
        ax.scatter(xd, yd, c=c, cmap='magma', s=25, alpha=0.8)
        ax.set_xlabel('Feature 1')
        ax.set_ylabel('Feature 2')
    plt.colorbar(axes[0].collections[0], ax=axes[0], label='F1 + F2')
    axes[0].axhline(yd.mean(), lw=1, ls='--', color='grey', zorder=-1)
    axes[0].axvline(xd.mean(), lw=1, ls='--', color='grey', zorder=-1)
    axes[0].set_title('matplotlib defaults')
    mplp(ax=axes[1],
         xlabel='Feature 1', ylabel='Feature 2', title='one mplp() call',
         colorbar=True, vmin=c.min(), vmax=c.max(), cmap='magma',
         clabel='F1 + F2',
         hlines=[yd.mean()], vlines=[xd.mean()],
         lines_kwargs={'lw': 1, 'ls': '--', 'color': 'grey', 'zorder': -1})
    save(fig, '09_everything')


# --------------------------------------------------------- 10. palettes
def fig_palettes():
    fams = get_color_families(ncolors=3, nfamilies=4)
    seq = get_ncolors_cmap(8, 'viridis')
    fig, axes = plt.subplots(2, 1, figsize=(8, 2.6),
                             gridspec_kw={'hspace': 0.9})
    for i, c in enumerate(seq):
        axes[0].add_patch(plt.Rectangle((i, 0), 0.94, 1, color=c))
    axes[0].set_xlim(0, len(seq)); axes[0].set_ylim(0, 1)
    axes[0].set_title("get_ncolors_cmap(8, 'viridis')", size=13, loc='left')

    k = 0
    for fam in fams:
        for c in fam:
            axes[1].add_patch(plt.Rectangle((k, 0), 0.94, 1, color=c))
            k += 1
        k += 0.6
    axes[1].set_xlim(0, k); axes[1].set_ylim(0, 1)
    axes[1].set_title('get_color_families(ncolors=3, nfamilies=4)',
                      size=13, loc='left')
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
    save(fig, '10_palettes')


# ------------------------------------------------- 11. prettify=False
def fig_prettify():
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.5))
    for ax in axes:
        ax.plot(x, y, lw=2, color='#3B6EA5')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    axes[0].set_title('matplotlib defaults')
    mplp(ax=axes[1], title='prettify=True (default)')
    mplp(ax=axes[2], prettify=False, title='prettify=False',
         hide_top_right=True, tight_layout=True)
    save(fig, '11_prettify')


# ----------------------------------------- 12. color families in action
def fig_families():
    """Grouped bars: 3 genotypes x 3 doses. Genotype = hue family,
    dose = shade within the family — readable at a glance, and still
    readable in greyscale."""
    rng = np.random.default_rng(3)
    genotypes = ['WT', 'Het', 'KO']
    doses = ['0 mg', '1 mg', '10 mg']
    means = np.array([[4.1, 3.6, 2.9],
                      [3.4, 2.7, 2.0],
                      [2.2, 1.6, 1.1]])
    sems = rng.uniform(0.12, 0.3, means.shape)

    families = get_color_families(ncolors=3, nfamilies=3, cmapstr='viridis')

    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    width = 0.25
    idx = np.arange(len(genotypes))

    # left: matplotlib's default cycle — three unrelated colors, no structure
    for j, dose in enumerate(doses):
        axes[0].bar(idx + (j - 1) * width, means[:, j], width,
                    yerr=sems[:, j], capsize=3, label=dose)
    axes[0].set_xticks(idx); axes[0].set_xticklabels(genotypes)
    axes[0].set_ylabel('Firing rate (Hz)')
    axes[0].legend()
    axes[0].set_title('matplotlib defaults')

    # right: one color family per genotype, one shade per dose
    for i, gen in enumerate(genotypes):
        for j, dose in enumerate(doses):
            axes[1].bar(i + (j - 1) * width, means[i, j], width,
                        yerr=sems[i, j], capsize=3,
                        color=families[i][j], ecolor='k',
                        label=dose if i == 0 else None)
    mplp(ax=axes[1],
         xticks=idx, xtickslabels=genotypes,
         ylim=(0, 5.4), yticks=[0, 1, 2, 3, 4, 5],
         ylabel='Firing rate (Hz)',
         title='get_color_families()',
         show_legend=True, legend_loc=(0.62, 0.5),
         tight_layout=True)
    save(fig, '12_color_families')


if __name__ == '__main__':
    print('Generating README figures...')
    for f in (fig_hero, fig_axes, fig_ticklabels, fig_lines, fig_colorbar,
              fig_bounded, fig_scalebar, fig_sizes, fig_everything,
              fig_palettes, fig_prettify, fig_families):
        f()
    print('Done.')
