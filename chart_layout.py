"""Calculate the plot geometry used by the training dashboard.

Build with Python 3.12, Transcrypt 3.9.5 and esbuild:
    python -m transcrypt -b -n -xt chart_layout.py
    esbuild __target__/chart_layout.js --bundle --minify --format=iife --global-name=trainingChart --banner:js="/*! Includes the Transcrypt runtime (Apache-2.0). See LICENSE-Transcrypt.txt. */" --outfile=chart-layout.js
"""

from math import floor, log10


def scale_step(values):
    peak = 1
    for value in values:
        peak = max(peak, value)
    target = peak / 4
    magnitude = 10 ** floor(log10(target))
    for factor in [1, 2, 2.5, 5, 10]:
        if factor * magnitude >= target:
            return factor * magnitude
    return 10 * magnitude


def layout(volume, progress, last_day):
    """Lay out two series of [day offset, value] pairs through last_day."""
    left, right, top, bottom = 57, 343, 27, 167
    span = max(1, last_day)

    def date_position(day):
        return left + day * (right - left) / span

    result = []
    for series in [volume, progress]:
        step = scale_step([pair[1] for pair in series])
        ticks = [[i * step, bottom - i * (bottom - top) / 4] for i in range(5)]
        points = [
            [date_position(day), bottom - value * (bottom - top) / (4 * step)]
            for day, value in series
        ]
        result.append([ticks, points])
    intervals = min(4, span)
    dates = [
        [day, date_position(day)]
        for day in [floor(i * last_day / intervals) for i in range(intervals + 1)]
    ] if last_day > 0 else [[0, left]]
    return [result[0], result[1], dates, left, right, bottom]
