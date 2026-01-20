# Elephant Memory Cloud (Gedankenstütze)

## Projektübersicht

### Ziel des Projekts
Entwicklung eines Python-Prototyps als „digitales Gedächtnis"
- Verwaltung von Ereignissen, Stammbäumen und Wasserstellen
- Wissenschaftlicher Schwerpunkt: Memory Management und zyklische Garbage Collection in Python

### Rahmenbedingungen
- **Studiengang:** Duales Studium Informatik, 5. Semester
- **Gruppenarbeit:** 3 Personen
- **Vorkenntnisse:** Keine Python-Vorkenntnisse
- **Fokus:** Nachvollziehbarkeit statt Produktreife

## Kernfunktionen

### 1. Ereignisse indexieren
- Jahr
- Ort (Wasserstelle)
- Beteiligte Herden / Elefanten

### 2. Stammbäume verwalten und visualisieren
- Verwandtschaftsbeziehungen
- Graph mit möglichen Zyklen

### 3. Wasserstellen-Suche
- Basierend auf historischen Trockenzeiten
- Regelbasierte Logik (keine KI)

### 4. Erinnerungs-Bot
- Jahrestage
- Start von Migrationen
- Konsolenausgabe oder Logfile

## Wissenschaftlicher Schwerpunkt (TOPIC 1)

### Vergleich
- Reference Counting
- Cyclic Garbage Collection

### Problem
Zirkuläre Referenzen in Verwandtschaftsgraphen

### Ziel
- Nachweis von Memory Leaks ohne GC
- Messbarer Effekt des zyklischen Garbage Collectors

## Arbeitsteilung (3 Personen)

### Person A – Datenmodell & Memory
- Klassen: Elefant, Herde, Ereignis
- Erzeugen zyklischer Referenzen
- Memory-Messungen
- GC-Analyse & Dokumentation

### Person B – Logik & Suche
- Ereignis-Index
- Wasserstellen-Suche
- Erinnerungs-Bot
- Funktionale Tests

### Person C – Visualisierung
- Stammbäume als Graphen
- Diagramme für Memory-Auswertung
- Einfache CLI oder Minimal-UI

## Technologien & Tools

### Programmiersprache
- Python 3.11+

### Standardbibliothek
- `gc`
- `sys`
- `tracemalloc`
- `weakref`
- `datetime`
- `math`
- `heapq`

### Externe Bibliotheken (empfohlen)
- `networkx` (Graphen, Stammbäume)
- `matplotlib` (Visualisierung, Diagramme)

### Optionale Alternativen
- `objgraph` (Objektvisualisierung)
- `memory_profiler` (Speicheranalyse)
- `graphviz` (Graph-Darstellung)

## Datenmodellierung

### Objektorientierter Ansatz
- Reine Python-Objekte
- Bewusst erzeugte Zyklen:
  - Elefant ↔ Eltern / Kinder
  - Elefant ↔ Herde
  - Ereignis ↔ beteiligte Elefanten
- Keine ORM-Frameworks

## Wasserstellen-Suche
- Historische Ereignisdaten aus Trockenzeiten
- Vereinfachte Koordinaten
- Entfernung + Häufigkeit als Entscheidungsgrundlage
- Keine Machine-Learning-Verfahren

## Erinnerungs-Bot
- Zeitbasierte Trigger (Simulation)
- Ausgabe:
  - Konsole
  - Logfile
- Keine externen Messenger-Dienste

## Memory- & GC-Analyse

### Vorgehen
1. Aufbau großer zyklischer Objektgraphen
2. Entfernen von Referenzen
3. Beobachtung:
   - Speicherverbrauch
   - Anzahl Objekte
   - GC-Zyklen
4. Vergleich:
   - GC deaktiviert vs. aktiviert
5. Ergebnisse grafisch darstellen

## Projektstruktur (Vorschlag)

```
models/
memory/
search/
bot/
visualization/
data/
main.py
```

## Zeitplanung (Richtwert)

| Woche | Aufgaben |
|-------|----------|
| 1 | Python-Grundlagen, Setup |
| 2 | Datenmodelle |
| 3 | Ereignisse & Suche |
| 4 | Visualisierung |
| 5 | GC-Experimente |
| 6 | Messungen & Diagramme |
| 7 | Dokumentation |
| 8 | Puffer / Präsentation |

## Wichtige Hinweise

⚠️ **Hinweise zur Umsetzung:**
- Kein Cloud-Overengineering
- Keine KI / ML
- Fokus auf Messbarkeit und Nachweis
- GC nicht nur erklären, sondern experimentell belegen

## Ressourcen

- [Garbage Collection in Python](https://www.geeksforgeeks.org/python/garbage-collection-python/)
