# Sloth’s Slow-Motion Hotel (DLBDSIPWP01)

## Projektbeschreibung
Dieses Projekt implementiert eine Hotel-Management-Software für "Sid Sloth". Ziel der Anwendung ist nicht Effizienz, sondern die **Maximierung der Langsamkeit**.
Die Software verwaltet Buchungen für Faultiere, berechnet Rabatte basierend auf Inaktivität (Bewegungs-Tracker) und sorgt mittels Design Patterns (State Pattern) für eine saubere Abbildung der Gast-Zustände.

**Wissenschaftlicher Fokus:** Structural & Behavioral Design Patterns in Python (Duck Typing, State Pattern).

---

## Setup & Installation

Voraussetzung: Python 3.10 oder höher.

1. **Repository klonen / öffnen**
2. **Virtuelle Umgebung erstellen & Abhängigkeiten installieren:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Ausführen**
   ```bash
   streamlit run src/app.py
   ```
   Die Anwendung ist unter [http://localhost:8501/](http://localhost:8501/) erreichbar
