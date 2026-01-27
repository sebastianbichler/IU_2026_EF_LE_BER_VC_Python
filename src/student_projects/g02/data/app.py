from storage.dataGenerator import DataGenerator
from storage.nutStorage import NutStorage
from engine.nativeEngine import NativePythonEngine
from engine.numpyEngine import NumpyVectorizedEngine
from benchmark.performance import PerformanceMonitor

class SquirrelApp:

    def run_benchmark(self, n_samples: int):
        data = DataGenerator.generate_dataset(n_samples)
        storage = NutStorage(data)

        native = NativePythonEngine()
        numpy_engine = NumpyVectorizedEngine()

        native_time = PerformanceMonitor.measure_execution_time(
            native.find_stolen_nuts,
            storage.get_data_as_native_list()
        )

        numpy_time = PerformanceMonitor.measure_execution_time(
            numpy_engine.find_stolen_nuts,
            storage.get_data_as_numpy()
        )

        print(f"Native Python: {native_time:.6f}s")
        print(f"NumPy SIMD:    {numpy_time:.6f}s")
        print(f"Speedup:      {native_time / numpy_time:.2f}x")


if __name__ == "__main__":
    app = SquirrelApp()
    app.run_benchmark(1_000_000)
