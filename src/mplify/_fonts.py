"""Font detection and matplotlib rcParam setup for mplify.

For mplify's editable default styling values (default_mplp_params,
SIZE_PRESETS), see DEFAULT_PARAMS.py instead — that's the file meant to be
hand-edited, and mplp() re-reads it live so changes there take effect on
your very next mplp() call, no kernel restart or %autoreload needed.
"""

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
