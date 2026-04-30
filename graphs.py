"""
analysis/graphs.py
───────────────────
All matplotlib visualisations for the Investment Knapsack project.

Charts produced (all shown in one figure with subplots):
  1. DP vs Greedy – total return bar chart
  2. Selected investments – cost vs return scatter (DP & greedy overlaid)
  3. All investments – cost vs return scatter coloured by category
  4. Value/weight ratio distribution – histogram
  5. DP selected portfolio – cost & return side-by-side bars
  6. Cumulative return as items are added (DP order)
  7. Budget utilisation – pie chart (used vs remaining)
  8. Category breakdown of DP-selected items – horizontal bar
  9. DP table heatmap (sampled rows/cols for readability)
 10. Return vs Cost scatter with ratio as colour map (all items)
"""

import matplotlib
matplotlib.use("TkAgg")          # works on Windows without a display server

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np


# ── Colour palette ─────────────────────────────────────────────
PALETTE = {
    "dp"         : "#2ecc71",   # green
    "greedy"     : "#e74c3c",   # red
    "neutral"    : "#3498db",   # blue
    "highlight"  : "#f39c12",   # orange
    "bg"         : "#1a1a2e",   # dark navy background
    "panel"      : "#16213e",   # slightly lighter panel
    "text"       : "#eaeaea",   # near-white text
    "grid"       : "#2c2c54",   # subtle grid lines
}

CATEGORY_COLORS = {
    "Stock"     : "#2ecc71",
    "Bond"      : "#3498db",
    "RealEstate": "#e67e22",
    "ETF"       : "#9b59b6",
    "Crypto"    : "#e74c3c",
    "Commodity" : "#1abc9c",
}


def _style_ax(ax, title: str = "", xlabel: str = "", ylabel: str = "") -> None:
    """Apply dark theme styling to an axes."""
    ax.set_facecolor(PALETTE["panel"])
    ax.tick_params(colors=PALETTE["text"], labelsize=8)
    ax.xaxis.label.set_color(PALETTE["text"])
    ax.yaxis.label.set_color(PALETTE["text"])
    ax.title.set_color(PALETTE["text"])
    for spine in ax.spines.values():
        spine.set_edgecolor(PALETTE["grid"])
    ax.grid(color=PALETTE["grid"], linestyle="--", linewidth=0.5, alpha=0.7)
    if title:
        ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=8)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=8)


# ══════════════════════════════════════════════════════════════
# Individual chart functions
# ══════════════════════════════════════════════════════════════

def _chart_dp_vs_greedy(ax, dp_return: int, greedy_return: int) -> None:
    """Bar chart: DP optimal vs Greedy total return."""
    methods = ["DP (Optimal)", "Greedy"]
    returns = [dp_return, greedy_return]
    colors  = [PALETTE["dp"], PALETTE["greedy"]]

    bars = ax.bar(methods, returns, color=colors, width=0.45,
                  edgecolor=PALETTE["text"], linewidth=0.8)

    for bar, val in zip(bars, returns):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(returns) * 0.01,
            f"${val}k",
            ha="center", va="bottom",
            color=PALETTE["text"], fontsize=9, fontweight="bold",
        )

    gap = dp_return - greedy_return
    ax.annotate(
        f"Gap: ${gap}k\n({gap/dp_return*100:.1f}% suboptimal)",
        xy=(1, greedy_return), xytext=(0.5, (dp_return + greedy_return) / 2),
        arrowprops=dict(arrowstyle="->", color=PALETTE["highlight"]),
        color=PALETTE["highlight"], fontsize=8, ha="center",
    )
    _style_ax(ax, "DP vs Greedy – Total Return", "Method", "Return ($k)")


