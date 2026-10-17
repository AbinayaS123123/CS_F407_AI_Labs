"""Compare heuristic choices for A*."""
from astar import (
    WAREHOUSE, astar, manhattan, zero_heuristic, euclidean, doubled_manhattan
)


def main() -> None:
    experiments = [
        ("Manhattan", manhattan),
        ("Zero (h=0)", zero_heuristic),
        ("Euclidean", euclidean),
        ("Doubled Manhattan (2h)", doubled_manhattan),
    ]
    print(f"{'Heuristic':<30} {'Found':<8} {'Path length':<13} {'Expanded':<10}")
    print("-" * 65)
    for name, heuristic in experiments:
        result = astar(WAREHOUSE, heuristic)
        print(
            f"{name:<30} {str(result['found']):<8} "
            f"{str(result['path_length']):<13} {result['states_expanded']:<10}"
        )


if __name__ == "__main__":
    main()
