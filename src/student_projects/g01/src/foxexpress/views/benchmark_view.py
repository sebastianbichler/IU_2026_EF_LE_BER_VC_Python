from __future__ import annotations

from typing import Callable

from foxexpress.models.data_types import BenchmarkResult, RouteResult


def display_route_result(
    route_cpython: RouteResult,
    route_numba: RouteResult,
    location_name_fn: Callable[[int], str] | None = None,
) -> None:
    import streamlit as st

    if location_name_fn is None:
        location_name_fn = lambda n: str(n)

    route_col, path_col = st.columns([1, 2])
    with route_col:
        st.subheader("Lieferweg")
        st.metric("Gesamtkosten", f"{route_cpython.cost:.2f} EUR")
        st.metric("Anzahl Stationen", len(route_cpython.path))
        st.metric("CPython", f"{route_cpython.time_ms:.3f} ms")
        st.metric("Numba", f"{route_numba.time_ms:.3f} ms")
    with path_col:
        st.subheader("Route")
        _display_route_map(route_cpython.path, location_name_fn)


def _display_route_map(path: list[int], location_name_fn: Callable[[int], str]) -> None:
    import streamlit as st

    if len(path) <= 15:
        _display_route_horizontal(path, location_name_fn)
    else:
        _display_route_compact(path, location_name_fn)


def _display_route_horizontal(path: list[int], location_name_fn: Callable[[int], str]) -> None:
    import streamlit as st

    for i, node in enumerate(path):
        if i == 0:
            st.markdown(
                f"""
                <div style="padding: 10px; background: #FF6B35; border-radius: 10px; color: white; margin-bottom: 5px;">
                    <strong>{location_name_fn(node)}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif i == len(path) - 1:
            st.markdown(
                f"""
                <div style="padding: 10px; background: #4CAF50; border-radius: 10px; color: white; margin-bottom: 5px;">
                    <strong>{location_name_fn(node)}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="padding: 10px; background: #2196F3; border-radius: 10px; color: white; margin-bottom: 5px;">
                    <strong>{location_name_fn(node)}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if i < len(path) - 1:
            st.markdown("<div style='text-align: center; color: #999; margin: -10px 0;'>|</div>", unsafe_allow_html=True)


def _display_route_compact(path: list[int], location_name_fn: Callable[[int], str]) -> None:
    import streamlit as st

    start = path[:4]
    end = path[-3:]
    middle_count = len(path) - 7

    for i, node in enumerate(start):
        if i == 0:
            st.markdown(
                f"""
                <div style="padding: 8px; background: #FF6B35; border-radius: 8px; color: white; margin-bottom: 5px;">
                    <strong>{location_name_fn(node)}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="padding: 8px; background: #2196F3; border-radius: 8px; color: white; margin-bottom: 5px;">
                    <strong>{location_name_fn(node)}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("<div style='text-align: center; color: #999; margin: -10px 0;'>|</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center; padding: 8px; background: #EEE; border-radius: 8px; color: #666; margin: 10px 0;">
            ... {middle_count} weitere Stationen ...
        </div>
        """,
        unsafe_allow_html=True
    )

    for i, node in enumerate(end):
        if i == len(end) - 1:
            st.markdown(
                f"""
                <div style="padding: 8px; background: #4CAF50; border-radius: 8px; color: white; margin-bottom: 5px;">
                    <strong>{location_name_fn(node)}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="padding: 8px; background: #2196F3; border-radius: 8px; color: white; margin-bottom: 5px;">
                    <strong>{location_name_fn(node)}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        if i < len(end) - 1:
            st.markdown("<div style='text-align: center; color: #999; margin: -10px 0;'>|</div>", unsafe_allow_html=True)


def display_benchmark_results(
    cpython_result: BenchmarkResult,
    numba_result: BenchmarkResult,
    pypy_result: BenchmarkResult,
) -> None:
    import pandas as pd
    import streamlit as st

    results_df = pd.DataFrame(
        [
            {
                "Umgebung": cpython_result.strategy_name,
                "Durchschnitt (ms)": cpython_result.mean_ms,
                "Standardabweichung (ms)": cpython_result.std_ms,
            },
            {
                "Umgebung": numba_result.strategy_name,
                "Durchschnitt (ms)": numba_result.mean_ms,
                "Standardabweichung (ms)": numba_result.std_ms,
            },
            {
                "Umgebung": pypy_result.strategy_name,
                "Durchschnitt (ms)": pypy_result.mean_ms,
                "Standardabweichung (ms)": pypy_result.std_ms,
            },
        ]
    ).sort_values("Durchschnitt (ms)")

    st.subheader("Benchmark-Ergebnisse")
    st.dataframe(results_df, width='stretch', hide_index=True)
    st.bar_chart(results_df.set_index("Umgebung")[["Durchschnitt (ms)"]])
    fastest = results_df.iloc[0]
    st.success(
        f"Schnellste Variante: **{fastest['Umgebung']}** mit durchschnittlich "
        f"**{fastest['Durchschnitt (ms)']:.3f} ms**."
    )
