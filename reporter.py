"""
utils/reporter.py
──────────────────
All console printing / display helpers.
Keeps I/O logic completely separate from algorithm logic.
"""

WIDTH = 65


def section(title: str) -> None:
    """Print a bold section header."""
    print("\n" + "=" * WIDTH)
    print(f"  {title}")
    print("=" * WIDTH)


def divider() -> None:
    print("─" * WIDTH)


def print_dataset_summary(
    n: int,
    budget: int,
    weights: list[int],
    values: list[int],
) -> None:
    section("Dataset Summary")
    print(f"""
  Investments  : {n}
  Budget       : ${budget}k
  Cost  range  : ${min(weights)}k – ${max(weights)}k per investment
  Return range : ${min(values)}k  – ${max(values)}k expected return
""")


def print_selected_items(
    indices: list[int],
    names: list[str],
    weights: list[int],
    values: list[int],
    capacity: int,
    max_return: int,
    label: str,
) -> None:
    """Print a formatted table of selected investments."""
    total_cost = sum(weights[i] for i in indices)

    divider()
    print(f"  {label}")
    divider()
    print(f"  {'#':<5} {'Name':<20} {'Cost ($k)':>10} {'Return ($k)':>12}  {'Ratio':>6}")
    print(f"  {'─'*5} {'─'*20} {'─'*10} {'─'*12}  {'─'*6}")

    for rank, i in enumerate(indices, 1):
        ratio = values[i] / weights[i]
        print(f"  {rank:<5} {names[i]:<20} {weights[i]:>10} {values[i]:>12}  {ratio:>6.2f}")

    divider()
    print(f"  Items selected : {len(indices)}")
    print(f"  Total cost     : ${total_cost}k  (budget: ${capacity}k)")
    print(f"  Total return   : ${max_return}k")
    divider()


def print_timing(label: str, ms: float) -> None:
    print(f"\n  {label} runtime : {ms:.2f} ms")


def print_space_saving(n: int, capacity: int) -> None:
    cells_2d = n * (capacity + 1)
    cells_1d = capacity + 1
    print(f"  Space saved : {cells_2d:,} cells (2D) → {cells_1d:,} cells (1D)")
