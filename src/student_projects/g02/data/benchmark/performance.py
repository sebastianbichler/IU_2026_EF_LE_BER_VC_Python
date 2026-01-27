import time

class PerformanceMonitor:

    @staticmethod
    def measure_execution_time(func, data, runs=5):
        times = []
        for _ in range(runs):
            start = time.perf_counter()
            func(data)
            times.append(time.perf_counter() - start)
        return min(times)
