import matplotlib.pyplot as plt
import matplotlib.lines as mlines


def slopechart(data, *, x, y, group, x_items=None,
    increase_color='tab:red', decrease_color='tab:blue', even_color='dimgray', size=8, fmt='{:.0f}', margin=0, ax=None):
    """Draw a slope chart.

    Args:
        data (`pandas.DataFrame`):
            Input data should be a long form.
        x, y (keys in `data`):
            Variables that specify posisions on the x and y axes.
        group (key in `data`):
            Grouping variable that will produce differnt lines.
        x_items (vector of strings, optional):
            Specify the levels and the order of plotting for the `x` semantic.
            Defaults to the all values in `x`.
        increase_color, decrease_color, even_color (strings, optional):
            Colors of the lines and the markers.
            Increase/decrease will be determined from the first values and the last values.
            Defaults to 'tab:red' as increase, 'tab:blue' as decrease, or 'dimgray' as even.
        size (float, optional):
            Radius of the markers, in points.
            Defaults to 8.
        fmt (string, optional):
            Format string of annotations.
            Defaults to '{:.0f}'.
        margin (float, optional):
            When the difference between the first value and the last value is within `margin`,
            the two values are considered equal, whose colors are `even_color`.
            If margin is under 0, it will be set as 0.
            Defaults to 0.
        ax (`matplotlib.axes.Axes`, optional):
            Pre-existing axes for the plot. Otherwise, generate new figure internally.

    Returns:
        `matplotlib.axes.Axes`:
            The matplotlib axes containing the plot.
    """

    if x_items is None:
        x_items = sorted(data[x].dropna().unique())
    lebel = data.query(f"{x} in @x_items")[group].value_counts(sort=False).loc[lambda x: x == len(x_items)].index.to_list()

    # Data to points
    series = []
    x_values = []
    for i, xi in enumerate(x_items):
        series.append(
            data.query(f"{group} in @lebel and {x} == @xi").set_index(group).loc[lebel, y].to_list()
        )
        x_values.append(1 + i * 2 / (len(x_items)-1))

    # Line colors
    colors = []
    margin = max(margin, 0)
    for y0, y1, c in zip(series[0], series[-1], lebel):
        if y1 > y0 + margin:
            colors.append(increase_color)
        elif y1 < y0 - margin:
            colors.append(decrease_color)
        else:
            colors.append(even_color)

    def newline(p1, p2, color):
        ax_ = plt.gca()
        l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=color)
        ax_.add_line(l)
        return l

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(8, 8))

    # Vertical Lines
    for x_val in x_values:
        ax.axvline(x=x_val, ymin=0.02, ymax=0.98, color='black', alpha=0.7, linewidth=1, linestyle='dotted')

    # Points
    for ser, x_val in zip(series, x_values):
        ax.scatter(y=ser, x=[x_val] * len(lebel), s=size**2, color=colors, zorder=10)

    # Line Segments
    for k in range(len(x_items)-1):
        for p1, p2, c in zip(series[k], series[k+1], colors):
            newline([x_values[k], p1], [x_values[k+1], p2], c)

    # Annotation
    for p1, p2, c in zip(series[0], series[-1], lebel):
        if p1 > 0:
            ax.text(x_values[0] - 0.05, p1, f'{c}, {fmt.format(p1)}', ha='right', va='center')
        if p2 > 0:
            ax.text(x_values[-1] + 0.05, p2, f'{c}, {fmt.format(p2)}', ha='left', va='center')

    # Decoration
    ax.set_title(y)
    ax.set(xlim=(x_values[0] - 1, x_values[-1] + 1))
    ax.set_xticks(x_values)
    ax.set_xticklabels(x_items)
    ax.grid(False)
    for pos in ['top', 'bottom', 'right']:
        ax.spines[pos].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.xaxis.set_ticks_position('none')

    return ax


def dumbbellchart(data, *, x, y, group, group_items=None,
    beforecolor='dimgray', aftercolor='tab:red', edgecolor='gray', size=8, ax=None):
    """Draw a dumbbell chart.

    Args:
        data (`pandas.DataFrame`):
            Input data should be a long form.
            Data will be internally sorted by the `x` values assigned to AFTER.
        x, y (keys in `data`):
            Variables that specify posisions on the x and y axes.
            `x` should be numeric data, and `y` should be categorical data.
        group (key in `data`):
            Grouping variable that will produce differnt markers, BEFORE and AFTER.
        group_items (vector of strings, optional):
            Specify BEFORE and AFTER for categorical levels of the `group` semantic.
            It must be iterable, and the length of it must be 2.
            Defaults to the all values in `group`.
        beforecolor, aftercolor, edgecolor (str, optional):
            Colors of the markers and the lines.
            Defaults to 'dimgray' as BEFORE, 'tab:red' as AFTER, or 'gray' as EDGE.
        size (float, optional):
            Radius of the markers, in points.
            Defaults to 8.
        ax (`matplotlib.axes.Axes`, optional):
            Pre-existing axes for the plot. Otherwise, generate new figure internally.

    Returns:
        `matplotlib.axes.Axes`:
            The matplotlib axes containing the plot.
    """

    if group_items is None:
        group_items = sorted(data[group].dropna().unique())
    assert len(group_items) == 2, 'Length of `group_items` must be 2.'

    # Data to points
    _data = (data
        .pivot_table(values=x, index=y, columns=group)
        [group_items]
        .dropna()
        .sort_values(group_items[1])
        .reset_index()
    )

    def newline(p1, p2):
        ax_ = plt.gca()
        l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=edgecolor)
        ax_.add_line(l)
        return l

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(8, 8))

    # Points
    ax.scatter(y=_data.index, x=_data[group_items[0]], s=size**2, color=beforecolor, label=group_items[0], zorder=10)
    ax.scatter(y=_data.index, x=_data[group_items[1]], s=size**2, color=aftercolor, label=group_items[1], zorder=11)

    # Line Segments
    for i, p1, p2 in zip(_data.index, _data[group_items[0]], _data[group_items[1]]):
        newline([p1, i], [p2, i])

    # Decoration
    ax.set_title(f"{x} - {group_items[0]} vs {group_items[1]}")
    ax.set(ylim=(-0.5, len(_data)-0.5))
    ax.set_yticks(_data.index.to_list())
    ax.set_yticklabels(_data[y])
    ax.grid(axis='x')
    for pos in ['top', 'bottom', 'left', 'right']:
        ax.spines[pos].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.legend(loc='lower right')

    return ax

