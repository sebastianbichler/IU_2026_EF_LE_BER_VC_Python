### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Während C# und Java zwischen **Value Types (structs)** und **Reference Types (classes)** unterscheiden, um Performance
und Speicher zu optimieren, ist in Python **alles** ein Referenz-Objekt auf dem Heap.

Dennoch hat Python spezialisierte Werkzeuge entwickelt, um die Probleme von „schwerfälligen“ Klassen zu lösen:
**NamedTuples**, **Dataclasses** und das **`__slots__`**-Feature.

---

# Objektorientierung (OOP) – Part2: Effiziente Datenstrukturen – Dataclasses, Structs & Records

### 1. Einleitung & Kontext

In C# nutzen wir `struct`, um Heap-Allokationen zu vermeiden (Stack-Zuweisung), und `record` für unveränderliche
Datenträger mit eingebauter Vergleichslogik.
In Python gibt es keine echten "Value Types" auf dem Stack. Ein Python-Objekt hat normalerweise einen hohen Overhead,
weil es ein internes Dictionary (`__dict__`) mitschleppt, um dynamisch neue Attribute zur Laufzeit aufzunehmen.

Python löst den Wunsch nach „leichtgewichtigen Records“ auf drei Ebenen:

1. **Speicher-Optimierung:** `__slots__` (Das „struct“-Äquivalent für RAM-Effizienz).
2. **Boilerplate-Reduktion:** `dataclasses` (Das „record“-Äquivalent).
3. **Immutability:** `NamedTuple`.

---

### 2. Wissenschaftliche Fragestellung

> *"Analyse der Speicherallokation und Instanziierungsgeschwindigkeit: Eine Untersuchung von Python Dataclasses
mit __slots__ als Äquivalent zu C# Structs in hochperformanten Datenpipelines."*

---

### 3. Die Python-Lösungen im Detail

#### A. Das Problem: Der Klassen-Overhead

Standardmäßig verbraucht jede Klasseninstanz in Python viel RAM, weil sie flexibel sein muss.

```python
class Elephant:
    def __init__(self, name):
        self.name = name

# Jedes Objekt hat ein geheimes __dict__, das viel Speicher kostet.
```

#### B. Die Lösung für Speicher: `__slots__` (Ähnlich wie C# Struct-Effizienz)

Wenn wir `__slots__` definieren, verbieten wir Python das Erstellen des `__dict__`. Das Objekt wird starr, aber extrem
klein und schnell – fast wie ein **C++ struct**.

```python
class CompactElephant:
    __slots__ = ['name', 'age']  # Nur diese zwei Attribute sind erlaubt

    def __init__(self, name, age):
        self.name = name
        self.age = age
```

*Vorteil:* Bis zu 50% weniger Speicherverbrauch bei Millionen von Objekten in der "Elephant Memory Cloud".

#### C. Die Lösung für Records: `dataclasses` (Wie C# Records)

Eingeführt in Python 3.7 (PEP 557). Sie generieren automatisch `__init__`, `__repr__` (ToString), und
Vergleichsoperatoren (`==`).

Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)  # frozen=True macht es unveränderlich wie ein C# Record
class ElephantRecord:
    id: int
    name: str
    species: str = "Afrikanisch"  # Default-Werte


e1 = ElephantRecord(1, "Tuffi")
# e1.name = "Neuer Name" # Fehler! Dank frozen=True
```

---

### 4. Konstruktoren, Methoden und Destruktoren

Anders als einfache C-Structs sind Python Dataclasses vollwertige Klassen:

- **Konstruktoren:** Werden automatisch generiert. Mit `__post_init__` kann man Logik nach der Erstellung ausführen (
  Validierung).
- **Methoden:** Man kann ganz normal Methoden definieren.
- **Destruktoren:** `__del__` existiert, wird aber in Python selten genutzt (wegen des Garbage Collectors).

Python

```python
@dataclass
class SmartSensor:
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Sensorwert kann nicht negativ sein!")

    def calibrate(self):
        print(f"Kalibriere Sensor mit Wert {self.value}")
```

---

### 5. Der Zusammenhang mit ENUM

In C# sind Enums oft einfache `int`-Wrapper. In Python ist ein `Enum` eine Klasse. Sie lassen sich perfekt mit
Dataclasses kombinieren, um Typsicherheit zu garantieren.

Python

```python
from enum import Enum, auto


class Status(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    MAINTENANCE = auto()


@dataclass
class Tracker:
    device_id: str
    status: Status  # Hier nutzen wir das Enum als Typ-Hint


t = Tracker("GPS_123", Status.ACTIVE)

if t.status == Status.ACTIVE:
    print("Tracker sendet Daten...")
```

---

### 6. Zusammenfassung (Der Vergleich)

| Feature                 | C# / Java         | Python Äquivalent         | Charakteristik in Python                          |
|:------------------------|:------------------|:--------------------------|:--------------------------------------------------|
| **Leichtgewicht-Daten** | `struct`          | `__slots__`               | Verringert RAM-Overhead massiv.                   |
| **Daten-Container**     | `record`          | `@dataclass`              | Automatisiert Boilerplate (`Equals`, `ToString`). |
| **Unveränderlichkeit**  | `readonly record` | `@dataclass(frozen=True)` | Schützt vor versehentlichen Änderungen.           |
| **Konstanten**          | `enum`            | `Enum`-Klasse             | Mächtiger als in C#, da es Objekte sind.          |

---

### Anwendung im Projekt "Elephant Memory Cloud"

Warum ist das wichtig für uns?
Wenn wir die Migrationsdaten von 10.000 Elefanten über 10 Jahre speichern (Sekundentakt), haben wir Milliarden von
Datenpunkten.

1. Ein normales **Objekt** würde den Server-RAM sprengen.
2. Ein **Dictionary** wäre zu langsam und speicherintensiv.
3. Wir nutzen **Dataclasses mit `__slots__`**, um die Elefanten-Positionen speichereffizient zu halten, aber
   gleichzeitig die Bequemlichkeit von Methoden (z.B. `calculate_distance()`) zu haben.

> **Merksatz:** "Dataclasses sind für den Programmierer (weniger Tipparbeit), `__slots__` sind für den
> Computer (weniger Speicher). Kombiniert man beide, erhält man das Python-Äquivalent zu hocheffizienten C#-Records."

---
