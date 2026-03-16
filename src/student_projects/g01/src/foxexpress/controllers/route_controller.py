from __future__ import annotations

from typing import List, Tuple

import numpy as np

from foxexpress.models.data_types import BenchmarkResult, RouteResult
from foxexpress.models.benchmark import (
    benchmark_cpython,
    benchmark_numba,
    benchmark_pypy,
    compute_route_cpython,
    compute_route_numba,
    validate_consistent_results,
)
from foxexpress.models.graph import generate_dense_graph


class RouteController:
    @staticmethod
    def generate_and_compute_routes(
        node_count: int,
        density: float,
        seed: int,
        start: int,
        target: int,
    ) -> Tuple[List[List[float]], np.ndarray, RouteResult, RouteResult]:
        py_graph, np_graph = generate_dense_graph(node_count, density, seed)
        route_cpython = compute_route_cpython(py_graph, start, target)
        route_numba = compute_route_numba(np_graph, start, target)
        return py_graph, np_graph, route_cpython, route_numba

    @staticmethod
    def validate_routes(route_cpython: RouteResult, route_numba: RouteResult) -> None:
        if route_cpython.path != route_numba.path or abs(route_cpython.cost - route_numba.cost) > 1e-9:
            raise ValueError("CPython- und Numba-Ergebnis stimmen nicht überein.")


class BenchmarkController:
    @staticmethod
    def run_benchmark(
        py_graph: List[List[float]],
        np_graph: np.ndarray,
        start: int,
        target: int,
        runs: int,
        pypy_executable: str,
        node_count: int,
        density: float,
        seed: int,
    ) -> Tuple[BenchmarkResult, BenchmarkResult, BenchmarkResult]:
        cpython_result = benchmark_cpython(py_graph, start, target, runs)
        numba_result = benchmark_numba(np_graph, start, target, runs)
        pypy_result = benchmark_pypy(
            pypy_executable=pypy_executable,
            node_count=node_count,
            density=density,
            seed=seed,
            start=start,
            target=target,
            runs=runs,
        )
        validate_consistent_results([cpython_result, numba_result, pypy_result])
        return cpython_result, numba_result, pypy_result
