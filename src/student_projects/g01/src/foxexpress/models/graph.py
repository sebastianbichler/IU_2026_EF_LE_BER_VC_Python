from __future__ import annotations

import random
from typing import List, Tuple

import numpy as np


class GraphGenerationError(ValueError):
    """Raised when the graph configuration is invalid."""


INF = float("inf")


def generate_dense_graph(
    node_count: int,
    density: float,
    seed: int,
    min_weight: int = 1,
    max_weight: int = 20,
) -> Tuple[List[List[float]], np.ndarray]:
    if node_count < 2:
        raise GraphGenerationError("node_count must be at least 2")
    if not 0 < density <= 1:
        raise GraphGenerationError("density must be within (0, 1]")
    if min_weight <= 0 or max_weight < min_weight:
        raise GraphGenerationError("invalid weight range")

    rng = random.Random(seed)
    matrix: List[List[float]] = [[INF for _ in range(node_count)] for _ in range(node_count)]
    for i in range(node_count):
        matrix[i][i] = 0.0

    edges = set()
    for i in range(node_count - 1):
        weight = float(rng.randint(min_weight, max_weight))
        matrix[i][i + 1] = weight
        matrix[i + 1][i] = weight
        edges.add((i, i + 1))

    max_edges = node_count * (node_count - 1) // 2
    target_edges = max(node_count - 1, int(max_edges * density))

    while len(edges) < target_edges:
        a = rng.randrange(0, node_count)
        b = rng.randrange(0, node_count)
        if a == b:
            continue
        edge = (a, b) if a < b else (b, a)
        if edge in edges:
            continue
        weight = float(rng.randint(min_weight, max_weight))
        matrix[edge[0]][edge[1]] = weight
        matrix[edge[1]][edge[0]] = weight
        edges.add(edge)

    np_matrix = np.array(matrix, dtype=np.float64)
    return matrix, np_matrix
