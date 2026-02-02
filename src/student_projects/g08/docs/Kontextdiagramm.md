```mermaid
flowchart LR
    %% --- Styling Definitionen ---
    classDef system fill:#f96,stroke:#333,stroke-width:2px,color:white;
    classDef actor fill:#fff,stroke:#333,stroke-width:1px;
    classDef external fill:#eee,stroke:#333,stroke-dasharray: 5 5;

    %% --- Knoten (Nodes) ---
    User["Nutzer - Fabrikleitung"]:::actor

    %% Hauptsystem
    System["Bear Honeyworks
    Python Anwendung mit typisiertem Domänenmodell"]:::system

    %% Externe Tools und Systeme
    MyPyTool["mypy Type Checker
    statische Typpruefung"]:::external
    IDE["IDE
    zeigt Typfehler und Hinweise"]:::external
    CI["CI Pipeline optional
    automatischer mypy Check"]:::external
    FileSystem["Dateisystem optional
    JSON CSV Logs"]:::external

    %% --- Beziehungen (Data Flow) ---
    %% User Interaktion
    User -- "1 Eingaben Produktion Lager Bestellung" --> System
    System -- "6 Ausgabe Status Bestand Ergebnisse" --> User

    %% System interne Verarbeitung
    System -- "2 Fuehrt Produktions und Lagerlogik aus" --> System

    %% mypy Check Ablauf
    IDE -- "3 Startet mypy Check" --> MyPyTool
    CI -- "3 Startet mypy Check" --> MyPyTool
    MyPyTool -- "4 Analysiert Typannotationen" --> System
    MyPyTool -- "5 Meldet Typfehler Hinweise" --> IDE

    %% Persistenz optional
    System -.-> |Optional| FileSystem
    FileSystem -.-> |Optional| System