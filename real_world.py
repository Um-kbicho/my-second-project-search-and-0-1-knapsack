"""
analysis/real_world.py
───────────────────────
Describes real-world applications of the 0/1 knapsack problem.
"""

from utils.reporter import section


def print_real_world() -> None:
    section("Real-World Applications")
    print("""
  Investment & Finance
  ─────────────────────
  • Capital budgeting  : a firm allocates a fixed R&D budget across
    projects, each with a cost and projected NPV.
  • Portfolio construction : select assets under a capital constraint
    to maximise expected return (when fractional shares are unavailable).
  • Venture capital : choose which startups to fund given a fund size.

  Operations & Logistics
  ───────────────────────
  • Cargo loading : pack a container/truck to maximise value within
    weight/volume limits.
  • Cloud resource allocation : assign VM instances to jobs under a
    cost cap to maximise throughput.
  • Sprint planning : pick tasks to complete in a sprint given
    developer-hour constraints.

  Other Domains
  ──────────────
  • Cryptography (subset-sum variant)
  • Bioinformatics (gene/feature selection)
  • Cutting stock problems in manufacturing
  • Ad selection under a display-time budget
""")
