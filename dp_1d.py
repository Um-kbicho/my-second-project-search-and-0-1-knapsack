"""
algorithms/dp_1d.py
────────────────────
0/1 Knapsack solved with a space-optimized 1D rolling array.

Key insight
───────────
The 2D recurrence only ever reads row (i-1) to fill row i.
We can therefore keep a single array and update it RIGHT-TO-LEFT:

    for w in range(W, weight_i - 1, -1):
        dp[w] = max(dp[w], dp[w - weight_i] + value_i)

Right-to-left traversal ensures dp[w - weight_i] still holds the
value from the PREVIOUS item's pass, so each item is counted at
most once (unlike unbounded knapsack which goes left-to-right).

Time  : O(n * W)   — identical to 2D version
Space : O(W)       — single array instead of n×W table

Trade-off: backtracking is not possible without the full table,
so this variant returns only the maximum value (no item list).
"""


def knapsack_dp_1d(
    weights: list[int],
    values: list[int],
    capacity: int,
) -> int:
    """
    Solve 0/1 knapsack using a 1D rolling array (space-optimized).

    Parameters
    ----------
    weights  : cost of each investment
    values   : expected return of each investment
    capacity : total budget

    Returns
    -------
    max_return : best achievable total return (int)
    """
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        w_i, v_i = weights[i], values[i]
        # Traverse right-to-left to avoid using item i more than once
        for w in range(capacity, w_i - 1, -1):
            candidate = dp[w - w_i] + v_i
            if candidate > dp[w]:
                dp[w] = candidate

    return dp[capacity]
