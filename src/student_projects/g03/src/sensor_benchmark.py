"""
Lazy vs. Eager Benchmark für Sensordaten.
Eager: alle Werte in einer Liste im Speicher.
Lazy: Generator-Pipeline, nur bei Bedarf berechnet.
"""
import sys
import time
import tracemalloc
from itertools import islice

from sensors import stream_soil_moisture


def process_eager(data_list, threshold_low=35.0):
    """Eager: Liste komplett im Speicher, Filter + Map als Listen."""
    filtered = [
        d for d in data_list
        if d["moisture"] < threshold_low or d["moisture"] > 80.0
    ]
    return [
        {
            "bed_id": d["bed_id"],
            "moisture": d["moisture"],
            "irrigation_need": max(0, min(100, 100 - d["moisture"])),
        }
        for d in filtered
    ]


def process_lazy(data_gen, threshold_low=35.0, max_items=None):
    """Lazy: Generator-Pipeline mit filter/map, begrenzt mit islice."""
    filtered = filter(
        lambda d: d["moisture"] < threshold_low or d["moisture"] > 80.0,
        data_gen,
    )
    irrigation = map(
        lambda d: {
            "bed_id": d["bed_id"],
            "moisture": d["moisture"],
            "irrigation_need": max(0, min(100, 100 - d["moisture"])),
        },
        filtered,
    )
    if max_items is not None:
        irrigation = islice(irrigation, max_items)
    return list(irrigation)


def benchmark_eager(bed_id: int, num_readings: int, base_moisture: float = 50.0):
    """Benchmark: Eager (Liste). Liefert Zeit, Speicher, Anzahl Ergebnisse."""
    tracemalloc.start()
    start = time.perf_counter()

    stream = stream_soil_moisture(bed_id=bed_id, base_moisture=base_moisture)
    data_list = list(islice(stream, num_readings))
    result = process_eager(data_list)

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    data_size = sys.getsizeof(data_list)
    for item in data_list[:100]:
        data_size += sys.getsizeof(item)

    return {
        "time": elapsed,
        "peak_memory_mb": peak / 1024 / 1024,
        "data_size_mb": data_size / 1024 / 1024,
        "result_count": len(result),
    }


def benchmark_lazy(bed_id: int, num_readings: int, base_moisture: float = 50.0):
    """Benchmark: Lazy (Generator). Liefert Zeit, Speicher, Anzahl Ergebnisse."""
    tracemalloc.start()
    start = time.perf_counter()

    stream = stream_soil_moisture(bed_id=bed_id, base_moisture=base_moisture)
    limited = islice(stream, num_readings)
    result = process_lazy(limited)

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    gen_size = sys.getsizeof(limited)

    return {
        "time": elapsed,
        "peak_memory_mb": peak / 1024 / 1024,
        "data_size_mb": gen_size / 1024 / 1024,
        "result_count": len(result),
    }
