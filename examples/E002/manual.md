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

Das direkte Einbetten von Matplotlib-Diagrammen in Flask-Webseiten, ohne sie zwischenzuspeichern, funktioniert über die Umwandlung des Bildes in einen **Base64-String**.

So geht's Schritt für Schritt:

### Schritt 1: Benötigte Module installieren

Stelle sicher, dass alle diese Pakete installiert sind (wenn nicht: `pip install matplotlib pandas flask base64 io`)

---

### Schritt 2: Die Flask-App (`app.py`) vorbereiten

Hier erzeugen wir das Diagramm und konvertieren es.

```python
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Zentraler Datenlader (wie in shared/data_utils.py)
def load_iris_data():
    try:
        # Versuche, die DB zu laden
        import sqlite3
        conn = sqlite3.connect("data/iris.sqlite")
        df = pd.read_sql("SELECT * FROM iris", conn)
        conn.close()
    except Exception:
        # Fallback auf CSV, falls DB nicht gefunden oder Fehler
        df = pd.read_csv("data/iris.csv")
    return df

@app.route('/')
def home():
    df = load_iris_data()

    # Beispiel: Mittelwerte pro Spezies berechnen
    avg_sepal_length_by_species = df.groupby('species')['sepal_length'].mean().reset_index()

    # Diagramm erstellen (Matplotlib)
    # Wichtig: fig, ax = plt.subplots() vor dem Plotten!
    fig, ax = plt.subplots(figsize=(8, 4)) # Größe des Diagramms
    ax.bar(avg_sepal_length_by_species['species'], avg_sepal_length_by_species['sepal_length'], color=['skyblue', 'lightcoral', 'lightgreen'])
    ax.set_title('Average Sepal Length by Species')
    ax.set_xlabel('Species')
    ax.set_ylabel('Average Sepal Length (cm)')
    
    # --- Hier beginnt der "Trick": Diagramm in Base64 umwandeln ---
    
    # 1. Diagramm in einen Speicher-Puffer schreiben (nicht auf die Festplatte)
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight') # 'tight' entfernt unnötigen Weißraum
    img_buffer.seek(0) # Cursor an den Anfang des Puffers setzen
    
    # 2. Den Inhalt des Puffers in Base64 umwandeln
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
    
    # 3. Den Puffer schließen und das Matplotlib-Figure-Objekt leeren
    img_buffer.close()
    plt.close(fig) # Sehr wichtig, um Speicherlecks zu vermeiden!
    
    # Flask rendert das HTML-Template und übergibt den Base64-String
    return render_template("index.html", plot_url=f"data:image/png;base64,{img_base64}")

if __name__ == '__main__':
    app.run(debug=True)

```

---

### Schritt 3: Das HTML-Template (`templates/index.html`) anpassen

Hier betten wir den empfangenen Base64-String als Bild ein.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iris Data Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Iris Data Visualization</h1>
    
    <p>This plot shows the average sepal length for different Iris species.</p>
    
    <img src="{{ plot_url }}" alt="Average Sepal Length Plot">
    
    <p>Data provided by the classic Iris dataset.</p>
</body>
</html>

