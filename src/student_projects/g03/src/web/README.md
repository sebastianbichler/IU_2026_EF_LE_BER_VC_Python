# RabbitFarm Web (nur App)

Alle webrelevanten Teile der **App** liegen hier. Jupyter-Notebooks bleiben an ihrem ursprünglichen Ort (`g03/static/notebooks/`).

## Struktur

- **`main.py`** – Einstiegspunkt (ehemals run_web.py)
- **`app.py`** – Flask-App, Routen, Daten laden
- **`routes.py`** – Web-Routen
- **`templates/`**, **`static/css/`** – Vorlagen und Styles

## Starten

Von Projektroot **g03** aus:

```bash
python -m src.web.main
```

Die App läuft dann unter http://127.0.0.1:8080
