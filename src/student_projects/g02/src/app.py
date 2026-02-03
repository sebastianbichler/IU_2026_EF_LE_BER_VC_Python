from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import random
import os

# --- Eigene Module ---
from .manager import StashManager
from .generator import generate_dummy_data
from .analytics import Analyzer

# Import der Visualisierungen
from .visualizer import (
    get_pie_chart, 
    get_stash_map,  
    get_theft_chart
)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
manager = StashManager()

@app.route('/')
def index():
    """Startseite: Zeigt Tabelle, Tortendiagramm und Karte."""
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
    stashes = manager.get_stashes()
    
    (is_enough, total_raw, lost, total_real, needed, 
     future_val, profit) = Analyzer.analyze_real_data(stashes)
    
    expected = int(total_raw * 1.1) if total_raw > 0 else 10
    theft_chart = get_theft_chart(total_real, total_raw)

    
    perf_stats = Analyzer.run_performance_comparison(stashes)

    return render_template('analysis.html', 
                           is_enough=is_enough, 
                           total_nuts=total_raw,
                           loss=lost,
                           real_stock=total_real,
                           needed=needed,
                           future_val=future_val, 
                           profit=profit,
                           theft_chart=theft_chart,
                           stats=perf_stats)

@app.route('/add', methods=['POST'])
def add_random():
    """Fügt 5 neue Verstecke hinzu."""
    new_data = generate_dummy_data(5)
    current = manager.get_stashes()
    last_id = current[-1].id if current else 0
    
    for i, s in enumerate(new_data):
        s.id = last_id + i + 1
        manager.add_stash(s)
    
    manager.save_data()
    return redirect(url_for('index'))

@app.route('/add_bulk', methods=['POST'])
def add_bulk():
    
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
    """Löscht die Datenbank komplett."""
    manager.stashes = []
    manager.save_data()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🌍 Starte Webserver auf http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False, port=5000)