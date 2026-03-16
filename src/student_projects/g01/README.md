
## 1. Projekt aufsetzen

1. Terminal im Projektordner öffnen
2. Virtuelle Umgebung anlegen
3. Abhängigkeiten installieren
4. PyPy installieren
5. Streamlit-App starten

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. PyPy installieren

### Windows

1. PyPy3 für Windows herunterladen
2. Entpacken, z. B. nach:

```text
C:\tools\pypy3.11-vX\
```

3. Den vollständigen Pfad zur ausführbaren Datei merken, z. B.:

```text
C:\tools\pypy3.11-vX\pypy3.exe
```

4. Diesen Pfad später in der Streamlit-Seitenleiste eintragen.

---

## 3. Anwendung starten

```bash
streamlit run app.py
```

Danach öffnet sich die Anwendung im Browser.

---

