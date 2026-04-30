"""
algorithms/dp_2d.py
────────────────────
0/1 Knapsack solved with a full 2D Dynamic Programming table.

Recurrence
──────────
  dp[i][w] = 0                                          if i == 0 or w == 0
  dp[i][w] = dp[i-1][w]                                if weights[i-1] > w
  dp[i][w] = max(dp[i-1][w],
                 dp[i-1][w - weights[i-1]] + values[i-1])  otherwise

Time  : O(n * W)
Space : O(n * W)  ← full table kept for backtracking
"""


def knapsack_dp_2d(
    weights: list[int],
    values: list[int],
    capacity: int,
    row_callback=None,
) -> tuple[int, list[int]]:
    """
    Solve 0/1 knapsack using a 2D DP table.

    Parameters
    ----------
    weights       : cost of each investment
    values        : expected return of each investment
    capacity      : total budget
    row_callback  : optional callable(i, n) called after each row i is filled
                    (used by the progress bar in main.py)

    Returns
    -------
    max_return : best achievable total return
    selected   : 0-based indices of chosen investments
    """
    n = len(weights)

    # ── Build (n+1) × (capacity+1) table ──
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(capacity + 1):
            # Option A: skip item i
            dp[i][w] = dp[i - 1][w]
            # Option B: take item i (only if it fits in remaining budget)
            if w_i <= w:
                take = dp[i - 1][w - w_i] + v_i
                if take > dp[i][w]:
                    dp[i][w] = take

        # Notify caller that row i is complete (drives progress bar)
        if row_callback:
            row_callback(i, n)

    # ── Backtrack through the table to recover selected items ──
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:   # item i was included
            selected.append(i - 1)      # store 0-based index
            w -= weights[i - 1]

    selected.reverse()
    return dp[n][capacity], selected
