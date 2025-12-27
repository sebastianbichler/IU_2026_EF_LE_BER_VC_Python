Ein Beispiel vom "manuellen" Verständnis hin zur professionellen Automatisierung und Bereitstellung.

Hier ist der systematische Leitfaden. Als Datensatz werden der klassische **"Iris"** und **"Titanic"** Datensatz verwendet, da diese als CSV online leicht verfügbar sind. 
Wir nutzen hier beispielhaft einen Datensatz über Verkaufszahlen oder Wetterdaten (CSV).

---

## Schritt 0: Datenquelle vorbereiten

In PyCharm kannst du die Datei einfach im Projektordner ablegen.

**Daten einlesen (Pandas Vorgriff für die Quelle):**

```python
import pandas as pd
# Online-Quelle:
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
df = pd.read_csv(url)
# Als lokale Sicherung speichern
df.to_csv("daten.csv", index=False)

```

*Tipp: PyCharm hat unten rechts einen Tab "Database". Dort kannst du eine SQLite-Datei einfach hineinziehen und wie in einem SQL-Manager betrachten.*

---

## Schritt 1: Python Basics (Ohne Pakete)

Hier zeigst du, wie mühsam es ohne Bibliotheken ist, um das Verständnis für Datentypen zu schärfen.

* **Lernziel:** `list`, `dict`, `str`, `float`, Loops.
* **Beispiel:** Datei manuell öffnen und Durchschnitt berechnen.

```python
with open("daten.csv", "r") as f:
    header = f.readline() # Header überspringen
    daten = []
    for line in f:
        spalten = line.strip().split(",")
        # Datentyp-Konvertierung (Cast)
        wert = float(spalten[0]) 
        daten.append(wert)

durchschnitt = sum(daten) / len(daten)
print(f"Datentyp: {type(daten)}, Durchschnitt: {durchschnitt}")

```

---

## Schritt 2: NumPy – Die Kraft der Vektorisierung

Zeige nun, wie man die Liste in ein Array umwandelt und warum das effizienter ist.

* **Lernziel:** `np.array`, Broadcasting, Performance.
* **Beispiel:**

```python
import numpy as np
np_daten = np.array(daten)
# Operation auf alle Elemente gleichzeitig (Broadcasting)
normalisierte_daten = (np_daten - np_daten.mean()) / np_daten.std()
print(f"NumPy Durchschnitt: {np_daten.mean()}")

```

---

## Schritt 3: Pandas – Tabellen-Power

Jetzt führst du DataFrames ein. Der Code wird kürzer und lesbarer.

* **Lernziel:** `DataFrame`, `head()`, `describe()`, Filtern.
* **Beispiel:**

```python
import pandas as pd
df = pd.read_csv("daten.csv")
# Schnelle Statistik
print(df.describe())
# Filtern: Alle Zeilen, wo die erste Spalte > Durchschnitt ist
gefiltert = df[df.iloc[:, 0] > df.iloc[:, 0].mean()]

```

---

## Schritt 4: Visualisierung (Matplotlib & Seaborn)

Vom nackten Plot zum schönen statistischen Diagramm.

* **Lernziel:** `fig, ax`, Scatterplots, Heatmaps.
* **Beispiel:**

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Matplotlib (Basis)
ax[0].plot(df.iloc[:, 0])
ax[0].set_title("Rohdaten Verlauf")

# Seaborn (Statistik)
sns.scatterplot(data=df, x=df.columns[0], y=df.columns[1], hue=df.columns[-1], ax=ax[1])
ax[1].set_title("Korrelation mit Seaborn")
plt.show()

```

---

## Schritt 5: SciPy – Wissenschaftliche Analyse

Hier zeigst du z.B. eine lineare Regression oder eine statistische Verteilung.

* **Lernziel:** Statistische Tests oder Linienanpassung.
* **Beispiel:**

```python
from scipy import stats
# Lineare Regression zwischen zwei Spalten
slope, intercept, r, p, std_err = stats.linregress(df.iloc[:, 0], df.iloc[:, 1])
print(f"Bestimmtheitsmaß (R²): {r**2}")

```

---

## Schritt 6: Die Flask Web-App

Wir bringen alles zusammen. Die App zeigt die Ergebnisse im Browser an.

1. **Struktur:**
* `app.py`
* `templates/index.html`


2. **`app.py`:**

```python
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    df = pd.read_csv("daten.csv")
    beschreibung = df.describe().to_html(classes="table table-striped")
    return render_template("index.html", table=beschreibung)

if __name__ == '__main__':
    app.run(debug=True)

```

3. **`templates/index.html`:**

```html
<!DOCTYPE html>
<html>
<head><title>Data Science App</title></head>
<body>
    <h1>Statistische Übersicht des Datensatzes</h1>
    <div> {{ table | safe }} </div>
</body>
</html>

```

---

### Dein Fahrplan für die Vorlesung:

1. **Live-Coding:** Starte mit der leeren Datei und installiere Pakete via `pip install pandas numpy matplotlib seaborn scipy flask`.
2. **Vergleich:** Zeige immer wieder den Unterschied zwischen dem manuellen Weg (Schritt 1) und den Paketen (Schritt 3).
3. **Deployment:** Starte am Ende die Flask-App und zeige den Studierenden, dass ihr Analyse-Modell nun eine "echte Software" ist.

**Soll ich dir für Schritt 6 (Flask) noch zeigen, wie du ein Diagramm als Bild direkt in die Webseite einbettest, ohne es vorher auf der Festplatte speichern zu müssen?**