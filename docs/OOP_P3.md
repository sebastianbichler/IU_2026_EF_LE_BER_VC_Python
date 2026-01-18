### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Objektorientierung (OOP) – Part3: Der Blueprint der OOP in Python

### 1. Basis-Struktur & Instanziierung

In Python gibt es kein Schlüsselwort `new`. Eine Klasse wird definiert und wie eine Funktion aufgerufen.

```python
class Elephant:
    def __init__(self, name: str):  # Konstruktor (Initialisierung)
        self.name = name  # Instanz-Variable


# Instanziierung
e = Elephant("Tuffi")
```

---

### 2. Konstruktoren & Initialisierung (`__init__` vs. `__post_init__`)

Python unterscheidet zwischen der Erzeugung des Objekts (`__new__`) und der Initialisierung (`__init__`).

* **`__init__`**: Der Standardweg, um Attribute zu setzen.
* **`__post_init__`**: Wird fast ausschließlich in **Dataclasses** verwendet, um Logik auszuführen, nachdem der
  automatisch generierte `__init__` fertig ist.

```python
from dataclasses import dataclass


@dataclass
class BioData:
    heart_rate: int

    def __post_init__(self):
        # Validierung nach der automatischen Erzeugung
        if self.heart_rate <= 0:
            self.heart_rate = 40  # Standardwert setzen
```

---

### 3. Vererbung & Mehrfachvererbung

Python erlaubt es, von beliebig vielen Klassen zu erben. Die Suche nach Methoden erfolgt über die **MRO (Method
Resolution Order)**.

```python
class Animal:
    def breathe(self): print("Atmen...")


class Tracker:
    def track(self): print("Sende GPS...")


# Mehrfachvererbung: SuperElephant ist beides
class SuperElephant(Animal, Tracker):
    def work(self):
        super().breathe()  # Zugriff auf Elternklasse
        self.track()
```

---

### 4. Abstrakte Klassen

Da Python dynamisch ist, erzwingt es Abstraktion nicht nativ. Wir nutzen das Modul `abc` (Abstract Base Classes).

```python
from abc import ABC, abstractmethod


class BaseSensor(ABC):
    @abstractmethod
    def read_data(self):
        pass  # Muss in Unterklasse implementiert werden


class TempSensor(BaseSensor):
    def read_data(self):
        return 25.5
```

---

### 5. Kapselung (Public, Protected, Private)

In Python gibt es keine echten Zugriffssperren. Es basiert auf **Konventionen**:

* `name`: **Public** (Überall zugänglich).
* `_name`: **Protected** (Konvention: "Bitte nur intern/in Unterklassen nutzen").
* `__name`: **Private** (Name Mangling: Python benennt das Attribut intern um, um versehentlichen Zugriff zu
  erschweren).

```python
class SecurityElephant:
    def __init__(self):
        self.public_id = "123"
        self._protected_status = "OK"
        self.__private_key = "SECRET_99"


e = SecurityElephant()
print(e.public_id)  # OK
print(e._protected_status)  # OK (aber verpönt)
# print(e.__private_key)     # AttributeError!
print(e._SecurityElephant__private_key)  # Hack: So kommt man trotzdem ran
```

---

### 6. Überschreiben von Funktionen

Einfach die Methode mit demselben Namen erneut definieren. Mit `super()` wird die Elternmethode aufgerufen.

```python
class BasicElephant:
    def sound(self):
        return "Törööö"


class LoudElephant(BasicElephant):
    def sound(self):
        original = super().sound()
        return f"{original} !!!".upper()
```

---

### 7. Rückgabewerte (Multiple Returns)

Eines der beliebtesten Features in Python: Funktionen können scheinbar mehrere Werte zurückgeben. Technisch gesehen wird
ein **Tuple** zurückgegeben, das beim Aufruf entpackt wird.

```python
def get_elephant_stats():
    weight = 5000
    height = 3.5
    age = 25
    return weight, height, age  # Gibt ein Tuple (5000, 3.5, 25) zurück


# Unpacking
w, h, a = get_elephant_stats()
print(f"Gewicht: {w}, Höhe: {h}")
```

---

### 8. Weitere Besonderheiten (Property Decorators)

Anstatt Getter und Setter wie in Java (`getWeight()`, `setWeight()`) zu schreiben, nutzt Python `@property`. Das sieht
von außen aus wie ein Feld, ist aber eine Methode.

```python
class SmartElephant:
    def __init__(self):
        self._weight = 4000

    @property
    def weight_kg(self):
        return self._weight

    @weight_kg.setter
    def weight_kg(self, value):
        if value > 0:
            self._weight = value
        else:
            raise ValueError("Gewicht muss positiv sein!")


e = SmartElephant()
e.weight_kg = 4500  # Nutzt den Setter
print(e.weight_kg)  # Nutzt den Getter
```

---

### Zusammenfassung für den Vergleich (Cheat Sheet)

| Merkmal               | Java / C#                         | Python                                         |
|:----------------------|:----------------------------------|:-----------------------------------------------|
| **Konstruktor**       | `ClassName()`                     | `__init__(self, ...)`                          |
| **Sichtbarkeit**      | Schlüsselwörter (`private`, etc.) | Präfixe (`_` oder `__`)                        |
| **Mehrfachvererbung** | Nein (nur Interfaces)             | **Ja**                                         |
| **Interfaces**        | `interface`                       | Abstrakte Basisklassen (`ABC`)                 |
| **Method Resolution** | Statisch (Compile Time)           | Dynamisch (MRO)                                |
| **Properties**        | Get/Set Methoden                  | `@property` Decorator                          |
| **Self-Referenz**     | `this`                            | `self` (muss explizit als 1. Parameter stehen) |

> **Wichtiger Hinweis für Studierende:** "In Python ist `self` kein magisches Wort wie `this` in C#. Es ist einfach der
> Name des ersten Parameters jeder Instanzmethode. Man könnte es theoretisch `hugo` nennen, aber tun Sie das bitte nie!"

---
