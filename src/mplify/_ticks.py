"""Tick generation and formatting utilities."""

import numpy as np
from math import floor, log10


def _myceil(x, base=5):
    return base * np.ceil(x / base)


def _myfloor(x, base=5):
    return base * np.floor(x / base)


def _ceil_power10(x):
    return 10 ** np.ceil(np.log10(x))


def _n_decimals(x):
    x_str = str(x)
    if '.' not in x_str:
        return 0
    return len(x_str.split('.')[1])


def get_bestticks(start, end, step=None, light=False):
    """Generate evenly spaced ticks between start and end
    (smartly spaced by 1, 5, or 10).

    If start=0 and end=10, ticks will be np.arange(0,10,1).
    If start=0 and end=50, ticks will be np.arange(0,50,5).

    Arguments:
        - start, end: Range bounds
        - step: Tick spacing (auto-calculated if None)
        - light: If True, doubles the step size (sparser ticks)
    """
    span = abs(end - start)
    if step is None:
        upper10 = _ceil_power10(span)
        if span <= upper10 / 5:
            step = upper10 * 0.01
        elif span <= upper10 / 2:
            step = upper10 * 0.05
        else:
            step = upper10 * 0.1
    if light:
        step *= 2
    if step >= span:
        raise ValueError(f'Step {step} exceeds span {span}')

    ticks = np.arange(_myceil(start, step), _myfloor(end, step) + step, step)
    decimals = _n_decimals(step)
    ticks = ticks.astype(int) if decimals <= 0 else np.round(ticks, decimals)

    return ticks if start <= end else ticks[::-1]


def get_bestticks_from_array(arr, step=None, light=False):
    """Generate evenly spaced ticks spanning an array's range.

    Arguments:
        - arr: Array or list of values
        - step: Tick spacing (auto-calculated if None)
        - light: If True, doubles the step size (sparser ticks)
    """
    return get_bestticks(np.min(arr), np.max(arr), step, light)


def get_labels_from_ticks(ticks, max_decimals=4, trim_zeros=True):
    """Format numerical tick values into consistently formatted string labels.

    Arguments:
        - ticks: Array of numerical values to format
        - max_decimals: Maximum number of decimal places to consider
        - trim_zeros: If True, remove trailing zeros after decimal point

    Returns:
        - list of formatted labels
        - number of decimal places used
    """
    ticks = np.asarray(ticks)

    # Find optimal decimal precision (up to max_decimals)
    decimals_needed = max_decimals
    for d in range(max_decimals + 1):
        if np.allclose(ticks, np.round(ticks, d)):
            decimals_needed = d
            break

    # Format tick labels
    if decimals_needed == 0:
        ticks_labels = list(ticks.astype(int))
        string_shift = 1
    else:
        ticks_labels = list(np.round(ticks, decimals_needed))
        string_shift = 2

    for i, label in enumerate(ticks_labels):
        label = str(label) + '0' * (decimals_needed + string_shift - len(str(label).replace('-', '')))
        if trim_zeros and '.' in label:
            label = label.rstrip('0').rstrip('.')
        ticks_labels[i] = label

    return ticks_labels, decimals_needed


def sci_notation(num, decimal_digits=1, precision=None, exponent=None):
    """Format a number in scientific notation for LaTeX/Mathtext.

    Arguments:
        - num: The number to format
        - decimal_digits: Number of significant decimal digits
        - precision: Number of decimal digits to show (defaults to decimal_digits)
        - exponent: Explicit exponent to use (auto-calculated if None)
    """
    if exponent is None:
        exponent = int(floor(log10(abs(num))))
    coeff = round(num / float(10 ** exponent), decimal_digits)
    if precision is None:
        precision = decimal_digits
    return r"${0:.{2}f}\cdot10^{{{1:d}}}$".format(coeff, exponent, precision)
