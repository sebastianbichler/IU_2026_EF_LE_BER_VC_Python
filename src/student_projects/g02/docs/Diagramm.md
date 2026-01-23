```mermaid
classDiagram
    %% Hauptsteuerung der Anwendung
    class SquirrelApp {
        +start_ui()
        +run_benchmark(n_samples)
        +show_results()
    }

    %% Datenhaltung
    class NutStorage {
        -data_arrays : dict
        -data_list : list
        +load_data()
        +get_data_as_numpy()
        +get_data_as_native_list()
    }

    %% Datenerzeugung
    class DataGenerator {
        +generate_dataset(size: int) : dict
    }

    %% Benchmark-Logik (Strategie-Muster)
    class MathKernel {
        <<interface>>
        +calculate_compound_interest(data, rate, years)
        +predict_winter_survival(data, days, temp_factor)
        +find_stolen_nuts(expected, actual)
    }

    class NativePythonEngine {
        +calculate_compound_interest()
        +predict_winter_survival()
        +find_stolen_nuts()
        -note: "Verwendet for-loops"
    }

    class NumpyVectorizedEngine {
        +calculate_compound_interest()
        +predict_winter_survival()
        +find_stolen_nuts()
        -note: "Verwendet SIMD / Broadcasting"
    }

    %% Performance Messung
    class PerformanceMonitor {
        +measure_execution_time(func, data)
        +compare_results(native_time, numpy_time)
        +plot_comparison()
    }

    %% Beziehungen
    SquirrelApp --> NutStorage : verwaltet
    SquirrelApp --> PerformanceMonitor : nutzt
    NutStorage --> DataGenerator : nutzt zur Init
    PerformanceMonitor --> MathKernel : testet
    MathKernel <|.. NativePythonEngine : implementiert
    MathKernel <|.. NumpyVectorizedEngine : implementiert
