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
    """Set axis size in inches.

    Arguments:
        - ax: matplotlib axis (or None to use current axis)
        - w: width in inches
        - h: height in inches
    """
    if ax is None:
        ax = plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w) / (r - l)
    figh = float(h) / (t - b)
    ax.figure.set_size_inches(figw, figh)
