import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


def slopechart(data, x, y, group, x_items=None, increasing_color='tab:orange', decreasing_color='tab:blue', fmt='{:.0f}', ax=None):
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
        increasing_color, decreasing_color (strings, optional):
            Colors of the lines and the markers.
            Increasing/decreasing will be determined from the first values and the last values.
            Defaults to 'tab:orange' as increasing, or 'tab:blue' as decreasing.
        fmt (string, optional):
            Format string of annotations.
            Defaults to '{:.0f}'.
        ax (_type_, optional):
            Pre-existing axes for the plot. Otherwise, generate new figure internally.

    Returns:
        `matplotlib.axes.Axes`: The matplotlib axes containing the plot.
    """

    default_color = 'black'

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
    for y0, y1, c in zip(series[0], series[-1], lebel):
        if y1 > y0:
            colors.append(increasing_color)
        elif y1 < y0:
            colors.append(decreasing_color)
        else:
            colors.append(default_color)


    def newline(p1, p2, color=default_color):
        ax_ = plt.gca()
        l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=color, marker='o', markersize=6)
        ax_.add_line(l)
        return l

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(14,14))

    # Vertical Lines
    for x_val in x_values:
        ax.axvline(x=x_val, ymin=0.02, ymax=0.98, color=default_color, alpha=0.7, linewidth=1, linestyle='dotted')

    # Points
    for ser, x_val in zip(series, x_values):
        ax.scatter(y=ser, x=[x_val] * len(lebel), s=10, color=default_color, alpha=0.7)

    # Line Segments
    for k in range(len(x_items)-1):
        for p1, p2, c in zip(series[k], series[k+1], colors):
            newline([x_values[k], p1], [x_values[k+1], p2], c)

    # Annotation
    for p1, p2, c in zip(series[0], series[-1], lebel):
        if p1:
            ax.text(x_values[0] - 0.05, p1, f'{c}, {fmt.format(p1)}', ha='right', va='center', fontdict={'size':14})
        if p2:
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
    ax.xaxis.set_ticks_position('none')

    return ax
