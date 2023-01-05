import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from collections.abc import Iterable


def highlightplot(func, data, hue, highlights, color='gray', **kwargs):
    """Draw seaborn chart, highlighting the specific items.

    Args:
        func (functions of `seaborn`):
            Plotting function defined in `seaborn` function interface.
        data (`pandas.DataFrame`):
            Input data should be a long form.
        hue (keys in `data`):
            Grouping variable that will produce points with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
        highlights (str / vector of str):
            Specify the highlighted items for categorical levels of the `hue` semantic.
        color (str, optional):
            Colors of the non-highlighted markers.
            Defaults to 'gray'.

    Returns:
        `matplotlib.axes.Axes`: The matplotlib axes containing the plot.
    """

    if isinstance(highlights, (str, int)):
        data_hl = data[data[hue] == highlights].copy()
    elif isinstance(highlights, Iterable):
        data_hl = data[data[hue].isin(highlights)].copy()
    else:
        assert False, '`highlight` must be str or vector of str'

    try:
        data_hl[hue] = data_hl[hue].cat.remove_unused_categories()
    except AttributeError:
        pass

    func(data=data, color=color, **kwargs)
    func(data=data_hl, hue=hue, **kwargs)

    return plt.gca()


def slopechart(data, x, y, group, x_items=None, increase_color='tab:red', decrease_color='tab:blue', even_color='dimgray', fmt='{:.0f}', margin=0, ax=None):
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
        fmt (string, optional):
            Format string of annotations.
            Defaults to '{:.0f}'.
        margin (float, optional):
            When the difference between the first value and the last value is within `margin`, 
            colors of the lines and the markers are `even_color`.
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
    lebel = data.query(f"{x} in @x_items")[group].value_counts().loc[lambda x: x == len(x_items)].index.to_list()

    # Data to points
    series = []
    x_values = []
    for i, xi in enumerate(x_items):
        series.append(
            data.query(f"{group} in @lebel and {x} == @xi")[y].to_list()
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
        l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=color, marker='o', markersize=6)
        ax_.add_line(l)
        return l

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(14,14))

    # Vertical Lines
    for x_val in x_values:
        ax.axvline(x=x_val, ymin=0.02, ymax=0.98, color='black', alpha=0.7, linewidth=1, linestyle='dotted')

    # Points
    for ser, x_val in zip(series, x_values):
        ax.scatter(y=ser, x=[x_val] * len(lebel), s=10, color=even_color, alpha=0.7)

    # Line Segments
    for k in range(len(x_items)-1):
        for p1, p2, c in zip(series[k], series[k+1], colors):
            newline([x_values[k], p1], [x_values[k+1], p2], c)

    # Annotation
    for p1, p2, c in zip(series[0], series[-1], lebel):
        if p1 > 0:
            ax.text(x_values[0] - 0.05, p1, f'{c}, {fmt.format(p1)}', ha='right', va='center', fontdict={'size':14})
        if p2 > 0:
            ax.text(x_values[-1] + 0.05, p2, f'{c}, {fmt.format(p2)}', ha='left', va='center', fontdict={'size':14})

    # Decoration
    ax.set_title(y, fontdict={'size':22})
    ax.set(xlim=(x_values[0] - 1, x_values[-1] + 1))
    ax.set_xticks(x_values)
    ax.set_xticklabels(x_items)
    for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(14)
    ax.grid(visible=False)
    for pos in ['top', 'bottom', 'right']:
        ax.spines[pos].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.xaxis.set_ticks_position('none')

    return ax


def dumbbellchart(data, x, y, group, group_items=None, before_color='dimgray', after_color='tab:red', ax=None):
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
        before_color, after_color (str, optional):
            Colors of the markers.
            The color of lines between markers is the same as `before_color`.
            Defaults to 'dimgray' as BEFORE, or 'tab:red' as AFTER.
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
        l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=before_color)
        ax_.add_line(l)
        return l

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(14, 14))

    # Points
    ax.scatter(y=_data.index, x=_data[group_items[0]], s=50, color=before_color, label=group_items[0], zorder=10)
    ax.scatter(y=_data.index, x=_data[group_items[1]], s=50, color=after_color, label=group_items[1], zorder=11)

    # Line Segments
    for i, p1, p2 in zip(_data.index, _data[group_items[0]], _data[group_items[1]]):
        newline([p1, i], [p2, i])

    # Decoration
    ax.set_title(f"{x} - {group_items[0]} vs {group_items[1]}", fontdict={'size':22})
    ax.set(ylim=(-0.5, len(_data)-0.5))
    ax.set_yticks(_data.index.to_list())
    ax.set_yticklabels(_data[y])
    for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(14)
    ax.grid(axis='x')
    for pos in ['top', 'bottom', 'left', 'right']:
        ax.spines[pos].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    ax.legend(loc='lower right', fontsize=14)

    return ax