def _chart_scatter_selected(
    ax,
    weights, values, names,
    dp_selected, greedy_selected,
) -> None:
    """Scatter: all items grey, DP selected green, greedy selected red."""
    all_idx = set(range(len(weights)))
    dp_set  = set(dp_selected)
    gr_set  = set(greedy_selected)
    neither = all_idx - dp_set - gr_set
    both    = dp_set & gr_set
    dp_only = dp_set - gr_set
    gr_only = gr_set - dp_set

    def _scatter(idx_set, color, label, zorder=2, marker="o", size=40):
        if idx_set:
            xs = [weights[i] for i in idx_set]
            ys = [values[i]  for i in idx_set]
            ax.scatter(xs, ys, c=color, label=label,
                       s=size, zorder=zorder, marker=marker,
                       edgecolors="white", linewidths=0.4, alpha=0.85)

    _scatter(neither, "#555577", "Not selected", zorder=1, size=20)
    _scatter(dp_only,  PALETTE["dp"],      "DP only",        zorder=3)
    _scatter(gr_only,  PALETTE["greedy"],  "Greedy only",    zorder=3)
    _scatter(both,     PALETTE["highlight"], "Both",         zorder=4, marker="*", size=90)

    ax.legend(fontsize=7, facecolor=PALETTE["panel"],
              labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])
    _style_ax(ax, "Selected Investments (DP vs Greedy)", "Cost ($k)", "Return ($k)")


def _chart_all_by_category(ax, weights, values, names) -> None:
    """Scatter: all investments coloured by category."""
    cat_map = {}
    for i, name in enumerate(names):
        cat = name.split("_")[0]
        cat_map.setdefault(cat, {"w": [], "v": []})
        cat_map[cat]["w"].append(weights[i])
        cat_map[cat]["v"].append(values[i])

    for cat, data in cat_map.items():
        ax.scatter(data["w"], data["v"],
                   c=CATEGORY_COLORS.get(cat, "#aaaaaa"),
                   label=cat, s=30, alpha=0.8,
                   edgecolors="white", linewidths=0.3)

    ax.legend(fontsize=7, facecolor=PALETTE["panel"],
              labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"],
              ncol=2)
    _style_ax(ax, "All Investments by Category", "Cost ($k)", "Return ($k)")


def _chart_ratio_histogram(ax, weights, values) -> None:
    """Histogram of value/weight ratios for all investments."""
    ratios = [v / w for v, w in zip(values, weights)]
    n, bins, patches = ax.hist(ratios, bins=20,
                                color=PALETTE["neutral"],
                                edgecolor=PALETTE["bg"], linewidth=0.6)

    # Colour bars by ratio magnitude
    norm = plt.Normalize(min(ratios), max(ratios))
    cmap = plt.cm.RdYlGn
    for patch, left in zip(patches, bins[:-1]):
        patch.set_facecolor(cmap(norm(left)))

    mean_r = np.mean(ratios)
    ax.axvline(mean_r, color=PALETTE["highlight"], linestyle="--", linewidth=1.2,
               label=f"Mean {mean_r:.2f}")
    ax.legend(fontsize=7, facecolor=PALETTE["panel"],
              labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])
    _style_ax(ax, "Value/Weight Ratio Distribution", "Ratio", "Count")


def _chart_dp_portfolio_bars(ax, weights, values, names, dp_selected) -> None:
    """Side-by-side bars: cost and return for each DP-selected investment."""
    if not dp_selected:
        ax.text(0.5, 0.5, "No items selected", transform=ax.transAxes,
                ha="center", color=PALETTE["text"])
        return

    # Show at most 25 items to keep the chart readable
    show = dp_selected[:25]
    labels = [names[i].replace("_", "\n") for i in show]
    costs   = [weights[i] for i in show]
    returns = [values[i]  for i in show]

    x = np.arange(len(show))
    w = 0.38
    ax.bar(x - w/2, costs,   width=w, label="Cost",   color=PALETTE["neutral"],  alpha=0.85)
    ax.bar(x + w/2, returns, width=w, label="Return", color=PALETTE["dp"],       alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=5, rotation=45, ha="right")
    ax.legend(fontsize=7, facecolor=PALETTE["panel"],
              labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])
    title_suffix = f" (first {len(show)})" if len(dp_selected) > 25 else ""
    _style_ax(ax, f"DP Portfolio – Cost vs Return{title_suffix}", "", "$k")


