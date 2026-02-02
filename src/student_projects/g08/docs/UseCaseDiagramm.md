```mermaid
flowchart LR
    User["Fabrikleitung / Entwickler"]

    subgraph APP["Bear Honeyworks Anwendung"]
        UC1(["Produktion konfigurieren"])
        UC2(["Honig produzieren"])
        UC3(["Lager verwalten"])
        UC4(["Bestellungen verarbeiten"])
        UC5(["Typpruefung mit mypy ausfuehren"])
        UC6(["Typfehler analysieren"])
    end

    %% Beziehung zwischen Akteur und Use Cases
    User --> UC1
    User --> UC3
    User --> UC4
    User --> UC5

    %% Include Beziehungen
    UC2 -.->|include| UC1
    UC3 -.->|include| UC2
    UC4 -.->|include| UC3
    UC5 -.->|include| UC6

    %% Notiz als eigener Knoten
    Note["Statische Typpruefung
    vor Programmausfuehrung"]
    UC5 -.-> Note