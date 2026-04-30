"""
data/generator.py
─────────────────
Generates a random dataset of investment opportunities.

Each investment has:
  - a name     (e.g. "Stock_042")
  - a weight   (cost in $1 000s, range 1–50)
  - a value    (expected return in $1 000s, range 1–100)
"""

import random


def generate_investments(n: int = 100, seed: int = 42) -> tuple[list, list, list]:
    """
    Generate `n` random investment opportunities.

    Parameters
    ----------
    n    : number of investments (default 100)
    seed : random seed for reproducibility

    Returns
    -------
    names   : list[str]  – investment labels
    weights : list[int]  – cost of each investment ($k)
    values  : list[int]  – expected return of each investment ($k)
    """
    random.seed(seed)

    categories = ["Stock", "Bond", "RealEstate", "ETF", "Crypto", "Commodity"]
    names, weights, values = [], [], []

    for i in range(n):
        category = random.choice(categories)
        names.append(f"{category}_{i + 1:03d}")
        weights.append(random.randint(1, 50))    # cost:   $1k – $50k
        values.append(random.randint(1, 100))    # return: $1k – $100k

    return names, weights, values