```

---

### Wie es funktioniert (für deine Erklärung an die Studierenden):

1. **`io.BytesIO()`**: Dies ist wie eine "virtuelle Datei" im Arbeitsspeicher deines Computers. Matplotlib kann in diese schreiben, als wäre es eine normale PNG-Datei.
2. **`fig.savefig(img_buffer, format='png')`**: Statt `fig.savefig('plot.png')` speichern wir direkt in diesen Speicher-Puffer.
3. **`img_buffer.seek(0)`**: Nach dem Schreiben steht der "Schreibkopf" am Ende des Puffers. `seek(0)` setzt ihn wieder an den Anfang, damit wir alles von dort lesen können.
4. **`base64.b64encode(...).decode('utf-8')`**: Der Binärinhalt des Bildes wird in einen Text-String umgewandelt (`b64encode`). `.decode('utf-8')` wandelt diesen binären String in einen normalen Python-String, den HTML lesen kann.
5. **`data:image/png;base64,...`**: Das ist das spezielle HTML-Format für direkt eingebettete Bilder. Der Browser weiß, dass er den folgenden Base64-Text als PNG-Bild interpretieren soll.
6. **`plt.close(fig)`**: Extrem wichtig! Matplotlib behält Diagramme im Speicher. Wenn du Hunderte von Anfragen an deine Flask-App hast, würde der Speicher überlaufen. `plt.close()` räumt auf.

--

## Vorteile für die Lehrveranstaltung:

* Zeigt eine moderne Art der Web-Integration.
* Keine temporären Dateien auf dem Server (gut für Performance und Sicherheit).
* Demonstriert den Umgang mit Binärdaten und Kodierungen.

---

## Nächste mögliche Schritte 
- Einbinden von nicht nur statisches Diagrammen, sondern interaktiver Plots (z.B. mit Plotly oder Bokeh) in Flask? Das wäre der nächste Level für die Visualisierung.
- ...oder das Hinzufügen von Benutzer-Input, um verschiedene Analysen dynamisch zu generieren!
- Deployment der Flask-App auf einem Cloud-Dienst wie Heroku oder AWS.
- Integration von Machine Learning Modellen mit Scikit-learn oder TensorFlow in die Web-App.
- Erweiterung der App um eine REST-API, um Daten programmgesteuert abzurufen oder zu senden.
- Nutzung von Docker zur Containerisierung der Flask-App für einfaches Deployment und Skalierung.
- Implementierung von Benutzer-Authentifizierung und -Autorisierung für den Zugriff auf bestimmte Daten oder Funktionen.
- Einbindung von Datenbanken (z.B. PostgreSQL, MongoDB) zur Speicherung und Verwaltung größerer Datensätze.
- Erstellung von Dashboards mit Flask und Plotly Dash für interaktive Datenvisualisierungen.
- Automatisierung von Tests für die Flask-App mit pytest und Flask-Testing.
- Optimierung der Performance der Flask-App durch Caching (z.B. mit Flask-Caching).
- Verwendung von Websockets (z.B. mit Flask-SocketIO) für Echtzeit-Datenaktualisierungen in der App.
- Integration von CI/CD-Pipelines (z.B. mit GitHub Actions) für automatisiertes Testing und Deployment der Flask-App.
- Erstellung von benutzerdefinierten Jinja2-Filtern für die Datenformatierung in den HTML-Templates.
- Nutzung von Flask-Blueprints zur Modularisierung der App für größere Projekte.
- Implementierung von Internationalisierung (i18n) und Lokalisierung (l10n) für mehrsprachige Unterstützung in der App.
- Einbindung von Frontend-Frameworks (z.B. React, Vue.js) für eine verbesserte Benutzeroberfläche.
- Verwendung von Flask-Admin zur schnellen Erstellung von Admin-Oberflächen für die Datenverwaltung.
- Analyse und Visualisierung von Zeitreihendaten mit Pandas und Matplotlib in der Flask-App.
- Integration von Geodaten und Kartenvisualisierungen (z.B. mit Folium) in die Flask-App.
- Erstellung von Berichten im PDF-Format (z.B. mit ReportLab) basierend auf den Analysen in der Flask-App.
- Nutzung von Flask-Mail zum Versenden von Analyseberichten per E-Mail.
- Implementierung von Hintergrundaufgaben (z.B. mit Celery) für langwierige Datenverarbeitungsprozesse.
- Einbindung von OAuth2 für die Authentifizierung über Drittanbieter (z.B. Google, Facebook).
- Erstellung von benutzerdefinierten Fehlerseiten (z.B. 404, 500) für eine bessere Benutzererfahrung.
- Nutzung von Flask-Migrate zur Verwaltung von Datenbankschemata und Migrationen.
- Implementierung von Rate Limiting (z.B. mit Flask-Limiter) zum Schutz der App vor Missbrauch.
- Erstellung von API-Dokumentationen (z.B. mit Swagger) für die Flask-App.
- Integration von Logging (z.B. mit Flask-Logging) zur Überwachung und Fehlerbehebung der App.
- Nutzung von Flask-Security zur Implementierung von Sicherheitsfunktionen wie Passwort-Hashing und Rollenmanagement.
- Erstellung von Unit-Tests für die Flask-Routen und Funktionen zur Sicherstellung der Codequalität.
- Implementierung von Webhooks zur Integration mit anderen Diensten und Anwendungen.
- Data Science Workflows automatisieren mit Airflow oder Prefect in Verbindung mit der Flask-App.

---

