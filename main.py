"""
main.py  ←  ONLY FILE YOU NEED TO RUN
══════════════════════════════════════════════════════════════════
0/1 Knapsack – Investment Portfolio Optimizer
──────────────────────────────────────────────
Real-world context:
  An investor has a fixed budget and must choose from a set of
  investment opportunities (stocks, bonds, real estate, etc.) to
  maximise total return.  Each investment is taken fully or not at
  all — no fractional positions.

Project structure
──────────────────
  main.py                  ← entry point (run this)
  data/
    generator.py           ← random dataset generation
  algorithms/
    dp_2d.py               ← DP with full 2D table  O(nW) time/space
    dp_1d.py               ← space-optimized DP     O(nW) time, O(W) space
    greedy.py              ← greedy by value/weight ratio
  analysis/
    comparator.py          ← DP vs greedy comparison + explanation
    complexity.py          ← complexity discussion
    real_world.py          ← real-world applications
    graphs.py              ← all 10 matplotlib charts
  utils/
    reporter.py            ← all printing / display helpers

Usage
──────
  python main.py
"""

import time

# ── Local imports ──────────────────────────────────────────────
from data.generator       import generate_investments
from algorithms.dp_2d     import knapsack_dp_2d
from algorithms.dp_1d     import knapsack_dp_1d
from algorithms.greedy    import knapsack_greedy
from analysis.comparator  import print_comparison, explain_greedy_failure
from analysis.complexity  import print_complexity
from analysis.real_world  import print_real_world
from analysis.graphs      import plot_all
from utils.reporter       import (
    section,
    print_dataset_summary,
    print_selected_items,
    print_timing,
    print_space_saving,
)

# ── Configuration ──────────────────────────────────────────────
N      = 100   # number of investment opportunities
BUDGET = 200   # total budget in $1 000s


def main() -> None:
    # ── 1. Generate dataset ────────────────────────────────────
    section("0/1 Knapsack – Investment Portfolio Optimizer")
    print(f"\n  Generating {N} random investment opportunities …")
    names, weights, values = generate_investments(N)
    print_dataset_summary(N, BUDGET, weights, values)

    # ── 2. DP with 2D table (optimal + backtracking) ───────────
    section("Dynamic Programming Solution (2D Table)")
    t0 = time.perf_counter()
    dp_return, dp_selected = knapsack_dp_2d(weights, values, BUDGET)
    dp_time = (time.perf_counter() - t0) * 1000

    print_selected_items(
        dp_selected, names, weights, values,
        BUDGET, dp_return,
        "Optimal Portfolio  –  DP 2D Table",
    )
    print_timing("DP 2D", dp_time)

    # ── 3. Space-optimized DP (1D rolling array) ───────────────
    section("Space-Optimized DP (1D Rolling Array)")
    t0 = time.perf_counter()
    dp1d_return = knapsack_dp_1d(weights, values, BUDGET)
    dp1d_time = (time.perf_counter() - t0) * 1000

    print(f"\n  Maximum return (1D DP) : ${dp1d_return}k")
    print(f"  Matches 2D result      : {dp1d_return == dp_return}")
    print_timing("DP 1D", dp1d_time)
    print_space_saving(N, BUDGET)

    # ── 4. Greedy approach ─────────────────────────────────────
    section("Greedy Approach (Value / Weight Ratio)")
    t0 = time.perf_counter()
    greedy_return, greedy_selected = knapsack_greedy(weights, values, BUDGET)
    greedy_time = (time.perf_counter() - t0) * 1000

    print_selected_items(
        greedy_selected, names, weights, values,
        BUDGET, greedy_return,
        "Greedy Portfolio  –  Ratio-Sorted",
    )
    print_timing("Greedy", greedy_time)

    # ── 5. Comparison ──────────────────────────────────────────
    print_comparison(
        dp_return, dp_selected, dp_time,
        greedy_return, greedy_selected, greedy_time,
    )

    # ── 6. Why greedy fails ────────────────────────────────────
    explain_greedy_failure(BUDGET, dp_return, greedy_return)

    # ── 7. Complexity analysis ─────────────────────────────────
    print_complexity(N, BUDGET)

    # ── 8. Real-world applications ─────────────────────────────
    print_real_world()

    print("=" * 65)
    print("  Done.")
    print("=" * 65 + "\n")

    # ── 9. Graphs ──────────────────────────────────────────────
    print("\n  Opening graphs window …  (close it to exit)\n")
    plot_all(
        names, weights, values, BUDGET,
        dp_return, dp_selected,
        greedy_return, greedy_selected,
    )


if __name__ == "__main__":
    main()
