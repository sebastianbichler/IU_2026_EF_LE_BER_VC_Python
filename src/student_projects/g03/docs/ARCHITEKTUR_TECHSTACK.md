# 3. Architektur und Tech-Stack

Dieses Dokument beschreibt die Architektur der RabbitFarm-Anwendung sowie die Auswahl und den Einsatz der verwendeten Technologien. Es entspricht **Kapitel 3** des Projektabschlussberichts.

---

## 3.1 Auswahl der Plattform (Begründung)

### Gewählte Plattform: Web-UI (Flask)

Für die Nutzeroberfläche wurde eine **klassische Web-Anwendung** mit **Flask** umgesetzt. Die Interaktion erfolgt im Browser über HTML-Seiten mit serverseitigem Rendering (Jinja2-Templates) und einer festen Sidebar-Navigation – die Anwendung verhält sich wie eine **Arbeits-App** (Dashboard, Formulare, Tabellen), nicht wie eine reine Informations-Webseite.

### Begründung der Entscheidung

| Kriterium | Web-UI (Flask) | Alternative: Streamlit | Alternative: Nur Jupyter |
|-----------|-----------------|------------------------|---------------------------|
| **Lernziel** | Klassisches Web-Framework, Trennung Frontend/Backend, Wiederverwendbarkeit des Kerns | Schnelle Prototypen, weniger Kontrolle über Struktur | Fokus auf Analyse; wenig „echte“ App-Struktur |
| **Wiederverwendung** | Kern (`models`, `data_manager`, `services`, `sensors`) bleibt UI-frei und kann von CLI, anderen Frontends oder Tests genutzt werden | Logik oft eng mit Streamlit-Widgets verknüpft | Notebooks eignen sich vor allem für Experimente und Auswertung |
| **Struktur** | Klare Trennung: Routen, Templates, Static; gut erweiterbar (z. B. weitere Blueprints) | Weniger klassische Schichten; State in Session | Pro Notebook ein eigener Kontext; schwer als einheitliche App zu betreiben |
| **Wissenschaftlicher Teil** | Sensordaten-Benchmark (Lazy vs. Eager) ist als eigene Seite integriert; gleicher Kern wie im Jupyter-Notebook | Möglich, aber Benchmark-Logik würde typisch im gleichen Skript liegen | Ideal für Analyse und Plots; bereits in `static/notebooks/` umgesetzt |

### Warum keine reine GUI (tkinter, PyQt)?

- **Verteilbarkeit:** Web-UI läuft im Browser, keine lokale Python-Installation für Endnutzer nötig (nur Server).
- **Einheitlichkeit:** Eine Codebasis für Kern; Web und ggf. Terminal-App nutzen dieselben Module.
- **Themenfokus:** Das Projekt soll Lazy Evaluation und funktionale Aspekte in Python zeigen; Flask erfordert explizite Struktur (Routen, Importe) und fördert damit die Trennung von Kern und Oberfläche.

### Rolle der Jupyter-Notebooks

Die **Jupyter-Notebooks** in `static/notebooks/` (z. B. Lazy vs. Eager, Generatoren) bleiben die **primäre Umgebung für die wissenschaftliche Auswertung** und Visualisierung. Die Web-UI bietet eine **anwendungsnahe Oberfläche** zum Testen der gleichen Logik (Sensordaten-Benchmark) und zur täglichen Nutzung (Beete, Gemüse, Lager, Kunden, Bestellungen, Finanzen). Damit ergänzen sich **Forschung/Lehre (Notebook)** und **Anwendung (Web-App)**.

---

## 3.2 Modularer Kern und Open-Closed Principle

### Grundidee

Die **Geschäftslogik** (Domänenmodelle, Persistenz, Dienste, Sensoren) ist in Modulen unter `src/` gekapselt und **unabhängig von der Art der Oberfläche**. Neue Oberflächen (z. B. REST-API, zweites Frontend) können hinzugefügt werden, **ohne den Kern zu ändern** (Open for Extension, Closed for Modification).

### Schichtenüberblick

