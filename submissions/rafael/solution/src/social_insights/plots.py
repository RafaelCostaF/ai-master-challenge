"""Shared chart style and small plotting helpers (one quiet look across notebooks)."""
import matplotlib.pyplot as plt
import pandas as pd

BLUE, ORANGE, GRAY, INK = "#2a78d6", "#eb6834", "#8a8984", "#52514e"


def apply_style() -> None:
    plt.rcParams.update({
        "figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.6,
        "axes.edgecolor": GRAY, "axes.titlesize": 11, "axes.titleweight": "bold",
        "axes.prop_cycle": plt.cycler(color=[BLUE, ORANGE]),
    })


def lift_bars(ax, table: pd.DataFrame, title: str, n: int = 12) -> None:
    """Horizontal lift bars (1 = average); significant rows (FDR) in blue, the rest gray."""
    rows = pd.concat([table.head(n // 2), table.tail(n // 2)]).drop_duplicates().iloc[::-1]
    labels = rows["feature"].str.replace("_distribution", "") + " = " + rows["value"]
    colors = [BLUE if s else GRAY for s in rows["significant"]]
    ax.barh(labels, rows["lift"] - 1, left=1, color=colors, height=0.6)
    ax.axvline(1, color=INK, linewidth=1)
    ax.set_title(title)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", labelsize=8)


def heatmap(ax, matrix: pd.DataFrame, title: str, cmap: str = "RdBu_r", vmin=None, vmax=None, fmt: str = "{:.1f}") -> None:
    im = ax.imshow(matrix.values, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    ax.set_xticks(range(matrix.shape[1]), matrix.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(matrix.shape[0]), matrix.index, fontsize=8)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, fmt.format(matrix.iat[i, j]), ha="center", va="center", fontsize=7)
    ax.grid(False)
    ax.set_title(title)
    plt.colorbar(im, ax=ax, shrink=0.8)
