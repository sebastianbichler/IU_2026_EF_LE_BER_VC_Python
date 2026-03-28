# Software Requirements – FoxPost

## 1. Funktionale Anforderungen

F1: Das System soll Paketdaten aus einer CSV-Datei einlesen können.

F2: Das System soll die eingelesenen Daten validieren und fehlerhafte Daten entfernen.

F3: Das System soll die Daten transformieren und bereinigen.

F4: Das System soll zusätzliche Felder berechnen, wie z. B. die Lieferdauer (`transit_hours`).

F5: Das System soll für jede Lieferung eine Route (`route_id`) generieren.

F6: Das System soll aggregierte Statistiken berechnen (z. B. Anzahl Pakete pro Route).

F7: Das System soll die verarbeiteten Daten im Parquet-Format speichern.

F8: Das System soll über die Kommandozeile gestartet werden können.

F9: Das System soll sowohl lokal als auch mit einem Dask-Cluster ausgeführt werden können.

---

## 2. Nicht-funktionale Anforderungen

NF1: Der Code soll übersichtlich, modular und wartbar sein.

NF2: Die Anwendung soll mit Python ausführbar sein.

NF3: Die Anwendung soll eine nachvollziehbare Dokumentation enthalten (README, Usage, Reflection).

NF4: Die Abhängigkeiten sollen in einer `requirements.txt` definiert sein.

NF5: Die Anwendung soll reproduzierbar ausführbar sein.

NF6: Die Anwendung soll grundlegende Tests enthalten (Unit- und Integrationstests).

---

## 3. Priorisierung

* Hoch: F1–F5 (Grundfunktionalität der Pipeline)
* Mittel: F6–F9 (Erweiterte Verarbeitung und Ausführung)
* Niedrig: Erweiterungsmöglichkeiten (z. B. Visualisierungen)