```
┌─────────────────────────────────────────────────────────────────┐
│  Präsentation (Presentation)                                       │
│  • Web-UI: src/web/ (Flask, routes.py, templates/, static/)       │
│  • Optional: Terminal-App (src/terminal-app/), Jupyter-Notebooks  │
└───────────────────────────────┬───────────────────────────────────┘
                                │ importiert / nutzt
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Kern (Core / Domain + Application)                              │
│  • models.py      – Domänenmodelle (Vegetable, Bed, Customer, …)  │
│  • data_manager.py – Persistenz (load_data, save_data, JSON)      │
│  • services.py    – Geschäftslogik (calculate_profit, Abo-Boxen)   │
│  • sensors.py     – Sensordaten-Generator (stream_soil_moisture)   │
│  • sensor_benchmark.py – Lazy/Eager-Benchmark (process_*, benchmark_*) │
└───────────────────────────────┬───────────────────────────────────┘
                                │ liest/schreibt
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Daten (Persistence)                                              │
│  • data/rabbitfarm_data.json                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Abhängigkeitsrichtung

- **Web-UI** importiert nur aus dem Kern: `data_manager`, `models`, ggf. `sensor_benchmark`. Sie kennt keine Details der JSON-Struktur; das übernimmt `data_manager`.
- **Kern** importiert weder Flask noch andere UI-Bibliotheken. Er nutzt nur Standardbibliothek, typische Datenverarbeitung (datetime, json, itertools) und die eigenen Module unter `src/`.

Damit bleibt die **Domänenlogik** (z. B. Frische eines Gemüses, Berechnung von Bewässerungsbedarf, Gewinnmarge) an einer Stelle und wird von allen Oberflächen gemeinsam genutzt.

### Konkrete Umsetzung im Projekt

| Komponente | Verantwortung | Abhängigkeiten |
|------------|----------------|----------------|
| `models.py` | Dataclasses, Methoden wie `is_fresh()`, `freshness_ratio()`, `add_harvest()` | Nur stdlib (datetime, typing, dataclasses) |
| `data_manager.py` | Laden/Speichern von vegetables, beds, customers, inventory, orders | `models`, os, json |
| `services.py` | Abo-Box-Generierung, Gewinnberechnung | `models`, itertools |
| `sensors.py` | Generator für Bodenfeuchtigkeit | random, datetime, typing |
| `sensor_benchmark.py` | process_eager, process_lazy, benchmark_eager, benchmark_lazy | `sensors`, itertools, time, tracemalloc |
| `src/web/` | Routen, Templates, Formulare, Start | Flask, oben genannte Kern-Module |

Erweiterungen (z. B. neuer Use Case „Berichte exportieren“) werden idealerweise im **Kern** (neue Funktion in `services` oder neuem Modul) implementiert; die Web-UI ruft nur diese neue Funktion auf, ohne Kern-Logik zu duplizieren.

---

## 3.3 Technologie-Stack

### Übersicht

| Kategorie | Technologie | Version / Quelle | Rolle im Projekt |
|-----------|-------------|-------------------|-------------------|
| **Sprache** | Python | 3.10+ empfohlen | Laufzeitumgebung |
| **Web-Framework** | Flask | ≥ 2.0 (`requirements.txt`) | Routing, Request/Response, Session; WSGI-App |
| **Templating** | Jinja2 | (mit Flask) | HTML-Seiten (layout, index, vegetables, beds, inventory, customers, orders, finance, sensors) |
| **Frontend-Styling** | Bootstrap | 5.3.2 (CDN) | Layout, Grid, Formulare, Buttons, Tabellen |
| **Icons** | Bootstrap Icons | 1.11.1 (CDN) | Sidebar, Dashboard, Buttons |
| **Persistenz** | JSON (stdlib) | – | `data/rabbitfarm_data.json`; Ein-/Ausgabe über `data_manager` |
| **Datenverarbeitung** | pandas | ≥ 1.3 | Optional; Auswertung, Tabellen (z. B. in Notebooks) |
| **Numerik** | NumPy | ≥ 1.21 | Optional; Basis für pandas und ggf. Auswertungen |
| **Visualisierung** | Matplotlib | ≥ 3.5 | Plots in Jupyter-Notebooks (Lazy vs. Eager, Benchmarks) |
| **Notebooks** | Jupyter, ipykernel, ipywidgets | siehe requirements | Wissenschaftliche Auswertung, Lazy/Eager-Demos, ggf. UI-Prototypen |
| **Speicheranalyse** | memory-profiler, tracemalloc | memory-profiler ≥ 0.60; tracemalloc (stdlib) | Benchmark Lazy vs. Eager (Speicherverbrauch); tracemalloc in `sensor_benchmark` |
| **Tests** | pytest (optional) | – | Unit- und Integrationstests; siehe IMPLEMENTIERUNG_QUALITAETSSICHERUNG.md |

### Detaillierte Rollen

- **Flask:** Zentrale Web-App in `src/web/app.py`; Registrierung eines Blueprints (`routes.py`) für alle Seiten; Bereitstellung von `static` (CSS) und `templates` (Jinja2). Keine direkte Geschäftslogik in den Routen – Aufruf von `data_manager` und Modellen.
- **Bootstrap (CDN):** Keine lokale Installation; einheitliches, responsives Layout (Sidebar, Karten, Formulare, Tabellen) und schnelle Anpassung ohne eigenes CSS-Framework.
- **Jinja2:** Vererbung (`extends layout.html`), Blöcke (`block content`), Schleifen und Bedingungen für Listen/Tabellen; `url_for` für Links und Static-URLs.
- **JSON:** Einfache, dateibasierte Persistenz ohne Datenbankserver; gut für den Projektumfang und Portabilität; Struktur in `data_manager` gekapselt.
- **tracemalloc (stdlib):** In `sensor_benchmark.py` für die Messung des Speicherverbrauchs bei Eager- vs. Lazy-Benchmarks; Ergebnis (z. B. Peak in MB) wird in der Web-UI auf der Seite „Sensordaten“ angezeigt.
- **itertools (stdlib):** In `sensors`, `sensor_benchmark` und `services`: `islice`, `filter`, `map`, `cycle` für generatorbasierte (lazy) Verarbeitung und Abo-Box-Generierung.

### Abhängigkeiten laut `src/requirements.txt`

```
matplotlib>=3.5.0
numpy>=1.21.0
pandas>=1.3.0
memory-profiler>=0.60.0
jupyter>=1.0.0
ipykernel>=6.0.0
ipywidgets>=7.6.0
memory_profiler>=0.61.0
flask>=2.0.0
```

Die **Web-UI** benötigt davon mindestens **Flask**. Matplotlib, NumPy, Pandas, Jupyter und Memory-Profiler werden vor allem in den **Jupyter-Notebooks** und für die wissenschaftliche Auswertung genutzt; die im Web verwendete Benchmark-Logik nutzt nur die Standardbibliothek (inkl. `tracemalloc`) und das Modul `sensors`.

---

## Kurzfassung

- **Plattform:** Web-UI mit Flask als Hauptoberfläche; Begründung gegenüber Streamlit, reiner Notebook-Lösung und klassischer Desktop-GUI (Verteilbarkeit, klare Struktur, Wiederverwendung des Kerns).
- **Architektur:** Modularer Kern unter `src/` (Modelle, Daten, Dienste, Sensoren, Benchmark); Web-UI in `src/web/` als eine von mehreren möglichen Präsentationsschichten; Open-Closed-Prinzip durch strikte Abhängigkeitsrichtung (UI → Kern → Daten).
- **Tech-Stack:** Flask, Jinja2, Bootstrap (inkl. Icons) für die Web-App; JSON für Persistenz; Python-Standardbibliothek (tracemalloc, itertools) und ggf. memory-profiler für Benchmarks; pandas, NumPy, Matplotlib, Jupyter für Analyse und Notebooks.

Dieses Dokument kann als Kapitel **3** in den Projektabschlussbericht übernommen werden.
