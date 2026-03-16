from __future__ import annotations

import argparse
import json
import random
import statistics
import time
from typing import List, Tuple

INF = float("inf")


def generate_dense_graph(
    node_count: int,
    density: float,
    seed: int,
    min_weight: int = 1,
    max_weight: int = 20,
) -> List[List[float]]:
    if node_count < 2:
        raise ValueError("node_count must be at least 2")
    if not 0 < density <= 1:
        raise ValueError("density must be within (0, 1]")
    if min_weight <= 0 or max_weight < min_weight:
        raise ValueError("invalid weight range")

    rng = random.Random(seed)
    matrix: List[List[float]] = [[INF for _ in range(node_count)] for _ in range(node_count)]

    for i in range(node_count):
        matrix[i][i] = 0.0

    # Verbindung garantieren
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

    return matrix


def dijkstra_pure_python(graph: List[List[float]], start: int, target: int) -> Tuple[List[int], float]:
    n = len(graph)
    dist = [INF] * n
    prev = [-1] * n
    visited = [False] * n
    dist[start] = 0.0

    for _ in range(n):
        current = -1
        current_dist = INF

        for node in range(n):
            if not visited[node] and dist[node] < current_dist:
                current = node
                current_dist = dist[node]

        if current == -1:
            break
        if current == target:
            break

        visited[current] = True
        row = graph[current]

        for neighbor in range(n):
            weight = row[neighbor]
            if visited[neighbor] or weight == INF or neighbor == current:
                continue

            new_dist = dist[current] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    if dist[target] == INF:
        raise RuntimeError("No route found")

    path: List[int] = []
    node = target
    while node != -1:
        path.append(node)
        node = prev[node]

    path.reverse()
    return path, dist[target]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark Dijkstra under PyPy")
    parser.add_argument("--nodes", type=int, required=True)
    parser.add_argument("--density", type=float, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument("--runs", type=int, required=True)
    args = parser.parse_args()

    py_graph = generate_dense_graph(args.nodes, args.density, args.seed)

    # Warmup für PyPy JIT
    for _ in range(5):
        dijkstra_pure_python(py_graph, args.start, args.target)

    durations_ms = []
    path, cost = dijkstra_pure_python(py_graph, args.start, args.target)

    for _ in range(args.runs):
        started = time.perf_counter()
        dijkstra_pure_python(py_graph, args.start, args.target)
        ended = time.perf_counter()
        durations_ms.append((ended - started) * 1000.0)

    payload = {
        "runs": args.runs,
        "mean_ms": statistics.fmean(durations_ms),
        "std_ms": statistics.pstdev(durations_ms) if len(durations_ms) > 1 else 0.0,
        "path": path,
        "cost": cost,
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    main()