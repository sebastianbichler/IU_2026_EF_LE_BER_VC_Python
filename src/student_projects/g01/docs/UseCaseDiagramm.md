```mermaid
flowchart LR
    User["👤 Fiona Fuchs(Dispatcher)"]

    subgraph GUI["FoxExpress (Streamlit GUI)"]
        UC1(["Lieferungen verwalten"])
        UC2(["Kürzesten Weg berechnen"])
        UC3(["Benchmark durchführen"])
        UC4(["Ergebnisse visualisieren"])
    end

    %% Beziehung zwischen Akteur und Use Cases
    User --> UC1
    User --> UC2
    User --> UC3

    %% Include-Beziehungen (gestrichelt, wie UML)
    UC3 -.->|include| UC2
    UC3 -.->|include| UC4

    %% Notiz als eigener Knoten
    Note["Testet: CPython, PyPy, Numba"]
    UC3 -.-> Note
