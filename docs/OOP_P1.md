### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Die Objektorientierung (OOP) in Python unterscheidet sich philosophisch stark von Java oder C#, obwohl sie oberflächlich
ähnlich aussieht. Während C# und Java **"starr"** sind (die Klasse ist ein unveränderlicher Bauplan), ist in Python *
*alles ein Objekt** – auch die Klasse selbst.


---

# Objektorientierung (OOP) – Part1: Dynamik & Meta-Objekte

### 1. Einleitung & Kontext

In Java oder C# ist eine Klasse eine Schablone, die zur Kompilierzeit feststeht. In Python ist eine Klasse ein
**lebendiges Objekt** im Speicher, das zur Laufzeit modifiziert werden kann. Python folgt dem Prinzip des "**Duck Typing
**": Es ist weniger wichtig, welcher Klasse ein Objekt angehört, sondern vielmehr, welche Methoden es implementiert.

- **Instanziierung:** Python verzichtet auf das Schlüsselwort `new`. Man ruft die Klasse einfach wie eine Funktion auf.
- **Zustand:** Es wird strikt zwischen **Klassen-Attributen** (statisch) und **Instanz-Attributen** unterschieden.

---

### 2. Wissenschaftliche Fragestellung

> *"Analyse der Flexibilität von Meta-Objekt-Protokollen: Wie beeinflusst die dynamische Bindung von Attributen die
Integrität von Datenmodellen im Vergleich zur statischen Typisierung in C#?"*

**Kernfokus:** Wie verwaltet Python "statische" Informationen (Klassen-Attribute) und wie löst es Konflikte bei der
Mehrfachvererbung?

---

### 3. Wissenschaftlicher Hintergrund

**Konstruktoren:** In Python gibt es keinen Konstruktor im klassischen Sinne, sondern zwei Phasen: `__new__` (erstellt
das Objekt) und `__init__` (initialisiert das Objekt).

**Mehrfachvererbung:** Im Gegensatz zu C# oder Java erlaubt Python Mehrfachvererbung. Um das berüchtigte "Diamond
Problem" (wenn zwei Elternklassen dieselbe Methode implementieren) zu lösen, nutzt Python den **C3 Linearization
Algorithmus**, auch bekannt als **MRO (Method Resolution Order)**.

---

### 4. Code-Demonstration (Notebook-Stil)

In der "Elephant Memory Cloud" müssen wir die Anzahl der aktiven Elefanten-Tracker überwachen und verschiedene
Sensortypen kombinieren.

#### Schritt 1: Klassen-Attribute (Statische Variablen) & Instanziierung

Hier zeigen wir, wie man Objekte zählt – genau wie statische Variablen in Java/C#.

Python

```python
class ElephantTracker:
    # Klassen-Attribut (entspricht 'static' in C#)
    # Es gehört der Klasse, nicht der Instanz
    tracker_count = 0

    def __init__(self, device_id):
        # Instanz-Attribut (gehört dem einzelnen Objekt)
        self.device_id = device_id

        # Zugriff auf das Klassen-Attribut zum Zählen
        ElephantTracker.tracker_count += 1
        print(f"Tracker {self.device_id} wurde aktiviert.")

    @classmethod
    def get_active_count(cls):
        # Klassen-Methode (entspricht 'static method')
        return cls.tracker_count


# Instanziierung (Kein 'new' nötig!)
t1 = ElephantTracker("GPS_001")
t2 = ElephantTracker("GPS_002")

print(f"Anzahl aktiver Tracker: {ElephantTracker.get_active_count()}")
```

#### Schritt 2: Vererbung & Mehrfachvererbung

Python erlaubt es, von mehreren Klassen gleichzeitig zu erben.

Python

```python
class BioSensor:
    def get_vitals(self):
        return "Herzfrequenz: 40 bpm"


class LocationSensor:
    def get_coords(self):
        return "7.123, 38.456"


# Mehrfachvererbung
class SuperTracker(BioSensor, LocationSensor):
    pass

st = SuperTracker()
print(st.get_vitals())  # Von BioSensor
print(st.get_coords())  # Von LocationSensor

# MRO anzeigen (Die Reihenfolge der Methodensuche)
print(f"Method Resolution Order: {SuperTracker.mro()}")
```

#### Schritt 3: Private Variablen? (Encapsulation)

In Python gibt es kein echtes `private`. Man nutzt Konventionen:

- `_name`: "Internal" (Bitte nicht von außen anfassen).
- `__name`: "Name Mangling" (Python erschwert den Zugriff von außen durch Umbenennung).

Python

```python
class SecretElephant:
    def __init__(self, secret_name):
        self.__secret_name = secret_name  # "Privat" durch Name Mangling


e = SecretElephant("Tuffi")
# print(e.__secret_name) # Würde einen Error werfen
print(e._SecretElephant__secret_name)  # So kommt man trotzdem ran (Python-Philosophie: 'We are all consenting adults')
```

---

### 5. Zusammenfassung

| **Merkmal**             | **Java / C#**                    | **Python**                                    |
|:------------------------|:---------------------------------|:----------------------------------------------|
| **Erzeugung**           | `new MyClass()`                  | `MyClass()`                                   |
| **Statische Variablen** | `static int count`               | Klassen-Attribut (außerhalb `__init__`)       |
| **Mehrfachvererbung**   | Nein (nur Interfaces)            | **Ja** (via MRO / C3 Linearization)           |
| **Sichtbarkeit**        | `public`, `private`, `protected` | Konvention (`_` und `__`), kein harter Schutz |
| **Konstruktor**         | Konstruktor-Name = Klassen-Name  | `__init__` (Initialisierung)                  |

---

### Anwendung im Projekt "Elephant Memory Cloud"

In unserem System nutzen wir **Mehrfachvererbung**, um Sensoren modular zusammenzusetzen. Ein `Elephant` Objekt könnte
von einer `Movable`-Basisklasse (für GPS) und einer `Biological`-Basisklasse (für Gesundheitsdaten) erben. Wir nutzen *
*Klassen-Attribute**, um globale Zustände wie die gesamte Datenrate aller Sensoren in Echtzeit zu aggregieren, ohne eine
externe Datenbank-Instanz für diesen Zähler bemühen zu müssen.

> **Merksatz:** "In C# ist eine Klasse ein Tresor – sicher, aber starr. In Python ist eine Klasse ein
> lebender Organismus – extrem flexibel, erfordert aber mehr Disziplin vom Entwickler (Konvention vor Restriktion)."

---
