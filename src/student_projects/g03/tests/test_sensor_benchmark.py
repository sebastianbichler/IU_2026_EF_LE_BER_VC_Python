"""Unit-Tests für sensor_benchmark.py – Eager/Lazy-Verarbeitung und Benchmarks."""

from sensor_benchmark import (
    process_eager,
    process_lazy,
    benchmark_eager,
    benchmark_lazy,
)
from sensors import stream_soil_moisture
from itertools import islice


class TestProcessEager:
    """Tests für process_eager()."""

    def test_filters_correctly(self):
        """Behält nur Messwerte, bei denen die Feuchtigkeit < 35 oder > 80 ist."""
        data = [
            {"bed_id": 1, "moisture": 20.0, "timestamp": None},
            {"bed_id": 1, "moisture": 50.0, "timestamp": None},
            {"bed_id": 1, "moisture": 90.0, "timestamp": None},
        ]
        result = process_eager(data)
        assert len(result) == 2

    def test_irrigation_need_calculation(self):
        """Der Bewässerungsbedarf errechnet sich aus 100 - Feuchtigkeit und bleibt im Bereich [0, 100]."""
        data = [{"bed_id": 1, "moisture": 20.0, "timestamp": None}]
        result = process_eager(data)
        assert result[0]["irrigation_need"] == 80

    def test_empty_input(self):
        """Eine leere Eingabe liefert eine leere Liste zurück."""
        assert process_eager([]) == []

    def test_all_normal_filtered_out(self):
        """Messwerte im Normalbereich erzeugen eine leere Ausgabe."""
        data = [
            {"bed_id": 1, "moisture": 50.0, "timestamp": None},
            {"bed_id": 1, "moisture": 60.0, "timestamp": None},
        ]
        assert process_eager(data) == []


class TestProcessLazy:
    """Tests für process_lazy()."""

    def test_filters_correctly(self):
        """Erzeugt die gleichen gefilterten Ergebnisse wie der Eager-Ansatz."""
        data = [
            {"bed_id": 1, "moisture": 20.0, "timestamp": None},
            {"bed_id": 1, "moisture": 50.0, "timestamp": None},
            {"bed_id": 1, "moisture": 90.0, "timestamp": None},
        ]
        result = process_lazy(iter(data))
        assert len(result) == 2

    def test_max_items_limit(self):
        """Berücksichtigt den max_items-Parameter."""
        data = [
            {"bed_id": 1, "moisture": 10.0, "timestamp": None},
            {"bed_id": 1, "moisture": 15.0, "timestamp": None},
            {"bed_id": 1, "moisture": 20.0, "timestamp": None},
        ]
        result = process_lazy(iter(data), max_items=2)
        assert len(result) == 2

    def test_consistent_with_eager(self):
        """Lazy- und Eager-Ausführung liefern bei gleicher Eingabe dieselben Resultate."""
        data = [
            {"bed_id": 1, "moisture": 10.0, "timestamp": None},
            {"bed_id": 1, "moisture": 50.0, "timestamp": None},
            {"bed_id": 1, "moisture": 85.0, "timestamp": None},
            {"bed_id": 1, "moisture": 30.0, "timestamp": None},
        ]
        eager_result = process_eager(data)
        lazy_result = process_lazy(iter(data))
        assert len(eager_result) == len(lazy_result)
        for e, l in zip(eager_result, lazy_result):
            assert e["moisture"] == l["moisture"]
            assert e["irrigation_need"] == l["irrigation_need"]


class TestBenchmarkEager:
    """Tests für benchmark_eager()."""

    def test_returns_valid_dict(self):
        """Liefert ein Dictionary mit time, peak_memory_mb, data_size_mb und result_count zurück."""
        result = benchmark_eager(bed_id=1, num_readings=100)
        assert isinstance(result, dict)
        assert "time" in result
        assert "peak_memory_mb" in result
        assert "data_size_mb" in result
        assert "result_count" in result

    def test_time_is_positive(self):
        """Die Verarbeitungszeit liegt über 0."""
        result = benchmark_eager(bed_id=1, num_readings=100)
        assert result["time"] > 0

    def test_result_count_non_negative(self):
        """Die Anzahl der Ergebnisse ist mindestens 0."""
        result = benchmark_eager(bed_id=1, num_readings=100)
        assert result["result_count"] >= 0


class TestBenchmarkLazy:
    """Tests für benchmark_lazy()."""

    def test_returns_valid_dict(self):
        """Gibt ein Dictionary mit denselben Schlüsseln wie benchmark_eager zurück."""
        result = benchmark_lazy(bed_id=1, num_readings=100)
        assert isinstance(result, dict)
        assert "time" in result
        assert "peak_memory_mb" in result
        assert "data_size_mb" in result
        assert "result_count" in result

    def test_time_is_positive(self):
        """Die Verarbeitungszeit liegt über 0."""
        result = benchmark_lazy(bed_id=1, num_readings=100)
        assert result["time"] > 0

    def test_lazy_uses_less_memory_for_large_n(self):
        """Für große Datenmengen beansprucht Lazy weniger Speicher als Eager."""
        eager = benchmark_eager(bed_id=1, num_readings=50_000)
        lazy = benchmark_lazy(bed_id=1, num_readings=50_000)
        assert lazy["peak_memory_mb"] < eager["peak_memory_mb"]
