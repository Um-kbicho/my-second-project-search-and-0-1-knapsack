"""
analysis/comparator.py
───────────────────────
Compares DP (optimal) vs Greedy results and explains
why the greedy approach fails for 0/1 knapsack.
"""

from utils.reporter import section, divider


def print_comparison(
    dp_return: int,
    dp_selected: list[int],
    dp_time_ms: float,
    greedy_return: int,
    greedy_selected: list[int],
    greedy_time_ms: float,
) -> None:
    """Print a side-by-side comparison table."""
    section("DP vs Greedy – Comparison")
    gap = dp_return - greedy_return
    pct = gap / dp_return * 100 if dp_return else 0

    print(f"""
  ┌──────────────────────────────────────────────────────────────┐
  │  Method          Return ($k)   Items   Runtime               │
  ├──────────────────────────────────────────────────────────────┤
  │  DP (optimal)    {dp_return:<13} {len(dp_selected):<7} {dp_time_ms:.2f} ms              │
  │  Greedy          {greedy_return:<13} {len(greedy_selected):<7} {greedy_time_ms:.2f} ms              │
  └──────────────────────────────────────────────────────────────┘
  Greedy is ${gap}k ({pct:.1f}%) below the true optimum.
""")


def explain_greedy_failure(
    budget: int,
    dp_return: int,
    greedy_return: int,
) -> None:
    """Explain with text and a concrete example why greedy fails."""
    section("Why Greedy Fails for 0/1 Knapsack")
    gap = dp_return - greedy_return

    print(f"""
  Greedy strategy: pick investments with the highest return/cost
  ratio first, then take the next best that still fits, and so on.

  This is OPTIMAL for the FRACTIONAL knapsack (you can take a
  partial position to fill the last dollar of budget exactly).

  For 0/1 knapsack it fails because:
  ┌─────────────────────────────────────────────────────────────┐
  │  Taking a high-ratio investment may consume budget that     │
  │  could have been used by several lower-ratio investments    │
  │  whose COMBINED return exceeds the single high-ratio one.  │
  └─────────────────────────────────────────────────────────────┘

  On this dataset (budget = ${budget}k):
    DP optimal return  : ${dp_return}k
    Greedy return      : ${greedy_return}k
    Suboptimality gap  : ${gap}k  ({gap/dp_return*100:.1f}% below optimal)

  ── Concrete toy example ──────────────────────────────────────
  Budget = $10k, three investments:

    A : cost=$6k, return=$8k  → ratio 1.33  ← greedy picks first
    B : cost=$5k, return=$6k  → ratio 1.20
    C : cost=$5k, return=$6k  → ratio 1.20

  Greedy picks A ($6k used), then neither B nor C fits → total $8k.
  DP     picks B + C ($10k used)                       → total $12k ✓

  The greedy algorithm has no look-ahead; it commits to locally
  optimal choices that can foreclose globally better combinations.
""")
