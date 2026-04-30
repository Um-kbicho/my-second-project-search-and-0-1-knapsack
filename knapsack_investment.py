"""
0/1 Knapsack Problem - Investment Portfolio Optimization
=========================================================
Real-world context: An investor has a fixed budget and must choose from a set of
investment opportunities (stocks, bonds, real estate) to maximize total return.
Each investment is either taken fully or not at all (no fractional investments).

Complexity: O(n * W) time, O(n * W) space for 2D DP table
             O(W) space with 1D rolling array optimization
"""

import random
import time


# ─────────────────────────────────────────────
# 1. Dataset Generation
# ─────────────────────────────────────────────

def generate_investments(n: int = 100, seed: int = 42) -> tuple[list, list, list]:
    """
    Generate n random investment opportunities.

    Returns:
        names   – list of investment labels
        weights – investment amounts (cost in $1000s)
        values  – expected returns (profit in $1000s)
    """
    random.seed(seed)

    categories = ["Stock", "Bond", "RealEstate", "ETF", "Crypto", "Commodity"]
    names, weights, values = [], [], []

    for i in range(n):
        category = random.choice(categories)
        names.append(f"{category}_{i+1:03d}")
        weights.append(random.randint(1, 50))   # cost:   $1k – $50k
        values.append(random.randint(1, 100))   # return: $1k – $100k

    return names, weights, values


# ─────────────────────────────────────────────
# 2. Dynamic Programming – 2D Table (O(nW) time, O(nW) space)
# ─────────────────────────────────────────────

