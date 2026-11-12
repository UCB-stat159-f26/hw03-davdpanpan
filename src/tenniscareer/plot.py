"""Plot a player's career matches like the NYT Serena Williams graphic."""

import matplotlib.pyplot as plt

WON_COLOR = "deepskyblue"
LOST_COLOR = "purple"
LABEL_COLOR = "dimgray"
GRID_COLOR = "gainsboro"
ZERO_COLOR = "gray"


def plot_career(career):
    """Scatter plot of a player's age vs. how much older they were than each opponent.

    career is the data frame returned by get_career(). Returns the figure, which
    can be saved with fig.savefig("plot.png").
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for won, color, label in ((False, LOST_COLOR, "Match lost"), (True, WON_COLOR, "Match won")):
        rows = career[career["won"] == won]
        ax.scatter(rows["player_age"], rows["age_diff"], s=15, color=color,
                   alpha=0.8, linewidths=0, label=label)

    style_axes(ax)
    name, ages = career["player"].iloc[0], career["player_age"]
    ax.set_title(f"{name}’s Professional Matches, Age {int(ages.min())} to {int(ages.max())}",
                 fontweight="bold", pad=40)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.05), ncol=2, frameon=False)

    return fig


def style_axes(ax):
    """Apply the same style as the original graphic."""
    ax.axhline(0, color=ZERO_COLOR, lw=0.9)
    ax.grid(color=GRID_COLOR, lw=0.8)
    ax.set_axisbelow(True)
    ax.spines[:].set_visible(False)
    ax.xaxis.tick_top()
    ax.tick_params(length=0, labelcolor=LABEL_COLOR)
    ax.set_yticks([-20, -10, 0, 10, 20], ["−20", "−10", "Same age", "+10", "+20 years"])
    ax.set_ylabel("Older (+) or younger (−) than opponent", color=LABEL_COLOR)
