"""
Modul für die Datenvisualisierung (View Layer).

Dieses Modul ist verantwortlich für die Generierung von statistischen Grafiken.
Es nutzt die Bibliothek 'Matplotlib', um Diagramme serverseitig zu erstellen
und diese als Base64-codierte Strings direkt an das Frontend zu senden.

Technischer Hinweis:
Um Konflikte zwischen dem Webserver (Flask) und der GUI-Bibliothek (Tkinter)
zu vermeiden, wird das 'Agg' Backend verwendet.
"""
import matplotlib
# WICHTIG: Setzt das Backend auf 'Agg' (Anti-Grain Geometry).
# Dies verhindert, dass Matplotlib versucht, ein Fenster zu öffnen, was
# in einer Server-Umgebung (ohne Bildschirm) zum Absturz führen würde.
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def get_pie_chart(stashes):
    """
    Erstellt ein Tortendiagramm zur Analyse der Verteilung (Deskriptive Statistik).
    
    Zeigt die prozentuale Verteilung der Nuss-Arten (nut_type) im Lager.
    
    Args:
        stashes (list): Liste der Datenobjekte.
        
    Returns:
        str: Base64-String des Bildes (oder None, falls keine Daten).
    """
    if not stashes:
        return None

    # Datenaggregation mittels NumPy für Effizienz
    types = [s.nut_type for s in stashes]
    unique_types, counts = np.unique(types, return_counts=True)

    # Plot erstellen
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=unique_types, autopct='%1.1f%%', startangle=140, colors=["#cd853f", "#8b4513", "#d2691e", "#f4a460"])
    
    # Als Bild speichern
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close() # Wichtig: Speicher freigeben
    img.seek(0)
    
    # Konvertierung zu Base64 für direkte Einbettung in HTML
    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()

def get_stash_map(stashes):
    """
    Erstellt einen Scatter-Plot zur geografischen Analyse.
    
    Visualisiert die X/Y-Koordinaten der Verstecke. Die Größe der Punkte
    korreliert mit der Menge der gelagerten Nüsse.
    """
    if not stashes:
        return None

    x_coords = [s.x for s in stashes]
    y_coords = [s.y for s in stashes]
    sizes = [s.amount * 2 for s in stashes] # Größe je nach Menge

    plt.figure(figsize=(6, 4))
    plt.scatter(x_coords, y_coords, s=sizes, c='#27ae60', alpha=0.6, edgecolors='black')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("X-Koordinate")
    plt.ylabel("Y-Koordinate")
    plt.xlim(0, 100)
    plt.ylim(0, 100)

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)

    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()

def get_theft_chart(real_stock, total_raw):
    """
    Erstellt ein Balkendiagramm für den Soll-Ist-Vergleich.
    Vergleicht den Brutto-Bestand (Gesammelt) mit dem Netto-Bestand (nach Diebstahl).
    """
    labels = ['Gesammelt (Soll)', 'Verfügbar (Ist)']
    values = [total_raw, real_stock]
    colors = ['#95a5a6', "#b2e094"]

    plt.figure(figsize=(5, 3))
    bars = plt.bar(labels, values, color=colors)
    plt.ylabel('Anzahl Nüsse')

    # Werte direkt in die Balken schreiben
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{int(yval)}", va='bottom', ha='center')

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    
    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()