```mermaid
flowchart LR
    %% Externe Akteure / Systeme
    Bear["Bär / Produktionsleiter"]
    Customer["Kunde / Abnehmer"]
    QA["Qualitätsprüfung (extern)"]
    Dev["Entwickler"]
    IDE["IDE (z. B. VS Code)"]
    CI["CI-Pipeline (optional)"]
    MyPy["mypy (Type Checker)"]
    FS["Dateisystem / Persistenz\n(z. B. JSON/CSV)"]

    %% Systemgrenze
    System["Bear Honeyworks\n(Honigfabrik-Software)\n\n- Domänenmodell\n- Produktionslogik\n- Lagerverwaltung\n- Bestellverarbeitung\n- Typisierte Schnittstellen"]

    %% Datenflüsse
    Bear -->|Produktionsauftrag / Parameter| System
    System -->|Produktionsreport / Status| Bear

    Customer -->|Bestellung (Sorte, Menge)| System
    System -->|Bestellbestätigung / Rechnung| Customer

    QA -->|Qualitätsfreigabe / Bewertung| System
    System -->|Prüfanforderung / Proben-Daten| QA

    %% Persistenz
    System <--> |Speichern / Laden (Bestand, Orders)| FS

    %% Typprüfung / Dev-Workflow
    Dev -->|ändert Code| System
    Dev -->|startet Checks| MyPy
    IDE -->|führt mypy aus / zeigt Fehler| MyPy
    CI -->|autom. Typcheck| MyPy
    MyPy -->|Typfehler / Hinweise| Dev

    %% Verbindung mypy <-> Codebase (konzeptionell)
    MyPy ---|analysiert Typannotationen| System