def _chart_cumulative_return(ax, weights, values, dp_selected) -> None:
    """Line chart: cumulative return as DP items are added one by one."""
    cumulative = []
    total = 0
    for i in dp_selected:
        total += values[i]
        cumulative.append(total)

    ax.plot(range(1, len(cumulative) + 1), cumulative,
            color=PALETTE["dp"], linewidth=2, marker="o",
            markersize=3, markerfacecolor=PALETTE["highlight"])
    ax.fill_between(range(1, len(cumulative) + 1), cumulative,
                    alpha=0.2, color=PALETTE["dp"])
    ax.axhline(total, color=PALETTE["highlight"], linestyle="--",
               linewidth=1, label=f"Final ${total}k")
    ax.legend(fontsize=7, facecolor=PALETTE["panel"],
              labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])
    _style_ax(ax, "Cumulative Return (DP Selection Order)",
              "Items Added", "Cumulative Return ($k)")


def _chart_budget_pie(ax, weights, dp_selected, budget: int) -> None:
    """Pie chart: budget used vs remaining."""
    used      = sum(weights[i] for i in dp_selected)
    remaining = budget - used

    sizes  = [used, remaining]
    labels = [f"Used\n${used}k", f"Remaining\n${remaining}k"]
    colors = [PALETTE["dp"], PALETTE["greedy"]]
    explode = (0.05, 0)

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, explode=explode,
        autopct="%1.1f%%", startangle=90,
        textprops={"color": PALETTE["text"], "fontsize": 8},
        wedgeprops={"edgecolor": PALETTE["bg"], "linewidth": 1.5},
    )
    for at in autotexts:
        at.set_color(PALETTE["bg"])
        at.set_fontweight("bold")

    ax.set_title("Budget Utilisation (DP)", fontsize=10,
                 fontweight="bold", color=PALETTE["text"], pad=8)


def _chart_category_breakdown(ax, names, weights, values, dp_selected) -> None:
    """Horizontal bar: total return per category in DP portfolio."""
    cat_return = {}
    cat_cost   = {}
    for i in dp_selected:
        cat = names[i].split("_")[0]
        cat_return[cat] = cat_return.get(cat, 0) + values[i]
        cat_cost[cat]   = cat_cost.get(cat, 0)   + weights[i]

    cats    = sorted(cat_return, key=cat_return.get, reverse=True)
    returns = [cat_return[c] for c in cats]
    costs   = [cat_cost[c]   for c in cats]
    colors  = [CATEGORY_COLORS.get(c, "#aaaaaa") for c in cats]

    y = np.arange(len(cats))
    ax.barh(y - 0.2, returns, height=0.35, color=colors,   label="Return", alpha=0.9)
    ax.barh(y + 0.2, costs,   height=0.35, color=colors,   label="Cost",
            alpha=0.45, hatch="//")

    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=8)
    ax.legend(fontsize=7, facecolor=PALETTE["panel"],
              labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])
    _style_ax(ax, "DP Portfolio – Category Breakdown", "$k", "")


