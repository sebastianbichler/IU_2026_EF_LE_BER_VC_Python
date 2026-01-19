# Projekt-Ressourcenplanung: Sloth’s Slow-Motion Hotel

Diese Dokumentation definiert die notwendigen technischen, datenseitigen und infrastrukturellen Ressourcen für die Umsetzung des Projekts. Ziel ist ein moderner, robuster Tech-Stack, der professionelle Software-Entwicklung (Clean Code) unterstützt.

---

## 1. Entwicklungsumgebung (Development Environment)

### Python Version
* **Python 3.13**
    * *Grund:* Wir benötigen Zugriff auf das `match` / `case` Statement (Structural Pattern Matching), welches erst ab Python 3.10 verfügbar ist. Dies ist essenziell für die elegante Umsetzung des **State Patterns** im Zustandsautomaten des Gastes.

### Code Quality Tools (Modern Standards)
Um die Anforderung "lesbarer, strukturierter Code" technisch zu erzwingen, werden folgende Tools in die Pipeline integriert:
* **Ruff** (oder Flake8): Ein moderner, extrem schneller Linter, um PEP8-Konformität zu prüfen.
* **Black**: Ein "uncompromising code formatter", der unseren Code automatisch formatiert. Damit garantieren wir einheitlichen Stil ohne manuelle Diskussionen.
* **Mypy**: Für statische Typ-Prüfung (Static Type Checking). Da wir wissenschaftlich arbeiten, ist Typ-Sicherheit (Type Hints) ein Muss.

---

## 2. Bibliotheken & Frameworks

Wir unterscheiden zwischen Standard-Bibliotheken (Core) und externen, modernen Frameworks, die über `pip` installiert werden.

### A. Externe Bibliotheken ("Modern Stack")
Diese Pakete müssen in der `requirements.txt` definiert werden.

1.  **Pydantic** (Daten-Validierung)
    * *Zweck:* Anstatt händisch `if`-Abfragen zu schreiben, um zu prüfen, ob Schritte negativ sind oder Buchungen < 7 Tage dauern, nutzen wir Pydantic-Models.
    * *Use-Case:* Validierung des User-Inputs (z.B. bei der Eingabe der Schritte für den Rabatt).
2.  **Pytest** (Testing Framework)
    * *Zweck:* Ersatz für das veraltete `unittest`. Pytest ist der aktuelle Industrie-Standard. Es erlaubt schlankere Tests und bessere Fehlerberichte ("Fixtures" statt "Setup/Teardown").
3.  **Faker** (Daten-Generierung)
    * *Zweck:* Um realistische Testdaten (Namen von Gästen, zufällige Datumsangaben) für unsere Simulationen zu erzeugen.

### B. Python Standard Library (Built-in)
Wird für die Kernlogik verwendet, um Abhängigkeiten gering zu halten.

* **`abc` (Abstract Base Classes):** Zwingend erforderlich für die saubere Architektur des **State Patterns** (Definition von Interfaces).
* **`datetime` / `time`:** Für die Zeit-Logik (Reifezeit der Blätter, 3h Weck-Verzögerung).
* **`json`:** Zum Speichern und Laden der Persistenz-Daten.
* **`logging`:** Für professionelle Ausgaben statt einfacher `print()` Befehle (Requirement: Dokumentierter Code).

---

## 3. Datensätze (Data Strategy)

Da keine externe Datenbank (SQL) gefordert ist, aber "Datensätze" notwendig sind, arbeiten wir mit **dateibasierter Persistenz (JSON)**.

### A. Synthetische Stammdaten (Master Data)
Diese Dateien werden initial angelegt:
* `data/menu_catalog.json`: Eine Datenbank mit Blättern, ihren Reifezeiten und Preisen.
    * *Beispiel:* Eukalyptus (Premium), Eiche (Standard).

### B. Transaktionsdaten (Dynamic Data)
Diese Dateien werden durch die App verändert:
* `data/bookings.json`: Speichert aktive Buchungen.
    * *Struktur:* `GuestID`, `RoomType`, `StartDate`, `EndDate` (Pydantic validiert hier die 7-Tage-Regel).
* `data/guest_stats.json`: Speichert die Bewegungsprofile.
    * *Inhalt:* Schritte pro Tag, errechneter Rabatt-Level, aktueller "Faulheits-Status" (State).

---

## 4. Infrastruktur & Dokumentation

### Versionskontrolle
* **Git:** Lokales Repository.
* **.gitignore:** Ausschluss von `venv/`, `__pycache__/` und `.pytest_cache/`.

### Visualisierung
* **Mermaid.js:** Für die dynamische Generierung von Diagrammen (Use-Case, State-Machine) direkt in der Markdown-Dokumentation (README.md).

### CI/CD Simulation
* **Makefile** (oder `tasks.py`): Ein Skript, das die Pipeline-Befehle bündelt.
    * `make install` -> Installiert Requirements.
    * `make format` -> Führt Black & Ruff aus.
    * `make test` -> Führt Pytest aus.

---

## 5. Zusammenfassung der `requirements.txt`

```text
# Core Logic
pydantic>=2.4.0

# Testing & Quality (Dev Dependencies)
pytest>=7.4.0
pytest-cov>=4.1.0   # Für Test-Coverage Berichte
black>=23.9.0
ruff>=0.1.0
faker>=19.0.0
