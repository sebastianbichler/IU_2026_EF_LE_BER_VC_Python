"""Unit tests for sensor_benchmark.py – eager/lazy processing and benchmarks."""

from sensor_benchmark import (
    process_eager,
    process_lazy,
    benchmark_eager,
    benchmark_lazy,
)
from sensors import stream_soil_moisture
from itertools import islice


class TestProcessEager:
    """Tests for process_eager()."""

    def test_filters_correctly(self):
        """Should only keep readings with moisture < 35 or > 80."""
        data = [
            {"bed_id": 1, "moisture": 20.0, "timestamp": None},
            {"bed_id": 1, "moisture": 50.0, "timestamp": None},
            {"bed_id": 1, "moisture": 90.0, "timestamp": None},
        ]
        result = process_eager(data)
        assert len(result) == 2

    def test_irrigation_need_calculation(self):
        """irrigation_need should be 100 - moisture, clamped to [0, 100]."""
        data = [{"bed_id": 1, "moisture": 20.0, "timestamp": None}]
        result = process_eager(data)
        assert result[0]["irrigation_need"] == 80

    def test_empty_input(self):
        """Empty input should return empty list."""
        assert process_eager([]) == []

    def test_all_normal_filtered_out(self):
        """Readings all in normal range should result in empty output."""
        data = [
            {"bed_id": 1, "moisture": 50.0, "timestamp": None},
            {"bed_id": 1, "moisture": 60.0, "timestamp": None},
        ]
        assert process_eager(data) == []


class TestProcessLazy:
    """Tests for process_lazy()."""

    def test_filters_correctly(self):
        """Should produce same filtered results as eager."""
        data = [
            {"bed_id": 1, "moisture": 20.0, "timestamp": None},
            {"bed_id": 1, "moisture": 50.0, "timestamp": None},
            {"bed_id": 1, "moisture": 90.0, "timestamp": None},
        ]
        result = process_lazy(iter(data))
        assert len(result) == 2

    def test_max_items_limit(self):
        """Should respect max_items parameter."""
        data = [
            {"bed_id": 1, "moisture": 10.0, "timestamp": None},
            {"bed_id": 1, "moisture": 15.0, "timestamp": None},
            {"bed_id": 1, "moisture": 20.0, "timestamp": None},
        ]
        result = process_lazy(iter(data), max_items=2)
        assert len(result) == 2

    def test_consistent_with_eager(self):
        """Lazy and eager should produce the same results for the same input."""
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
    """Tests for benchmark_eager()."""

    def test_returns_valid_dict(self):
        """Should return a dict with time, peak_memory_mb, data_size_mb, result_count."""
        result = benchmark_eager(bed_id=1, num_readings=100)
        assert isinstance(result, dict)
        assert "time" in result
        assert "peak_memory_mb" in result
        assert "data_size_mb" in result
        assert "result_count" in result

    def test_time_is_positive(self):
        """Processing time should be > 0."""
        result = benchmark_eager(bed_id=1, num_readings=100)
        assert result["time"] > 0

    def test_result_count_non_negative(self):
        """Result count should be >= 0."""
        result = benchmark_eager(bed_id=1, num_readings=100)
        assert result["result_count"] >= 0


class TestBenchmarkLazy:
    """Tests for benchmark_lazy()."""

    def test_returns_valid_dict(self):
        """Should return a dict with the same keys as benchmark_eager."""
        result = benchmark_lazy(bed_id=1, num_readings=100)
        assert isinstance(result, dict)
        assert "time" in result
        assert "peak_memory_mb" in result
        assert "data_size_mb" in result
        assert "result_count" in result

    def test_time_is_positive(self):
        """Processing time should be > 0."""
        result = benchmark_lazy(bed_id=1, num_readings=100)
        assert result["time"] > 0

    def test_lazy_uses_less_memory_for_large_n(self):
        """For large N, lazy should use less peak memory than eager."""
        eager = benchmark_eager(bed_id=1, num_readings=50_000)
        lazy = benchmark_lazy(bed_id=1, num_readings=50_000)
        assert lazy["peak_memory_mb"] < eager["peak_memory_mb"]
