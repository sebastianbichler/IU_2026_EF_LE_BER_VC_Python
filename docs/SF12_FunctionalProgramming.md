### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Thema 12: Funktionales Programmieren & Lazy Evaluation

### 1. Einleitung & Kontext

Wir beschäftigen uns mit einem Paradigmenwechsel: weg vom imperativen „Schritt-für-Schritt“-Befehl hin zur deklarativen
Beschreibung von Datenströmen. Python wird oft als rein objektorientierte Sprache wahrgenommen, ist aber tatsächlich *
*multi-paradigmatisch**. Besonders die funktionale Programmierung (FP) hat Einzug in den Python-Alltag gehalten, da sie
oft zu kürzerem, eleganterem und weniger fehleranfälligem Code führt.

Ein Kernkonzept ist hierbei die **Lazy Evaluation** (verzögerte Auswertung). Anstatt eine Liste mit einer Million
Elementen sofort im Speicher zu erstellen (Eager Evaluation), erstellen wir eine „Vorschrift“, wie die Elemente bei
Bedarf erzeugt werden sollen.

- **C# Analogie:** Das Pendant in C# ist **LINQ (Language Integrated Query)**. Ein `IEnumerable` mit `Where` und
  `Select` verhält sich fast identisch zu Pythons Generatoren.
- **Ziele:** Unveränderlichkeit (Immutability), Funktionen als „First-Class Citizens“ und massive Speichereinsparung.

---

### 2. Wissenschaftliche Fragestellung

> *"Analyse der Speicherkomplexität und Laufzeit-Charakteristika von Generator-Pipelines: Eine Untersuchung der
Effizienz von Lazy Evaluation gegenüber List-Comprehensions bei der Verarbeitung von High-Velocity Telemetriedaten."*

**Kernfokus:** Wie verändert sich der Memory-Footprint, wenn wir Datenströme nicht als Kollektionen, sondern als
Iteratoren behandeln?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *Structure and Interpretation of Computer Programs* (Abelson & Sussman) / *PEP 255 (Simple
Generators)*.

In der Informatik erlaubt FP das Prinzip der **Referenziellen Transparenz**: Eine Funktion liefert bei gleichem Input
immer den gleichen Output und hat keine Seiteneffekte. Python implementiert FP-Elemente primär durch:

1. **Lambda-Funktionen:** Anonyme Einzeiler.
2. **Higher-Order Functions:** Funktionen wie `map()`, `filter()` und `reduce()`, die Funktionen als Argumente nehmen.
3. **Generatoren (`yield`):** Funktionen, die ihren Zustand „einfrieren“ und später genau dort weitermachen können.

---

### 4. Code-Demonstration (Notebook-Stil)

Wir verarbeiten Sensordaten der „Elephant Memory Cloud“ (z. B. Herzfrequenz-Daten), um Ausreißer zu finden.

#### Schritt 1: Imperativ vs. Funktional (Lambda, Map, Filter)

Python

```python
data = [45, 52, 110, 48, 125, 50, 47]  # Herzfrequenz in bpm

# Imperativ:
high_heart_rates = []
for x in data:
    if x > 100:
        high_heart_rates.append(x)

# Funktional:
high_heart_rates_fp = list(filter(lambda x: x > 100, data))
print(f"Alarme bei: {high_heart_rates_fp}")
```

#### Schritt 2: Der Speicher-Gigant (Eager vs. Lazy)

Wir vergleichen eine List-Comprehension mit einer Generator-Expression.

Python

```python
import sys

# Eager: Erstellt sofort eine Liste mit 1 Mio. Quadratzahlen im RAM
eager_list = [x ** 2 for x in range(1_000_000)]

# Lazy: Erstellt nur ein Generator-Objekt (den "Bauplan")
lazy_gen = (x ** 2 for x in range(1_000_000))

print(f"Speicher Liste: {sys.getsizeof(eager_list) / 1024 / 1024:.2f} MB")
print(f"Speicher Generator: {sys.getsizeof(lazy_gen)} Bytes")

# Erst beim Iterieren werden die Werte berechnet:
print(next(lazy_gen))
print(next(lazy_gen))
```

#### Schritt 3: Custom Generatoren mit `yield`

Dies ist die mächtigste Form der Lazy Evaluation.

Python

```python
def stream_elephant_sensor(sensor_id):
    """Simuliert einen endlosen Datenstrom eines Sensors."""
    val = 50
    while True:
        val += 1  # Simuliere Messung
        yield {"id": sensor_id, "val": val}
        if val > 55: break  # Demo-Stopp


for measurement in stream_elephant_sensor("E_001"):
    print(f"Empfangen: {measurement}")
```

---

### 5. Zusammenfassung

| **Merkmal**       | **Imperativ (Listen)**   | **Funktional (Generatoren)**     |
|:------------------|:-------------------------|:---------------------------------|
| **Speicher**      | Hoch (alle Daten im RAM) | Minimal (nur 1 Element im RAM)   |
| **Zustand**       | Explizit (Variablen)     | Implizit (Iterator-State)        |
| **Unendlichkeit** | Nicht möglich            | Problemlos (Infinite Streams)    |
| **Syntax**        | Schleifen (for/while)    | Map/Filter/Yield/Comprehensions  |
| **C# Analogie**   | `List<T>`, `Array`       | `IEnumerable<T>`, `yield return` |

---

### Anwendung im Projekt "Elephant Memory Cloud"

In der Cloud-Architektur nutzen wir funktionale Pipelines für das **Log-Processing**. Anstatt Gigabytes an Logfiles der
Sensoren komplett einzulesen, öffnen wir einen Dateistream als Generator. Jede Zeile durchläuft eine Kette von
`filter` (nur Fehler finden) und `map` (Zeitstempel konvertieren), bevor sie in der Datenbank landet.
Der Vorteil: Der RAM-Verbrauch bleibt konstant bei wenigen Kilobytes, egal ob das Logfile 1 MB oder 100 GB groß ist.

> **Merksatz für Studierende:** "Denken Sie nicht in Eimern (Listen), sondern in Rohren (Generatoren). Ein Rohr
> transportiert das Wasser (Daten) fließend, anstatt es in einem riesigen Becken zu stauen, das irgendwann überläuft."

---
