from __future__ import annotations

import json
import statistics
import subprocess
import time
from pathlib import Path
from typing import Callable, List

import numpy as np

from foxexpress.models.dijkstra import (
    dijkstra_cpython,
    dijkstra_numba,
    dijkstra_numba_core,
)
from foxexpress.models.data_types import BenchmarkResult


def _measure_callable(fn: Callable[[], object], runs: int) -> tuple[float, float]:
    durations_ms: List[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        fn()
        end = time.perf_counter()
        durations_ms.append((end - start) * 1000.0)
    mean_ms = statistics.fmean(durations_ms)
    std_ms = statistics.pstdev(durations_ms) if len(durations_ms) > 1 else 0.0
    return mean_ms, std_ms


def compute_route_cpython(py_graph: List[List[float]], start: int, target: int) -> "RouteResult":
    from foxexpress.models.data_types import RouteResult

    started = time.perf_counter()
    path, cost = dijkstra_cpython(py_graph, start, target)
    ended = time.perf_counter()
    return RouteResult("CPython", path, cost, (ended - started) * 1000.0)


def compute_route_numba(np_graph: np.ndarray, start: int, target: int) -> "RouteResult":
    from foxexpress.models.data_types import RouteResult

    dijkstra_numba_core(np_graph, start, target)
    started = time.perf_counter()
    path, cost = dijkstra_numba(np_graph, start, target)
    ended = time.perf_counter()
    return RouteResult("Numba", path, cost, (ended - started) * 1000.0)


def benchmark_cpython(
    py_graph: List[List[float]], start: int, target: int, runs: int
) -> BenchmarkResult:
    path, cost = dijkstra_cpython(py_graph, start, target)
    mean_ms, std_ms = _measure_callable(lambda: dijkstra_cpython(py_graph, start, target), runs)
    return BenchmarkResult("CPython", runs, mean_ms, std_ms, path, cost)


def benchmark_numba(np_graph: np.ndarray, start: int, target: int, runs: int) -> BenchmarkResult:
    dijkstra_numba_core(np_graph, start, target)
    path, cost = dijkstra_numba(np_graph, start, target)
    mean_ms, std_ms = _measure_callable(lambda: dijkstra_numba(np_graph, start, target), runs)
    return BenchmarkResult("Numba", runs, mean_ms, std_ms, path, cost)


def benchmark_pypy(
    pypy_executable: str,
    node_count: int,
    density: float,
    seed: int,
    start: int,
    target: int,
    runs: int,
) -> BenchmarkResult:
    script_path = Path(__file__).resolve().parent.parent.parent.parent / "pypy_benchmark.py"
    cmd = [
        pypy_executable,
        str(script_path),
        "--nodes",
        str(node_count),
        "--density",
        str(density),
        "--seed",
        str(seed),
        "--start",
        str(start),
        "--target",
        str(target),
        "--runs",
        str(runs),
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True)

    if completed.returncode != 0:
        raise RuntimeError(
            "PyPy-Benchmark fehlgeschlagen.\n\n"
            f"Command: {' '.join(cmd)}\n\n"
            f"STDOUT:\n{completed.stdout}\n\n"
            f"STDERR:\n{completed.stderr}"
        )

    payload = json.loads(completed.stdout)
    return BenchmarkResult(
        strategy_name="PyPy",
        runs=int(payload["runs"]),
        mean_ms=float(payload["mean_ms"]),
        std_ms=float(payload["std_ms"]),
        path=[int(node) for node in payload["path"]],
        cost=float(payload["cost"]),
    )


def validate_consistent_results(results: List[BenchmarkResult]) -> None:
    baseline = results[0]
    for result in results[1:]:
        if result.path != baseline.path or abs(result.cost - baseline.cost) > 1e-9:
            raise AssertionError(
                "Routing results differ between environments. "
                f"Baseline={baseline.strategy_name}, compared={result.strategy_name}"
            )
