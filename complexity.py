"""
analysis/complexity.py
───────────────────────
Prints a detailed complexity analysis of all three approaches
and discusses the space-optimization from 2D → 1D DP.
"""

from utils.reporter import section


def print_complexity(n: int, capacity: int) -> None:
    section("Complexity Analysis")
    cells = n * capacity

    print(f"""
  ┌──────────────────────────────────────────────────────────────┐
  │  Algorithm          Time          Space                      │
  ├──────────────────────────────────────────────────────────────┤
  │  DP 2D table        O(n·W)        O(n·W)  ← full table       │
  │  DP 1D rolling      O(n·W)        O(W)    ← space-optimized  │
  │  Greedy             O(n log n)    O(n)    ← not optimal      │
  └──────────────────────────────────────────────────────────────┘

  With n={n} items and budget W={capacity}:
    DP table cells  : {n} × {capacity} = {cells:,}
    Memory (2D)     : ~{cells * 4 / 1024:.1f} KB  (4 bytes / int)
    Memory (1D)     : ~{capacity * 4 / 1024:.1f} KB  (4 bytes / int)

  ── Space Optimization: 2D → 1D ──────────────────────────────
  The 2D recurrence only reads row (i-1) to compute row i.
  We keep a single 1D array and update it RIGHT-TO-LEFT:

      for w in range(W, weight_i - 1, -1):
          dp[w] = max(dp[w], dp[w - weight_i] + value_i)

  Right-to-left traversal ensures dp[w - weight_i] still holds
  the value from the PREVIOUS item's pass, so each investment is
  selected at most once.  (Left-to-right would allow an item to
  be reused, turning it into an unbounded knapsack.)

  Trade-off: the 1D version cannot backtrack to recover which
  items were selected — you need the full 2D table for that.

  ── Pseudo-polynomial note ────────────────────────────────────
  O(n·W) is pseudo-polynomial: W is the numeric value of the
  budget, not its bit-length.  For very large W the problem is
  NP-hard in the strong sense, and approximation schemes (FPTAS)
  are used in practice (e.g., rounding values to reduce W).
""")