def knapsack_dp_2d(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
    """
    Solve 0/1 knapsack with a full 2D DP table.

    dp[i][w] = maximum return using the first i items with budget w.

    Recurrence:
        dp[i][w] = dp[i-1][w]                              if weights[i-1] > w
        dp[i][w] = max(dp[i-1][w],
                       dp[i-1][w - weights[i-1]] + values[i-1])  otherwise

    Returns:
        max_return  – best achievable total return
        selected    – 0-based indices of chosen investments
    """
    n = len(weights)

    # Build (n+1) x (capacity+1) table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(capacity + 1):
            # Option 1: skip item i
            dp[i][w] = dp[i - 1][w]
            # Option 2: take item i (only if it fits)
            if w_i <= w:
                take = dp[i - 1][w - w_i] + v_i
                if take > dp[i][w]:
                    dp[i][w] = take

    # ── Backtrack to find selected items ──
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:   # item i was taken
            selected.append(i - 1)      # convert to 0-based index
            w -= weights[i - 1]

    selected.reverse()
    return dp[n][capacity], selected


# ─────────────────────────────────────────────
# 3. Space-Optimized DP – 1D Rolling Array (O(W) space)
# ─────────────────────────────────────────────

def knapsack_dp_1d(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Same recurrence as 2D but uses a single array updated in-place.

    Key insight: iterate w from capacity → 0 (right to left) so each
    dp[w] still represents the state BEFORE item i was considered,
    preventing an item from being counted twice.

    Space: O(W)  |  Time: O(n * W)  — identical to 2D version.

    Note: backtracking is not possible without storing the full table,
    so this variant returns only the maximum value.
    """
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        w_i, v_i = weights[i], values[i]
        for w in range(capacity, w_i - 1, -1):   # right-to-left prevents reuse
            if dp[w - w_i] + v_i > dp[w]:
                dp[w] = dp[w - w_i] + v_i

    return dp[capacity]


# ─────────────────────────────────────────────
# 4. Greedy Approach (value/weight ratio)
# ─────────────────────────────────────────────

def knapsack_greedy(weights: list[int], values: list[int], capacity: int) -> tuple[int, list[int]]:
    """
    Greedy heuristic: sort by value-to-weight ratio (highest first),
    then greedily pick items that still fit.

    This is OPTIMAL for the fractional knapsack but NOT for 0/1 knapsack.
    It can miss the true optimum because taking a high-ratio item may
    block several lower-ratio items whose combined value is greater.
    """
    n = len(weights)
    ratios = [(values[i] / weights[i], i) for i in range(n)]
    ratios.sort(reverse=True)   # descending ratio

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


# ─────────────────────────────────────────────
# 5. Reporting Helpers
# ─────────────────────────────────────────────

def print_section(title: str) -> None:
    width = 65
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_selected_items(
    indices: list[int],
    names: list[str],
    weights: list[int],
    values: list[int],
    capacity: int,
    max_return: int,
    label: str,
) -> None:
    total_cost = sum(weights[i] for i in indices)
    print(f"\n{'─'*65}")
    print(f"  {label}")
    print(f"{'─'*65}")
    print(f"  {'#':<5} {'Name':<20} {'Cost ($k)':>10} {'Return ($k)':>12}  {'Ratio':>6}")
    print(f"  {'─'*5} {'─'*20} {'─'*10} {'─'*12}  {'─'*6}")
    for rank, i in enumerate(indices, 1):
        ratio = values[i] / weights[i]
        print(f"  {rank:<5} {names[i]:<20} {weights[i]:>10} {values[i]:>12}  {ratio:>6.2f}")
    print(f"{'─'*65}")
    print(f"  Items selected : {len(indices)}")
    print(f"  Total cost     : ${total_cost}k  (budget: ${capacity}k)")
    print(f"  Total return   : ${max_return}k")
    print(f"{'─'*65}")


def explain_greedy_failure(
    names, weights, values, capacity,
    dp_return, dp_selected,
    greedy_return, greedy_selected,
) -> None:
    print_section("Why Greedy Fails for 0/1 Knapsack")

    gap = dp_return - greedy_return
    print(f"""
  Greedy strategy: pick items with the highest return/cost ratio first.
  This works perfectly for the FRACTIONAL knapsack (you can take parts
  of an item to fill the remaining budget exactly).

  For 0/1 knapsack it fails because:
  ┌─────────────────────────────────────────────────────────────┐
  │  Taking a high-ratio item may consume budget that could     │
  │  have been used by several lower-ratio items whose          │
  │  COMBINED return exceeds the single high-ratio item.        │
  └─────────────────────────────────────────────────────────────┘

  On this dataset (n=100, budget=${capacity}k):
    DP optimal return  : ${dp_return}k
    Greedy return      : ${greedy_return}k
    Suboptimality gap  : ${gap}k  ({gap/dp_return*100:.1f}% below optimal)

  Concrete example of greedy's blind spot
  ─────────────────────────────────────────
  Suppose budget = $10k and we have three items:
    A: cost=$6k, return=$8k  → ratio 1.33  ← greedy picks this first
    B: cost=$5k, return=$6k  → ratio 1.20
    C: cost=$5k, return=$6k  → ratio 1.20

  Greedy picks A ($6k used), then cannot fit B or C → total = $8k.
  DP picks B + C ($10k used)                        → total = $12k  ✓

  The greedy algorithm has no look-ahead; it commits to locally
  optimal choices that can foreclose globally better combinations.
""")


# ─────────────────────────────────────────────
# 6. Complexity Discussion
# ─────────────────────────────────────────────

def print_complexity(n: int, capacity: int) -> None:
    print_section("Complexity Analysis")
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
    Memory (2D)     : ~{cells * 4 / 1024:.1f} KB  (4 bytes per int)
    Memory (1D)     : ~{capacity * 4 / 1024:.1f} KB  (4 bytes per int)

  Space Optimization Detail
  ──────────────────────────
  The 2D recurrence only ever looks at row i-1 to compute row i.
  We can therefore keep a single 1D array and update it right-to-left:

      for w in range(W, weight_i - 1, -1):
          dp[w] = max(dp[w], dp[w - weight_i] + value_i)

  Right-to-left traversal ensures dp[w - weight_i] still holds the
  value from the PREVIOUS item's row, preventing an item from being
  selected more than once (which would turn it into an unbounded
  knapsack).  Backtracking requires the full 2D table.

  Pseudo-polynomial note
  ───────────────────────
  O(n·W) is pseudo-polynomial: W is the numeric value of the budget,
  not its bit-length.  For very large W the problem is NP-hard in the
  strong sense, and approximation schemes (FPTAS) are used in practice.
""")


# ─────────────────────────────────────────────
# 7. Real-World Connection
# ─────────────────────────────────────────────

def print_real_world() -> None:
    print_section("Real-World Applications")
    print("""
  Investment & Finance
  ─────────────────────
  • Capital budgeting: a firm allocates a fixed R&D budget across
    projects, each with a cost and projected NPV.
  • Portfolio construction: select assets under a capital constraint
    to maximise expected return (when fractional shares are unavailable).
  • Venture capital: choose which startups to fund given a fund size.

  Operations & Logistics
  ───────────────────────
  • Cargo loading: pack a container/truck to maximise value within
    weight/volume limits.
  • Cloud resource allocation: assign VM instances to jobs under a
    cost cap to maximise throughput.
  • Project scheduling: pick tasks to complete in a sprint given
    developer-hour constraints.

  Other Domains
  ──────────────
  • Cryptography (subset-sum variant), bioinformatics (gene selection),
    cutting stock problems in manufacturing.
""")


# ─────────────────────────────────────────────
# 8. Main Driver
# ─────────────────────────────────────────────

def main() -> None:
    N = 100          # number of investment opportunities
    BUDGET = 200     # total budget in $1000s

    print_section("0/1 Knapsack – Investment Portfolio Optimizer")
    print(f"\n  Generating {N} random investment opportunities …")
    names, weights, values = generate_investments(N)

    print(f"  Budget : ${BUDGET}k")
    print(f"  Items  : {N}")
    print(f"  Weight range : ${min(weights)}k – ${max(weights)}k per investment")
    print(f"  Value  range : ${min(values)}k – ${max(values)}k expected return")

    # ── DP 2D ──
    print_section("Dynamic Programming Solution (2D Table)")
    t0 = time.perf_counter()
    dp_return, dp_selected = knapsack_dp_2d(weights, values, BUDGET)
    dp_time = (time.perf_counter() - t0) * 1000

    print_selected_items(dp_selected, names, weights, values, BUDGET, dp_return,
                         "Optimal Portfolio (DP 2D)")
    print(f"\n  DP 2D runtime : {dp_time:.2f} ms")

    # ── DP 1D (space-optimized) ──
    print_section("Space-Optimized DP (1D Rolling Array)")
    t0 = time.perf_counter()
    dp1d_return = knapsack_dp_1d(weights, values, BUDGET)
    dp1d_time = (time.perf_counter() - t0) * 1000

    print(f"\n  Maximum return (1D DP) : ${dp1d_return}k")
    print(f"  Matches 2D result      : {dp1d_return == dp_return}")
    print(f"  1D DP runtime          : {dp1d_time:.2f} ms")
    print(f"  Space saved            : {N * (BUDGET + 1)} cells → {BUDGET + 1} cells")

    # ── Greedy ──
    print_section("Greedy Approach (Value/Weight Ratio)")
    t0 = time.perf_counter()
    greedy_return, greedy_selected = knapsack_greedy(weights, values, BUDGET)
    greedy_time = (time.perf_counter() - t0) * 1000

    print_selected_items(greedy_selected, names, weights, values, BUDGET, greedy_return,
                         "Greedy Portfolio (ratio-sorted)")
    print(f"\n  Greedy runtime : {greedy_time:.2f} ms")

    # ── Comparison ──
    print_section("DP vs Greedy Comparison")
    print(f"""
  ┌──────────────────────────────────────────────────────────────┐
  │  Method          Return ($k)   Items   Runtime               │
  ├──────────────────────────────────────────────────────────────┤
  │  DP (optimal)    {dp_return:<13} {len(dp_selected):<7} {dp_time:.2f} ms              │
  │  Greedy          {greedy_return:<13} {len(greedy_selected):<7} {greedy_time:.2f} ms              │
  └──────────────────────────────────────────────────────────────┘
  Greedy is {dp_return - greedy_return}k ({(dp_return - greedy_return)/dp_return*100:.1f}%) below the true optimum.
""")

    # ── Explanations ──
    explain_greedy_failure(names, weights, values, BUDGET,
                           dp_return, dp_selected,
                           greedy_return, greedy_selected)
    print_complexity(N, BUDGET)
    print_real_world()

    print("=" * 65)
    print("  Done.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
