"""
algorithms/greedy.py
─────────────────────
Greedy heuristic for the 0/1 knapsack problem.

Strategy
────────
Sort investments by value-to-weight ratio (highest first).
Greedily pick each investment if it still fits in the remaining budget.

Why it is OPTIMAL for fractional knapsack
──────────────────────────────────────────
When you can take fractions of an item, always taking the highest
ratio item (or a fraction of it to fill the last gap) is provably
optimal by an exchange argument.

Why it FAILS for 0/1 knapsack
──────────────────────────────
You cannot take fractions.  A high-ratio item may consume budget
that could have been used by several lower-ratio items whose
combined return is greater.  The greedy algorithm has no look-ahead
and commits to locally optimal choices that can foreclose globally
better combinations.

Time  : O(n log n)  — dominated by the sort
Space : O(n)
"""


def knapsack_greedy(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> tuple[int, list[int]]:
    """
    Greedy 0/1 knapsack by value/weight ratio.

    Parameters
    ----------
    weights  : cost of each investment
    values   : expected return of each investment
    capacity : total budget

    Returns
    -------
    total_value : total return achieved by the greedy selection
    selected    : 0-based indices of chosen investments (sorted)
    """
    n = len(weights)

    # Pair each item with its ratio and original index, then sort descending
    ratios = sorted(
        [(values[i] / weights[i], i) for i in range(n)],
        reverse=True,
    )

    total_value = 0
    remaining = capacity
    selected = []

    for ratio, i in ratios:
        if weights[i] <= remaining:
            selected.append(i)
            total_value += values[i]
            remaining -= weights[i]

    selected.sort()
    return total_value, selected
