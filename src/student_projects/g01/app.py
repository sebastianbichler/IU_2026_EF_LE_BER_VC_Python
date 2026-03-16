from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st

from foxexpress.controllers.route_controller import BenchmarkController, RouteController
from foxexpress.models.graph import GraphGenerationError
from foxexpress.models.locations import (
    POSTAMT_NODE_ID,
    get_location_name,
    get_location_options,
)
from foxexpress.views.benchmark_view import display_benchmark_results, display_route_result

st.set_page_config(page_title="FoxExpress", page_icon="🦊", layout="wide")

st.title("FoxExpress - Paketzustellung im Wald")
st.caption(
    "Der Fuchs bringt Pakete von seinem Postamt zu verschiedenen Tier-Heimatorten im Wald."
)

with st.sidebar:
    st.header("Lieferkonfiguration")
    node_count = st.slider("Anzahl Knoten", min_value=20, max_value=250, value=120, step=10)
    density = st.slider("Graph-Dichte", min_value=0.05, max_value=1.0, value=0.25, step=0.05)
    seed = st.number_input("Seed", min_value=1, max_value=99999, value=42, step=1)

    st.markdown("---")
    st.header("Start & Ziel")

    st.markdown("**Start:** Fuchs Postamt")

    target_options = get_location_options(node_count)
    target_index = min(1, len(target_options) - 1)
    target = st.selectbox(
        "Zielort auswählen:",
        options=range(len(target_options)),
        format_func=lambda i: target_options[i][1],
        index=target_index,
    )
    target_node = target_options[target][0]

    runs = st.slider("Benchmark-Wiederholungen", min_value=3, max_value=50, value=10, step=1)
    pypy_executable = st.text_input("PyPy ausführbare Datei", value="pypy3")
    run_button = st.button("Lieferung starten", type="primary")

st.markdown(
    """
### FoxExpress - Zustellung

Der freundliche Fuchs liefert Pakete vom **Fuchs Postamt** zu verschiedenen Zielorten im Wald.
Wähle oben einen Zielort aus und starte die Lieferung!
"""
)

if run_button:
    try:
        start_node = POSTAMT_NODE_ID
        target_node_id = target_node
        seed_val = int(seed)

        if start_node == target_node_id:
            st.error("Start und Ziel müssen unterschiedlich sein.")
            st.stop()

        st.info(f"Lieferung von **{get_location_name(start_node, seed_val)}** nach **{get_location_name(target_node_id, seed_val)}** wird berechnet...")

        py_graph, np_graph, route_cpython, route_numba = RouteController.generate_and_compute_routes(
            node_count=int(node_count),
            density=float(density),
            seed=seed_val,
            start=start_node,
            target=target_node_id,
        )

        RouteController.validate_routes(route_cpython, route_numba)

        display_route_result(route_cpython, route_numba, lambda n: get_location_name(n, seed_val))

        with st.spinner("Führe Multi-Environment-Benchmark aus ..."):
            cpython_result, numba_result, pypy_result = BenchmarkController.run_benchmark(
                py_graph=py_graph,
                np_graph=np_graph,
                start=start_node,
                target=target_node_id,
                runs=int(runs),
                pypy_executable=pypy_executable,
                node_count=int(node_count),
                density=float(density),
                seed=seed_val,
            )

        display_benchmark_results(cpython_result, numba_result, pypy_result)

    except FileNotFoundError:
        st.error(
            "PyPy wurde nicht gefunden. Prüfe den Pfad in der Seitenleiste oder installiere PyPy. "
            "Die genaue Einrichtung steht in der README.md."
        )
    except GraphGenerationError as exc:
        st.error(f"Ungültige Graph-Konfiguration: {exc}")
    except Exception as exc:
        st.exception(exc)
else:
    st.info("Waehle einen Zielort aus und klicke auf 'Lieferung starten'!")
