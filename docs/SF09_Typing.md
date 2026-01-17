### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---
Thema 9: Typisierung – Gradual Typing & MyPy

### 1. Einleitung & Kontext

Einer der größten Kritikpunkte an Python in großen Enterprise-Umgebungen war lange Zeit die fehlende Typsicherheit. In
C# ist ein `int` immer ein `int`, und der Compiler verweigert den Dienst, wenn wir versuchen, eine Zeichenfolge darin zu
speichern. Python hingegen ist von Natur aus **dynamisch typisiert** („Duck Typing“).

Mit der Einführung von **Type Hints** (PEP 484) hat Python jedoch das Konzept des **Gradual Typing** übernommen. Das
bedeutet:

- Wir *können* Typen definieren, müssen es aber nicht.
- Die Typen werden zur Laufzeit vom Interpreter ignoriert (Type Erasure).
- Externe Tools wie **MyPy** oder **Pyright** nutzen diese Informationen, um Fehler zu finden, *bevor* der Code
  ausgeführt wird.

In der **Elephant Memory Cloud** hilft uns dies, bei tausenden Codezeilen den Überblick über komplexe Datenstrukturen zu
behalten.

---

### 2. Wissenschaftliche Fragestellung

> *"Auswirkungen von Gradual Typing auf die Fehlerrate und Wartbarkeit in heterogenen Software-Systemen: Eine empirische
Untersuchung von MyPy-gestützter statischer Analyse gegenüber der strikten Typprüfung in C#."*

**Kernfokus:** Reduziert die nachträgliche Typisierung die Anzahl der Laufzeitfehler (AttributeErrors), ohne die
Agilität der dynamischen Entwicklung zu opfern?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *The Theory of Type Hints* (Guido van Rossum et al.) / *Gradual Typing for Functional Languages* (
Siek & Taha).

Die Forschung unterscheidet zwischen **Nominal Typing** (wie in C#, wo die Vererbungshierarchie zählt) und **Structural
Typing** (in Python via `Protocols`). Python erlaubt es, Systeme schrittweise („gradual“) zu migrieren. Ein Projekt kann
zu 10% typisiert sein; MyPy prüft nur diese 10% und lässt den Rest dynamisch. Das ist ein fundamentaler Unterschied zum
„Alles-oder-nichts“-Ansatz von C#.

---

### 4. Code-Demonstration (Notebook-Stil)

Wir simulieren ein Modul zur Verarbeitung von Sensordaten unserer Elefanten.

#### Schritt 1: Das Problem (Dynamik ohne Netz)

Python

```python
def process_weight(weight):
    # Erwartet eine Zahl, aber was passiert bei einem String?
    return weight * 0.453592  # Umrechnung lbs in kg


print(process_weight(100))  # Funktioniert
print(process_weight("100"))  # Semantischer Fehler: Produziert '100100100...'
```

#### Schritt 2: Gradual Typing mit Type Hints

Wir fügen Typ-Annotationen hinzu. Wichtig: Python führt dies trotzdem aus! Der Fehler wird erst durch einen statischen
Checker (MyPy) sichtbar.

Python

```python
from typing import List, Optional, Union


def process_elephant_data(
        name: str,
        age: int,
        gps_coords: Optional[List[float]] = None
) -> str:
    if gps_coords:
        return f"Elefant {name} ({age}) ist bei {gps_coords}"
    return f"Elefant {name} hat keine GPS-Daten."

# MyPy würde hier einen Fehler melden:
# process_elephant_data("Tuffi", "unbekannt")
```

#### Schritt 3: Statische Analyse simulieren (Duck Typing vs. Protocols)

In C# nutzen wir `Interfaces`. In Python nutzen wir `Protocols` (Structural Typing), um zu sagen: „Es ist mir egal, was
du bist, solange du eine Methode `track()` hast.“

Python

```python
from typing import Protocol


class Trackable(Protocol):
    def track(self) -> str: ...


class GPSChip:
    def track(self) -> str:
        return "GPS-Signal empfangen"


class Camera:
    def track(self) -> str:
        return "Bildanalyse aktiv"


def monitor_device(device: Trackable):
    print(device.track())


monitor_device(GPSChip())
monitor_device(Camera())  # Funktioniert, da die Struktur passt (Structural Typing)
```

---

### 5. Zusammenfassung für die Folien

| **Merkmal**       | **Python (Gradual Typing)**            | **C# (Static Typing)**                |
|-------------------|----------------------------------------|---------------------------------------|
| **Prüfzeitpunkt** | Zur Entwicklungszeit (externes Tool)   | Zur Kompilierzeit (Compiler)          |
| **Laufzeit**      | Typen werden ignoriert (kein Overhead) | Typen sind im Bytecode fest verankert |
| **Flexibilität**  | Hoch (Mischbetrieb möglich)            | Gering (Alles muss typisiert sein)    |
| **Typ-System**    | Primär Structural (Protocols)          | Primär Nominal (Interfaces)           |

---

### Anwendung im Projekt "Elephant Memory Cloud"

In der Cloud-Infrastruktur nutzen wir MyPy, um sicherzustellen, dass die JSON-Antworten der Sensoren korrekt in unsere
Datenklassen (`Pydantic Models`) überführt werden. Während wir in der Prototyping-Phase schnell und dynamisch ohne Typen
arbeiten, „härten“ wir den Code für den Production-Einsatz, indem wir Type Hints hinzufügen und MyPy in die
CI/CD-Pipeline (GitHub Actions) integrieren.

> **Merksatz für Studierende:** "Type Hints in Python sind wie Kommentare, die man maschinell prüfen kann. Sie ändern
> nicht, wie der Code läuft, aber sie verhindern, dass man nachts um 3 Uhr wegen eines `TypeError` geweckt wird."

---
