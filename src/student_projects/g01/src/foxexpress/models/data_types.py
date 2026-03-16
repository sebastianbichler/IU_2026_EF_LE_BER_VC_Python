from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class RouteResult:
    strategy_name: str
    path: List[int]
    cost: float
    time_ms: float


@dataclass(slots=True)
class BenchmarkResult:
    strategy_name: str
    runs: int
    mean_ms: float
    std_ms: float
    path: List[int]
    cost: float
