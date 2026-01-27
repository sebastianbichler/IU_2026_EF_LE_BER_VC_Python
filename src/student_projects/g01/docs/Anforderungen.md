# Anforderungen – FoxExpress

### Funktional

## 🟥 Must Have


1. **Kürzesten Weg berechnen (Dijkstra)**
   - Das System muss zwischen zwei Knoten den kürzesten Pfad berechnen können.

2. **Benchmark-Funktion für CPython, PyPy und Numba**
   - Das System muss identische Routenberechnungen unter  
     **CPython**, **PyPy** und **Numba** ausführen und die Laufzeiten messen.

3. **Zeitmessung und Vergleich der Laufzeiten**
   - Die Ausführungszeiten müssen gemessen, gespeichert und vergleichend dargestellt werden.

---

## 🟧 Should Have


4. **Lieferungen anlegen und verwalten**
   - Benutzer können Lieferungen mit Start- und Zielknoten anlegen und bearbeiten.

5. **Auswahl der Ausführungsumgebung**
   - Benutzer sollen auswählen können, ob ein Benchmark unter CPython, PyPy oder Numba ausgeführt wird.

---

## 🟨 Could Have


6. **Paketstatus-Tracking**
   - Verwaltung von Status wie Eingegangen, Unterwegs, Zugestellt.

7. **Express-Zuschläge berechnen**
   - Berechnung zusätzlicher Kosten abhängig von der Gefährlichkeit der Route.
   
8. **Empfänger-Präferenzen speichern**
    - Speicherung, ob Pakete versteckt oder persönlich übergeben werden sollen.

9. **Interaktive Graph-Eingabe**
    - Benutzer können eigene Graphen definieren.

10. **Export der Ergebnisse**
    - Export der Benchmark-Ergebnisse als Datei (z.B. CSV).

---

### Nicht-funktional

1. **Trennung von GUI und Logik**
   - Routing- und Benchmark-Code sollen unabhängig von der Streamlit-GUI implementiert sein.

2. **Reproduzierbarkeit der Messungen**
   - Gleiche Eingaben sollen zu vergleichbaren Messergebnissen führen.