def _chart_dp_heatmap(ax, weights, values, capacity: int) -> None:
    """
    Heatmap of a sampled portion of the DP table.
    Rows = first 30 items, Cols = every 5th budget unit up to capacity.
    """
    n_show  = min(30, len(weights))
    w_step  = max(1, capacity // 50)
    w_range = list(range(0, capacity + 1, w_step))

    # Build the sub-table
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if wi <= w and dp[i - 1][w - wi] + vi > dp[i][w]:
                dp[i][w] = dp[i - 1][w - wi] + vi

    sub = np.array([[dp[i][w] for w in w_range] for i in range(1, n_show + 1)])

    im = ax.imshow(sub, aspect="auto", cmap="YlGn", interpolation="nearest")
    plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02).ax.tick_params(
        colors=PALETTE["text"], labelsize=7)

    ax.set_xticks(range(0, len(w_range), max(1, len(w_range) // 8)))
    ax.set_xticklabels(
        [w_range[i] for i in range(0, len(w_range), max(1, len(w_range) // 8))],
        fontsize=7,
    )
    ax.set_yticks(range(n_show))
    ax.set_yticklabels([f"Item {i+1}" for i in range(n_show)], fontsize=6)
    _style_ax(ax, f"DP Table Heatmap (first {n_show} items)",
              "Budget ($k)", "Item")


def _chart_ratio_colormap(ax, weights, values, names, dp_selected) -> None:
    """Scatter of all items; colour = ratio, size = value, DP items marked."""
    ratios = [v / w for v, w in zip(values, weights)]
    sizes  = [v * 0.8 for v in values]

    sc = ax.scatter(weights, values, c=ratios, s=sizes,
                    cmap="RdYlGn", alpha=0.75,
                    edgecolors="white", linewidths=0.3)
    plt.colorbar(sc, ax=ax, fraction=0.03, pad=0.02,
                 label="Return/Cost Ratio").ax.tick_params(
        colors=PALETTE["text"], labelsize=7)

    # Outline DP-selected items
    dp_w = [weights[i] for i in dp_selected]
    dp_v = [values[i]  for i in dp_selected]
    ax.scatter(dp_w, dp_v, s=120, facecolors="none",
               edgecolors=PALETTE["dp"], linewidths=1.5,
               label="DP selected", zorder=5)
    ax.legend(fontsize=7, facecolor=PALETTE["panel"],
              labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])
    _style_ax(ax, "All Items – Return/Cost Ratio (colour) & Value (size)",
              "Cost ($k)", "Return ($k)")


# ══════════════════════════════════════════════════════════════
# Main entry point called from main.py
# ══════════════════════════════════════════════════════════════

def plot_all(
    names    : list,
    weights  : list,
    values   : list,
    capacity : int,
    dp_return    : int,
    dp_selected  : list,
    greedy_return: int,
    greedy_selected: list,
) -> None:
    """
    Build and display all 10 charts in a single maximised figure.

    Parameters
    ----------
    names, weights, values : investment dataset
    capacity               : total budget
    dp_return / dp_selected        : DP results
    greedy_return / greedy_selected: greedy results
    """
    # ── Figure setup ──────────────────────────────────────────
    fig = plt.figure(figsize=(22, 18), facecolor=PALETTE["bg"])
    fig.suptitle(
        "0/1 Knapsack – Investment Portfolio Analysis",
        fontsize=16, fontweight="bold",
        color=PALETTE["text"], y=0.98,
    )

    # 4-row × 3-col grid; last row uses 2 wide + 1 narrow
    gs = gridspec.GridSpec(
        4, 3,
        figure=fig,
        hspace=0.52,
        wspace=0.35,
        left=0.06, right=0.97,
        top=0.94, bottom=0.05,
    )

    ax1  = fig.add_subplot(gs[0, 0])   # DP vs Greedy bar
    ax2  = fig.add_subplot(gs[0, 1])   # scatter selected
    ax3  = fig.add_subplot(gs[0, 2])   # scatter by category
    ax4  = fig.add_subplot(gs[1, 0])   # ratio histogram
    ax5  = fig.add_subplot(gs[1, 1])   # DP portfolio bars
    ax6  = fig.add_subplot(gs[1, 2])   # cumulative return
    ax7  = fig.add_subplot(gs[2, 0])   # budget pie
    ax8  = fig.add_subplot(gs[2, 1])   # category breakdown
    ax9  = fig.add_subplot(gs[2, 2])   # DP heatmap
    ax10 = fig.add_subplot(gs[3, :])   # ratio colourmap (full width)

    # ── Draw each chart ───────────────────────────────────────
    _chart_dp_vs_greedy(ax1, dp_return, greedy_return)
    _chart_scatter_selected(ax2, weights, values, names, dp_selected, greedy_selected)
    _chart_all_by_category(ax3, weights, values, names)
    _chart_ratio_histogram(ax4, weights, values)
    _chart_dp_portfolio_bars(ax5, weights, values, names, dp_selected)
    _chart_cumulative_return(ax6, weights, values, dp_selected)
    _chart_budget_pie(ax7, weights, dp_selected, capacity)
    _chart_category_breakdown(ax8, names, weights, values, dp_selected)
    _chart_dp_heatmap(ax9, weights, values, capacity)
    _chart_ratio_colormap(ax10, weights, values, names, dp_selected)

    plt.show()
