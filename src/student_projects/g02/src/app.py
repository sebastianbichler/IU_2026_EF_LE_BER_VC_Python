"""
Haupt-Controller der Webanwendung

Diese Datei fungiert als Schnittstelle zwischen:
1. Dem Nutzer (Browser/HTTP-Requests)
2. Der Datenhaltung (StashManager)
3. Der Fachlogik (Analyzer)
4. Der Darstellung (Templates/Visualizer)

Verantwortlichkeiten:
- Routing von URLs (z.B. /, /add, /analyze)
- Orchestrierung des Datenflusses
- Bereitstellung der REST-ähnlichen Endpunkte
"""
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import random
import os

# --- Eigene Module (Model & Logic Layer) ---
from .manager import StashManager
from .generator import generate_dummy_data
from .analytics import Analyzer

# --- Visualisierungs-Layer ---
from .visualizer import (
    get_pie_chart, 
    get_stash_map,  
    get_theft_chart
)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
manager = StashManager()

@app.route('/')
def index():
    """
    Rendert das Haupt-Dashboard (Startseite)
    
    Ablauf:
    1. Lädt den aktuellen Datenbestand aus dem JSON-Speicher
    2. Generiert dynamische Diagramme (Torte, Karte) mittels Matplotlib
    3. Übergibt Daten und Bilder an das HTML-Template
    
    Returns:
        Rendered HTML Template 'index.html'.
    """
    stashes = manager.get_stashes()
    
    # 1. Diagramme erstellen
    pie_image = get_pie_chart(stashes)
    map_image = get_stash_map(stashes)
    
    return render_template('index.html', 
                           stashes=stashes, 
                           pie_image=pie_image, 
                           map_image=map_image)

@app.route('/analyze')
def analyze_data():
    """
    Führt die wissenschaftliche Analyse und den Performance-Benchmark durch.
    
    Hier passiert der Kern des Experiments:
    1. Fachliche Analyse: Reicht der Vorrat für den Winter? 
    2. Technischer Benchmark: Messung von Python vs. NumPy Laufzeiten auf den echten Daten
    
    Returns:
        Rendered HTML Template 'analysis.html' mit statistischen Kennzahlen
    """
    stashes = manager.get_stashes()
    
    # 1. Fachliche Simulation (Business Logic Layer)
    # Berechnet Soll/Ist-Bestände, Verluste und Zinseszins-Prognosen
    (is_enough, total_raw, lost, total_real, needed, 
     future_val, profit) = Analyzer.analyze_real_data(stashes)

    # Visualisierung des Diebstahls erstellen
    theft_chart = get_theft_chart(total_real, total_raw)

    # 2. Performance-Messung (Technical Layer)
    # Startet den Vergleichsalgorithmus (SISD vs SIMD) auf dem aktuellen Dataset
    perf_stats = Analyzer.run_performance_comparison(stashes)

    return render_template('analysis.html', 
                           # Fachliche KPIs
                           is_enough=is_enough, 
                           total_nuts=total_raw,
                           loss=lost,
                           real_stock=total_real,
                           needed=needed,
                           future_val=future_val, 
                           profit=profit,
                           theft_chart=theft_chart,
                           # Technische Benchmark-Daten
                           stats=perf_stats)

@app.route('/add', methods=['POST'])
def add_random():
    """
    Fügt eine kleine Menge (5 Stück) neuer Verstecke hinzu
    Dient zur manuellen Erweiterung der Datenbasis
    """
    new_data = generate_dummy_data(5)
    current = manager.get_stashes()

    # Fortlaufende ID vergeben
    last_id = current[-1].id if current else 0
    
    for i, s in enumerate(new_data):
        s.id = last_id + i + 1
        manager.add_stash(s)
    
    manager.save_data()
    return redirect(url_for('index'))

@app.route('/add_bulk', methods=['POST'])
def add_bulk():
    """
    Massendaten-Generator (+1000 Verstecke)
    
    Wichtig für den wissenschaftlichen Teil:
    Ermöglicht das schnelle Erzeugen von "Big Data", um den Performance-Vorteil
    von Vektorisierung (NumPy) sichtbar zu machen.
    """
    count = 1000
    new_data = generate_dummy_data(count)
    current = manager.get_stashes()
    last_id = current[-1].id if current else 0
    
    for i, s in enumerate(new_data):
        s.id = last_id + i + 1
        manager.add_stash(s)
    
    manager.save_data()
    return redirect(url_for('index'))

@app.route('/reset')
def reset_db():
    """
    Setzt die Datenbank zurück (Löscht alle Einträge)
    Ermöglicht die Wiederholbarkeit des Experiments
    """
    manager.stashes = []
    manager.save_data()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🌍 Starte Webserver auf http://127.0.0.1:5000")
    # debug=True erlaubt Live-Reloading bei Code-Änderungen
    app.run(debug=True, use_reloader=False, port=5000)