
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

Nach dem Start der Anwendung öffnet sich die Benutzeroberfläche im Browser. Dort kann ein Zielknoten ausgewählt werden, während der Startknoten fest auf das Postamt gesetzt ist und nicht verändert werden kann. Durch Klick auf „Lieferung starten“ wird die Berechnung ausgelöst. Anschließend wird der kürzeste Pfad vom Postamt zum gewählten Zielknoten sowie die Gesamtkosten der Route angezeigt. Zusätzlich wird ein Diagramm dargestellt, das die Laufzeiten von CPython, Numba und PyPy miteinander vergleicht.

---

