# Projekt-Ressourcenplanung: Sloth’s Slow-Motion Hotel

Diese Dokumentation definiert die notwendigen technischen, datenseitigen und infrastrukturellen Ressourcen für die Umsetzung des Projekts. Ziel ist ein moderner, robuster Tech-Stack, der professionelle Software-Entwicklung (Clean Code) unterstützt und wissenschaftlichen Standards genügt.

---

## 1. Entwicklungsumgebung (Development Environment)

### Python Version
* **Python 3.13** (oder 3.10+)
    * *Warum:* Wir benötigen Zugriff auf das `match` / `case` Statement (Structural Pattern Matching), welches erst ab Python 3.10 eingeführt wurde. Dies ist essenziell für die elegante und lesbare Umsetzung des **State Patterns** (Zustandsautomat des Gastes), da es komplexe `if-elif-else`-Ketten ersetzt.

### Code Quality Tools (Modern Standards)
Um die Anforderung "lesbarer, strukturierter Code" technisch zu erzwingen, werden folgende Tools in die Pipeline integriert:

* **Ruff** (Linter)
    * *Warum:* Ruff ersetzt ältere Tools wie Flake8 oder Pylint. Er ist in Rust geschrieben und extrem schnell. Er hilft uns, potenzielle Bugs und Verstöße gegen PEP8 (Styleguide) in Echtzeit zu finden.
* **Black** (Formatter)
    * *Warum:* Ein "uncompromising code formatter". Er formatiert den Code automatisch beim Speichern. Das garantiert einen einheitlichen Coding-Style im gesamten Projekt und verhindert Diskussionen über Einrückungen oder Klammersetzung.

---

## 2. Bibliotheken & Frameworks

Wir unterscheiden zwischen Standard-Bibliotheken (Core) und externen, modernen Frameworks, die über `pip` installiert werden.

### A. Externe Bibliotheken ("Modern Stack")
Diese Pakete bilden das technologische Rückgrat und müssen in der `requirements.txt` definiert werden.

1.  **Streamlit** (GUI & Frontend)
    * *Zweck:* Framework zur Erstellung von Web-Applikationen rein mit Python.
    * *Warum:* Im Gegensatz zu veralteten GUI-Frameworks wie `tkinter` oder komplexen Web-Stacks (Django/React) ermöglicht Streamlit **Rapid Prototyping**. Es ist der Standard im Data-Science-Bereich. Es erlaubt uns, die Logik (Buchung, State Pattern) interaktiv und visuell ansprechend zu präsentieren, ohne Zeit mit HTML/CSS zu verlieren.
2.  **Pydantic** (Daten-Validierung & Parsing)
    * *Zweck:* Definition von Datenmodellen mit automatischer Validierung.
    * *Warum:* Anstatt händisch fehleranfällige `if`-Abfragen zu schreiben (z.B. `if age < 0: raise Error`), definieren wir deklarative Modelle. Pydantic garantiert, dass Daten, die in unser System gelangen (z.B. User-Input in der GUI oder JSON-Imports), korrekt typisiert sind und den Geschäftsregeln (Requirements) entsprechen.
3.  **Pytest** (Testing Framework)
    * *Zweck:* Framework zum Schreiben und Ausführen von Tests.
    * *Warum:* Ersatz für das eingebaute, aber verbale `unittest`. Pytest ist der aktuelle Industrie-Standard. Es erlaubt schlankere Tests ohne Boilerplate-Code und bietet mit "Fixtures" ein mächtiges Werkzeug für Setup/Teardown-Szenarien (z.B. Erstellen eines Test-Gastes vor jedem Test).
4.  **Faker** (Synthetische Daten)
    * *Zweck:* Generierung von Fake-Daten.
    * *Warum:* Um realistische Simulationen durchzuführen, benötigen wir diverse Namen, Adressen oder Szenarien, ohne echte Personendaten zu verletzen (GDPR/DSGVO Compliance Simulation).

### B. Python Standard Library (Built-in)
Wird für die Kernlogik verwendet, um externe Abhängigkeiten gering zu halten ("Keep it simple").

* **`abc` (Abstract Base Classes):**
    * *Warum:* Zwingend erforderlich für die architektonisch saubere Umsetzung des **State Patterns**. Wir definieren damit ein striktes Interface (`SlothState`), das alle konkreten Zustände (`Sleeping`, `Eating`) implementieren müssen.
* **`datetime` / `time`:**
    * *Warum:* Essenziell für die Business-Logik (Berechnung von 7 Tagen Mindestaufenthalt, Addieren von 3 Stunden Verzögerung beim Weckruf).
* **`json`:**
    * *Warum:* Dient als leichtgewichtige "Datenbank" (Persistenzschicht), da für dieses Projekt kein SQL-Server gefordert ist.
* **`logging`:**
    * *Warum:* Professionelle Software nutzt keine `print()`-Statements für Statusmeldungen, sondern Logging mit verschiedenen Levels (INFO, WARNING, ERROR).

---

## 3. Datensätze (Data Strategy)

Da keine externe Datenbank (SQL) gefordert ist, aber "Datensätze" notwendig sind, arbeiten wir mit **dateibasierter Persistenz (JSON)**. Dies ermöglicht einfaches Backup und menschliche Lesbarkeit.

### A. Synthetische Stammdaten (Master Data)
Diese Dateien sind statisch oder werden initial angelegt:
* `data/config.json`: Zentrale Konfigurationsdatei (z.B. Schwellenwerte für Rabatte, Mindestbuchungsdauer). Vermeidet Hardcoding im Quellcode.
* `data/menu_catalog.json`: Eine Datenbank mit Blättern, ihren Reifezeiten und Preisen.

### B. Transaktionsdaten (Dynamic Data)
Diese Dateien werden durch die App zur Laufzeit verändert:
* `data/bookings.json`: Speichert aktive Buchungen.
* `data/guest_stats.json`: Speichert Bewegungsprofile für statistische Auswertungen im Paper.

---

## 4. Infrastruktur & Dokumentation

### Versionskontrolle
* **Git:** Lokales Repository zur Nachverfolgung von Änderungen.
* **.gitignore:** Ausschluss von `venv/`, `__pycache__/` und `.pytest_cache/`, um das Repository sauber zu halten.

### Visualisierung
* **Mermaid.js:** Erlaubt "Diagrams as Code". Diagramme (Use-Case, State-Machine) werden direkt in Markdown geschrieben. Das macht sie versionierbar und leicht änderbar, im Gegensatz zu exportierten PNG-Dateien.

### CI/CD Simulation
* **Pipeline-Skript (Simulation):** Ein Skript, das die Schritte einer echten CI-Pipeline (Build -> Lint -> Test) lokal ausführt, um die geforderte Qualitätssicherung nachzuweisen.

---

## 5. Zusammenfassung der `requirements.txt`

Hier ist der finale Inhalt der Abhängigkeits-Datei für die Abgabe:

```text
# --- Application Core ---
streamlit>=1.28.0   # GUI Framework
pydantic>=2.4.0     # Data Validation

# --- Testing & Quality (Dev Dependencies) ---
pytest>=7.4.0       # Testing Framework
pytest-cov>=4.1.0   # Test Coverage Reports
faker>=19.0.0       # Data Generation
black>=23.9.0       # Code Formatting
ruff>=0.1.0         # Linting
mypy>=1.6.0         # Static Type Checking
