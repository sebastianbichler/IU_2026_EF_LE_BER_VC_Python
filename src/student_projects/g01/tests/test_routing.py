from __future__ import annotations

import pytest
from foxexpress.models.dijkstra import RouteNotFoundError, dijkstra_cpython, dijkstra_numba
from foxexpress.models.graph import GraphGenerationError, generate_dense_graph
from foxexpress.models.locations import (
    POSTAMT_NODE_ID,
    get_location,
    get_location_name,
    get_location_options,
)


class TestDijkstra:
    def test_small_graph_shortest_path(self) -> None:
        inf = float("inf")
        graph = [
            [0.0, 2.0, 5.0, inf],
            [2.0, 0.0, 1.0, 4.0],
            [5.0, 1.0, 0.0, 1.0],
            [inf, 4.0, 1.0, 0.0],
        ]
        path, cost = dijkstra_cpython(graph, 0, 3)
        assert path == [0, 1, 2, 3]
        assert cost == 4.0

    def test_direct_path(self) -> None:
        graph = [
            [0.0, 5.0],
            [5.0, 0.0],
        ]
        path, cost = dijkstra_cpython(graph, 0, 1)
        assert path == [0, 1]
        assert cost == 5.0

    def test_same_start_target(self) -> None:
        graph = [[0.0, 5.0], [5.0, 0.0]]
        path, cost = dijkstra_cpython(graph, 0, 0)
        assert path == [0]
        assert cost == 0.0

    def test_invalid_start_node(self) -> None:
        graph = [[0.0, 5.0], [5.0, 0.0]]
        with pytest.raises(ValueError):
            dijkstra_cpython(graph, -1, 1)

    def test_invalid_target_node(self) -> None:
        graph = [[0.0, 5.0], [5.0, 0.0]]
        with pytest.raises(ValueError):
            dijkstra_cpython(graph, 0, 5)

    def test_no_route_exists(self) -> None:
        inf = float("inf")
        graph = [
            [0.0, inf, inf],
            [inf, 0.0, inf],
            [inf, inf, 0.0],
        ]
        with pytest.raises(RouteNotFoundError):
            dijkstra_cpython(graph, 0, 2)


class TestDijkstraNumba:
    def test_numba_matches_cpython(self) -> None:
        py_graph, np_graph = generate_dense_graph(node_count=25, density=0.3, seed=42)
        py_path, py_cost = dijkstra_cpython(py_graph, 0, 24)
        nb_path, nb_cost = dijkstra_numba(np_graph, 0, 24)
        assert py_path == nb_path
        assert py_cost == nb_cost

    def test_numba_invalid_graph(self) -> None:
        import numpy as np
        graph = np.zeros((2, 2, 2))
        with pytest.raises(ValueError):
            dijkstra_numba(graph, 0, 1)


class TestGraphGeneration:
    def test_generate_dense_graph(self) -> None:
        py_graph, np_graph = generate_dense_graph(node_count=10, density=0.5, seed=42)
        assert len(py_graph) == 10
        assert len(np_graph) == 10
        assert py_graph[0][0] == 0.0

    def test_invalid_node_count(self) -> None:
        with pytest.raises(GraphGenerationError):
            generate_dense_graph(node_count=1, density=0.5, seed=42)

    def test_invalid_density_zero(self) -> None:
        with pytest.raises(GraphGenerationError):
            generate_dense_graph(node_count=10, density=0.0, seed=42)

    def test_invalid_density_negative(self) -> None:
        with pytest.raises(GraphGenerationError):
            generate_dense_graph(node_count=10, density=-0.5, seed=42)

    def test_invalid_weight_range(self) -> None:
        with pytest.raises(GraphGenerationError):
            generate_dense_graph(node_count=10, density=0.5, seed=42, min_weight=-1)

    def test_graph_has_path_between_all_nodes(self) -> None:
        py_graph, _ = generate_dense_graph(node_count=20, density=0.5, seed=123)
        for i in range(20):
            for j in range(20):
                if i != j:
                    path, cost = dijkstra_cpython(py_graph, i, j)
                    assert cost < float("inf")

    def test_deterministic_with_seed(self) -> None:
        g1, _ = generate_dense_graph(node_count=10, density=0.5, seed=99)
        g2, _ = generate_dense_graph(node_count=10, density=0.5, seed=99)
        assert g1 == g2


class TestLocations:
    def test_postamt_node_id(self) -> None:
        assert POSTAMT_NODE_ID == 0

    def test_get_location_name_fixed(self) -> None:
        name = get_location_name(0, seed=42)
        assert name == "Fuchs Postamt"

    def test_get_location_name_biberdamm(self) -> None:
        name = get_location_name(1, seed=42)
        assert name == "Biberdamm"

    def test_get_location_name_generated(self) -> None:
        name = get_location_name(100, seed=42)
        assert name is not None
        assert len(name) > 0

    def test_get_location(self) -> None:
        loc = get_location(0, seed=42)
        assert loc.node_id == 0
        assert loc.name == "Fuchs Postamt"
        assert loc.animal_type == "Fuchs"

    def test_get_location_options(self) -> None:
        options = get_location_options(max_nodes=25)
        assert len(options) == 24
        assert options[0][0] == 1

    def test_location_deterministic(self) -> None:
        loc1 = get_location(50, seed=42)
        loc2 = get_location(50, seed=42)
        assert loc1.name == loc2.name
