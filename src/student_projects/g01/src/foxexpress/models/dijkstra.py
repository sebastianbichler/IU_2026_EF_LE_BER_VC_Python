from __future__ import annotations

from typing import List, Tuple

import numpy as np
from numba import jit


INF = float("inf")


class RouteNotFoundError(RuntimeError):
    """Raised when no route exists between the chosen nodes."""


def dijkstra_cpython(graph: List[List[float]], start: int, target: int) -> Tuple[List[int], float]:
    n = len(graph)
    if not (0 <= start < n and 0 <= target < n):
        raise ValueError("start and target must be valid node indices")

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
        raise RouteNotFoundError(f"No route found from {start} to {target}")

    path = []
    node = target
    while node != -1:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path, dist[target]


@jit(nopython=True)
def dijkstra_numba_core(graph: np.ndarray, start: int, target: int) -> tuple[np.ndarray, np.ndarray, float]:
    n = graph.shape[0]
    dist = np.full(n, np.inf, dtype=np.float64)
    prev = np.full(n, -1, dtype=np.int64)
    visited = np.zeros(n, dtype=np.bool_)
    dist[start] = 0.0

    for _ in range(n):
        current = -1
        current_dist = np.inf
        for node in range(n):
            if not visited[node] and dist[node] < current_dist:
                current = node
                current_dist = dist[node]

        if current == -1:
            break
        if current == target:
            break

        visited[current] = True
        for neighbor in range(n):
            weight = graph[current, neighbor]
            if visited[neighbor] or neighbor == current or np.isinf(weight):
                continue
            new_dist = dist[current] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current

    return dist, prev, dist[target]


def dijkstra_numba(graph: np.ndarray, start: int, target: int) -> Tuple[List[int], float]:
    if graph.ndim != 2 or graph.shape[0] != graph.shape[1]:
        raise ValueError("graph must be a square adjacency matrix")
    n = graph.shape[0]
    if not (0 <= start < n and 0 <= target < n):
        raise ValueError("start and target must be valid node indices")

    _, prev, target_dist = dijkstra_numba_core(graph, start, target)
    if np.isinf(target_dist):
        raise RouteNotFoundError(f"No route found from {start} to {target}")

    path: List[int] = []
    node = target
    while node != -1:
        path.append(int(node))
        node = int(prev[node])
    path.reverse()
    return path, float(target_dist)
