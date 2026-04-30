# 0/1 Knapsack – Investment Portfolio Optimizer

A Python implementation of the classic **0/1 Knapsack problem** applied to
real-world **investment portfolio optimization**.

An investor has a fixed budget and must choose from 100 investment
opportunities (stocks, bonds, real estate, ETFs, crypto, commodities) to
**maximise total return**. Each investment is taken fully or not at all —
no fractional positions.

---

## Project Structure

```
knapsack_project/
├── main.py                  ← ONLY file you need to run
├── data/
│   └── generator.py         ← 100 random investment opportunities
├── algorithms/
│   ├── dp_2d.py             ← DP with full 2D table  O(nW) time & space
│   ├── dp_1d.py             ← Space-optimized DP     O(W) space
│   └── greedy.py            ← Greedy by value/weight ratio
├── analysis/
│   ├── comparator.py        ← DP vs Greedy comparison + explanation
│   ├── complexity.py        ← Complexity discussion
│   ├── real_world.py        ← Real-world applications
│   └── graphs.py            ← 10 matplotlib charts
└── utils/
    ├── reporter.py          ← Console printing helpers
    └── animator.py          ← Terminal animations
```

---

## Features

| Feature | Detail |
|---|---|
| **Algorithm** | 0/1 Knapsack via Dynamic Programming (2D table) |
| **Space optimization** | 1D rolling array — same result, O(W) space |
| **Greedy comparison** | Shows why greedy fails with concrete example |
| **Dataset** | 100 random investments, reproducible via seed |
| **Terminal animations** | Progress bar, spinner, typing effect |
| **10 charts** | Dark-themed matplotlib dashboard |

---

## Charts

1. DP vs Greedy — total return bar chart  
2. Selected investments scatter (DP vs Greedy overlay)  
3. All investments coloured by category  
4. Value/weight ratio histogram  
5. DP portfolio — cost vs return bars  
6. Cumulative return as items are added  
7. Budget utilisation pie chart  
8. Category breakdown of DP portfolio  
9. DP table heatmap  
10. Return/cost ratio colourmap scatter  

---

## Requirements

```
matplotlib
numpy
```

Install with:

```bash
pip install matplotlib numpy
```

---

## How to Run

```bash
cd knapsack_project
python main.py
```

The terminal output runs first (with animations), then the graph window opens.

---

## Complexity

| Algorithm | Time | Space |
|---|---|---|
| DP 2D table | O(n·W) | O(n·W) |
| DP 1D rolling | O(n·W) | O(W) |
| Greedy | O(n log n) | O(n) |

Where **n** = number of investments, **W** = budget.

---

## Real-World Applications

- **Capital budgeting** — allocate R&D budget across projects by NPV  
- **Portfolio construction** — select assets under a capital constraint  
- **Cargo loading** — maximise value within weight/volume limits  
- **Sprint planning** — pick tasks within developer-hour constraints  
- **Cloud resource allocation** — assign VMs to jobs under a cost cap  

---

## Why Greedy Fails

The greedy approach (pick highest return/cost ratio first) is **optimal for
fractional knapsack** but **not for 0/1 knapsack**:

> Taking a high-ratio investment may consume budget that could have been used
> by several lower-ratio investments whose **combined return is greater**.

Example with budget = $10k:

| Item | Cost | Return | Ratio |
|---|---|---|---|
| A | $6k | $8k | 1.33 ← greedy picks |
| B | $5k | $6k | 1.20 |
| C | $5k | $6k | 1.20 |

- **Greedy**: picks A → total **$8k**  
- **DP**: picks B + C → total **$12k** ✓
