import matplotlib
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def get_pie_chart(stashes):
    """Erstellt ein Tortendiagramm der Nuss-Arten."""
    if not stashes:
        return None

    # Daten zählen
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
    
    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()

def get_stash_map(stashes):
    """Erstellt eine Scatter-Plot Karte (X/Y Koordinaten)."""
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
    """Zeigt Soll (Total) vs Ist (Real) Bestand."""
    labels = ['Gesammelt (Soll)', 'Verfügbar (Ist)']
    values = [total_raw, real_stock]
    colors = ['#95a5a6', "#b2e094"]

    plt.figure(figsize=(5, 3))
    bars = plt.bar(labels, values, color=colors)
    plt.ylabel('Anzahl Nüsse')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{int(yval)}", va='bottom', ha='center')

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    
    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()