### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

![Python Check](https://github.com/sebastianbichler/IU_2026_EF_LE_BER_VC_Python/actions/workflows/python-check.yml/badge.svg)

## Environment Setup (env, virtualenv)

1. Installiere Python 3.8 oder höher von https://www.python.org/downloads/

2. Installiere pip (Python Paket-Manager), falls nicht bereits vorhanden.

3. Erstelle ein virtuelles Environment (optional, aber empfohlen):

  ```bash

     python -m venv dlbdsipwp01_env

     source dlbdsipwp01_env/bin/activate  # Linux/Mac

     dlbdsipwp01_env\Scripts\activate     # Windows

  ```

Die Umgebung wird in der Regel über die IDE verwaltet.

---

## Modules

Use: pip install <module_name>, z.B.:

`pip install pandas numpy matplotlib seaborn scipy flask`.

Die Pakete können global installiert werden. Es wird jedoch empfohlen, ein virtuelles Environment zu verwenden.

- NumPy
- Pandas
    - pandas-stubs (für Typenunterstützung)
- Matplotlib
- Scikit-learn
- Seaborn
- SciPy
- PyTorch
- TensorFlow
- Keras
- Statsmodels
- Jupyter Notebook (notebook)
- JupyterLab
- Flask
- Django
- IPyWidgets

Verwende die folgende Datei `requirements.txt`, um alle Abhängigkeiten auf einmal zu installieren:

``` pip install -r requirements.txt ```

---

## Modul-Übersicht

| Bereich        | Modul                   | Tool                      | Zweck, Besonderheit                  |
|----------------|-------------------------|---------------------------|--------------------------------------|
| Numerik        | NumPy                   | Arrays & Matrizen         | Die Basis für fast alles.            |
| Tabellen       | Pandas                  | Daten-Manipulation        | Excel in Python                      |
| Statistik      | SciPy                   | Komplexe Berechnungen     | Integration, Optimierung, FFT.       |
| Statistik      | arviz                   | Bayesian Analysis         | Visualisierung und Diagnose.         |
| Statistik      | PyMC3                   | Bayesian Modeling         | Probabilistische Programmierung.     |
| Visualisierung | Matplotlib              | Grafiken & Plots          | Sehr mächtig, etwas sperrig.         |
| Stat. Visual.  | Seaborn                 | Schöne Grafiken           | Einfacher als Matplotlib.            |
| Workflow       | JupyterLab              | Interaktives Arbeiten     | Browser-IDE für Daten-Exploration.   |
| Deep Learning  | PyTorch,Neuronale Netze | Sehr flexibel             | Favorit der Forschung."              |
| Deep Learning  | TensorFlow              | Neuronale Netze           | Industriestandard von Google.        |
| ML-Einstieg    | Keras                   | Einfaches Deep Learning   | Nutzt TensorFlow im Hintergrund.     |
| Web (Klein)    | Flask                   | Web-Apps (leicht)         | Minimalistisch und flexibel.         |
| Web (Groß)     | Django                  | Web-Apps (komplett)       | Alles inklusive (Login, Admin etc.). |
| Statistik      | Statsmodels             | Statistische Modelle      | Regressionen, Zeitreihenanalyse.     |
| GUI            | IPyWidgets              | UI-Controls in Noteboooks | Verzicht auf Desktop- oder Web-UI    |

---

## Ordner-Struktur

- examples: Für Beispiele und Übungen
- data: Für Datensätze (CSV, Excel, etc.) (Daten gehören üblicherweise nicht in ein Repo, hier nur für Demos)
- src: Für gemeinsamen Code (Module, Funktionen) (shared code)
    - examples: Für Beispiele und Übungen
    - students_projects: Für Projekte der Studierenden nach dem Template
        - data: Datensatze auf Dateibasis
        - docs: Dokumentation (Markdown, Jupyter Notebooks)
        - src: Quellcode (Module, Skripte)
        - tests: Tests für den Quellcode

- tests: Für globale Tests (shared code)

**Jede Gruppe wird in ihrem eigenen Branch arbeiten und später mergen.**

---

## Best Practices

- Schreibe sauberen, gut dokumentierten Code.
- Verwende virtuelle Environments für jedes Projekt, um Abhängigkeitskonflikte zu vermeiden.
- Nutze Versionskontrolle (z.B. Git). Die Gruppen werden in einem eigenen Branch arbeiten und später mergen.
- Teste deinen Code regelmäßig.
- Halte deine Abhängigkeiten aktuell.
- Verwende Jupyter Notebooks für explorative Datenanalyse.
- Kommentiere deinen Code ausreichend.
- Folge den PEP 8 Stilrichtlinien für Python-Code.
- Nutze Logging anstelle von print() für Debugging und Informationsausgaben.
- Schreibe Unit-Tests für wichtige Funktionen und Module.
- Verwende aussagekräftige Variablennamen.
- Strukturiere deinen Code in Funktionen und Klassen.
- Dokumentiere deine Funktionen mit Docstrings.
- Nutze List Comprehensions für sauberen und effizienten Code.
- Vermeide globale Variablen, wenn möglich.
- Verwende Kontextmanager (with statement) für Dateioperationen.
- Optimiere die Performance nur bei Bedarf, nicht vorzeitig.
- Nutze Profiling-Tools, um Engpässe zu identifizieren.
- Halte dich an das DRY-Prinzip (Don't Repeat Yourself).
- Verwende weitere Design-Patterns, wo sinnvoll (gerade für Standardsituationen).
- Nutze Linter (z.B. ruff, flake8, pylint), um Codequalität zu gewährleisten.
- Committe regelmäßig und mit aussagekräftigen Nachrichten.
- Committe kleine Änderungen lokal und push nur funktionierenden Code (regelmäßig).
- Verwende Type Hints für bessere Lesbarkeit und Wartbarkeit.
  ```python

  def add(a: int, b: int) -> int:

      return a + b
  ```

---

## Nützliche Ressourcen

- [Python Package Index](https://pypi.org/)
- [Python Official Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [SciPy Documentation](https://docs.scipy.org/doc/scipy/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [TensorFlow Documentation](https://www.tensorflow.org/learn)
- [Keras Documentation](https://keras.io/)
- [Jupyter Documentation](https://jupyter.org/documentation)
- [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [Streamlit](https://pypi.org/project/streamlit/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Real Python Tutorials](https://realpython.com/)
- [Awesome Python](https://awesome-python.com/)

---

## Weitere Dokumente für das Projekt

- [Vorlesung](student_projects_part1.md)
- [Python-Schwerpunkte](lecture_topics.md)
- [Studentische Projekte](student_projects_part3.md)

---

## Code snippets

- **Pakete installieren**: `pip install package_name`
- **Abhängigkeiten speichern**:
  - `pip freeze > requirements.txt`
  - `python -m pip freeze | Set-Content -Path requirements.txt -Encoding utf8NoBOM`
- **Abhängigkeiten installieren**: `pip install -r requirements.txt`
- **Virtuelle Umgebung erstellen**: `python -m venv env_name`
- **Virtuelle Umgebung aktivieren**: `source env_name/bin/activate (Linux/Mac)` oder
  `env_name\Scripts\activate (Windows)`
- **Aktuelle virtuelle Umgebung anzeigen:** `which python (Linux/Mac)` oder `where python (Windows)`
- **Formatierung standardisieren**: `ruff format`
- **Code-Qualität prüfen**: `ruff check .`
- **Check line endings:** `git ls-files --eol`
- **Pre-Commit-Checks:** `pre-commit run --all-files`
- **Interaktive Python-Shell starten:** `python -m IPython`
- **Jupyter Notebook starten**: `jupyter notebook`
- **JupyterLab starten**: `jupyter lab`
- **Unit-Tests ausführen**: `python -m unittest discover tests`
- **Code mit Type Hints versehen**:
- **Git-Origin/Remote-Repository**:`git remote -v`
- **Default-Branch:** `git remote show origin`
- **Lokaler aktueller Branch:** `git branch --show-current`
- **Git-Branch erstellen**: `git checkout -b branch_name`
- **Änderungen committen**: `git commit -m "Commit message"`
- **Code pushen**: `git push origin branch_name`
- **Code fetch**: `git fetch origin branch_name`
- **Code pull**: `git pull origin branch_name`
- **Ziel-Branch wählen**: `git checkout main`
- **Code mergen**: `git merge branch_name`
- **Merge abbrechen (bei Fehlern)**: `git merge --abort`
- **Datei zu Git hinzufügen**: `git add file_name`
- **Alle Änderungen zu Git hinzufügen**: `git add .`
- **Pull-Request abrufen**: `git fetch origin pull/ID/head:lokaler-branch-name`
- **Git-Status anzeigen**: `git status`
- **Git-Log anzeigen**: `git log`
- **Einen Commit zurücksetzen**: `git reset --hard commit_hash`
