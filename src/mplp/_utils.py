"""Internal utilities for mplp."""

from ast import literal_eval as _ale

import matplotlib.pyplot as plt


def _isnumeric(x):
    """Check if a string represents a numeric value."""
    x = str(x).replace('\u2212', '-')
    try:
        _ale(x)
        return True
    except Exception:
        return False


def _pprint_dic(dic):
    """Pretty-print a dictionary for docstrings."""
    kv = "".join([f"    {k}: {v},\n" for k, v in dic.items()])
    return "{\n" + kv + "}"


def _docstring_decorator(*args):
    """Decorator to format a function's docstring with the given arguments."""
    def decorate(f):
        f.__doc__ = f.__doc__.format(*args)
        return f
    return decorate


def set_ax_size(ax, w, h):
    """Set axis size in inches within the existing figure.

    Repositions the axis (centered at its current center) so that it
    occupies exactly w × h inches, without changing the figure size.
    Warns if the requested size exceeds the figure dimensions.

    Arguments:
        - ax: matplotlib axis (or None to use current axis)
        - w: width in inches
        - h: height in inches
    """
    import warnings

    if ax is None:
        ax = plt.gca()

    fig = ax.get_figure()
    fig_w, fig_h = fig.get_size_inches()

    if w > fig_w or h > fig_h:
        warnings.warn(
            f"Requested axis size ({w}\" × {h}\") exceeds figure size "
            f"({fig_w}\" × {fig_h}\"). The axis will be clipped. "
            f"Increase figsize or reduce axsize.",
            UserWarning,
            stacklevel=2,
        )

    # Convert desired inches to figure-fraction coordinates
    frac_w = w / fig_w
    frac_h = h / fig_h

    # Keep the axis centered at its current center
    cur_pos = ax.get_position()
    cx = (cur_pos.x0 + cur_pos.x1) / 2
    cy = (cur_pos.y0 + cur_pos.y1) / 2

    new_x0 = cx - frac_w / 2
    new_y0 = cy - frac_h / 2

    # Clamp to figure bounds so the axis stays visible
    new_x0 = max(0, min(new_x0, 1 - frac_w))
    new_y0 = max(0, min(new_y0, 1 - frac_h))

    ax.set_position([new_x0, new_y0, frac_w, frac_h])
