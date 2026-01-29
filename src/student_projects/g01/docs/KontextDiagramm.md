```mermaid
flowchart LR
    %% --- Styling Definitionen ---
    classDef system fill:#f96,stroke:#333,stroke-width:2px,color:white;
    classDef actor fill:#fff,stroke:#333,stroke-width:1px;
    classDef external fill:#eee,stroke:#333,stroke-dasharray: 5 5;

    %% --- Knoten (Nodes) ---
    User("👤 Fiona Fuchs<br>(Dispatcher)"):::actor
    
    %% Das Hauptsystem beinhaltet CPython und Numba
    System("🦊 FoxExpress<br>(Streamlit auf CPython + Numba)"):::system
    
    %% Externe Systeme
    PyPyEnv("⚙️ PyPy Umgebung<br>(Externer Prozess)"):::external
    FileSystem("📂 Dateisystem<br>(CSV-Export / Logs)"):::external

    %% --- Beziehungen (Data Flow) ---
    %% User Interaktion
    User -- "1. Konfiguriert Route & Startet Benchmark" --> System
    System -- "5. Visualisiert Karte & Laufzeit-Vergleich" --> User
    System -- "2. Führt Algorithmus aus" --> System

    %% PyPy Subprozess (Besonderheit)
    System -- "2. Startet Subprozess (script.py)" --> PyPyEnv
    PyPyEnv -- "3. Führt Algorithmus aus (JIT-Tracing)" --> PyPyEnv
    PyPyEnv -- "4. Liefert Messdaten (JSON/Stdout)" --> System

    %% Dateisystem
    System -.-> |Optional| FileSystem
