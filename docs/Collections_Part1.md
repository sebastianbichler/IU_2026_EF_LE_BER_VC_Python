### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Diese Übersicht schließt den Kreis zwischen den klassischen Datenstrukturen (wie man sie aus C# oder Java kennt) und der
hochdynamischen, funktionalen Arbeitsweise von Python.

---

# Datentypen, Generics & Funktionale Schnittstellen

### 1. Einleitung & Kontext

In statisch typisierten Sprachen wie C# sind Collections streng an Typen und Interfaces gebunden (`List<T>`,
`IEnumerable`, `IComparable`). In Python sind Collections von Natur aus **heterogen** (können verschiedene Typen
mischen) und nutzen das **Protocol-Prinzip** (Dunder-Methoden) anstelle von expliziten Interface-Deklarationen.

---

### 2. Die wichtigsten Built-in Collections

| Typ              | Charakteristik                                         | C# / Java Pendant             |
|:-----------------|:-------------------------------------------------------|:------------------------------|
| **List** `[]`    | Geordnet, veränderlich, dynamische Größe.              | `List<T>` / `ArrayList`       |
| **Tuple** `()`   | Geordnet, **unveränderlich**. Oft für Records genutzt. | `Tuple<T>` / `ReadOnlyList`   |
| **Set** `{}`     | Ungeordnet, **eindeutige** Elemente (Hashing).         | `HashSet<T>`                  |
| **Dict** `{k:v}` | Schlüssel-Wert-Paare, extrem optimiert.                | `Dictionary<K,V>` / `HashMap` |

---

### 3. Generische Datenstrukturen (Generics)

Seit Python 3.9/3.10 nutzt man Typ-Hints für Generics. Python erzwingt diese nicht zur Laufzeit, aber statische
Checker (MyPy) nutzen sie wie C#-Compiler.

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')  # Ein Platzhalter für einen beliebigen Typ


class Stack(Generic[T]):
    def __init__(self):
        self._items: List[T] = []

    def push(self, item: T):
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()


# Nutzung
int_stack = Stack[int]()
int_stack.push(10)
```

---

### 4. Schnittstellen & Protokolle (Die "Magie" unter der Haube)

Anstatt Interfaces wie `IComparable` zu implementieren, überschreibt Python **Dunder-Methoden** (Double Underscore).

#### A. Comparable (Vergleichbarkeit)

In C#: `IComparable`. In Python: **Rich Comparisons**.

```python
class Elephant:
    def __init__(self, weight):
        self.weight = weight

    def __lt__(self, other):  # Less Than (<)
        return self.weight < other.weight

    def __eq__(self, other):  # Equal (==)
        return self.weight == other.weight
```

#### B. Iteratoren (Durchlaufbarkeit)

In C#: `IEnumerable`. In Python: `__iter__` und `__next__`.

```python
class MyCollection:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return iter(self.data)  # Delegiert an den internen Iterator


for item in MyCollection([1, 2, 3]):
    print(item)
```

#### C. Composite Pattern (Struktur)

Da Python dynamisch ist, benötigt das Composite-Pattern (Einzelobjekt und Gruppe gleich behandeln) oft keine gemeinsame
Basisklasse, sondern nur dieselbe Methoden-Signatur.

---

### 5. Funktionale Programmierung auf Collections

Python bietet mächtige Werkzeuge, um auf diesen Datenstrukturen deklarativ zu arbeiten.

#### A. Lambda & Higher-Order Functions

```python
numbers = [1, 5, 8, 10, 3]

# Filter: Alle über 5
big_ones = list(filter(lambda x: x > 5, numbers))

# Map: Alle verdoppeln
doubled = list(map(lambda x: x * 2, numbers))

# Reduce: Summe bilden
from functools import reduce

total = reduce(lambda x, y: x + y, numbers)
```

#### B. Comprehensions (Der "Pythonic Way")

C#-Entwickler nutzen LINQ (`Select`, `Where`). In Python nutzt man fast immer Comprehensions, da sie schneller und
lesbarer sind.

```python
# List Comprehension (Wie Select + Where)
names = ["Ana", "Bob", "Alice", "Tuffi"]
a_names = [n.upper() for n in names if n.startswith("A")]
# Ergebnis: ["ANA", "ALICE"]

# Dict Comprehension
name_lengths = {n: len(n) for n in names}
# Ergebnis: {"Ana": 3, "Bob": 3, ...}

# Set Comprehension
unique_initials = {n[0] for n in names}
```

---

### 6. Zusammenfassung

| Konzept        | Java / C#              | Python                                 |
|:---------------|:-----------------------|:---------------------------------------|
| **Interface**  | `interface IRunnable`  | `Protocol` oder Dunder `__call__`      |
| **Iterator**   | `IEnumerator`          | `__iter__` + `yield`                   |
| **Generics**   | `List<T>`              | `list[T]` (Type Hints)                 |
| **LINQ**       | `data.Where(x => ...)` | `[x for x in data if ...]`             |
| **Dictionary** | `IDictionary`          | `dict` (Hash-Map ist Kern der Sprache) |

---

### Anwendung im Projekt "Elephant Memory Cloud"

In der Cloud verarbeiten wir GPS-Daten.

1. Wir speichern die letzten 100 Positionen in einer **List**.
2. Wir nutzen ein **Set**, um die IDs aller Elefanten in einem Gebiet schnell und ohne Dubletten zu finden.
3. Wir nutzen **Comprehensions**, um Rohdaten in Millisekunden zu filtern:
   `[p for p in path if p.is_valid()]`
4. Wir implementieren `__lt__` in unserer `Elephant`-Klasse, damit wir eine Liste von Elefanten einfach mit
   `elephants.sort()` nach ihrem Alter oder Gewicht sortieren können.

> **Merksatz für Studierende:** "In C# fragt man: 'Implementierst du das Interface?'. In Python fragt man: 'Hast du die
> nötige Dunder-Methode?'. Wenn es wie eine Ente quakt (die Methode hat), dann ist es eine Ente (erfüllt das Interface)."

---

**Möchten Sie, dass ich hierzu noch ein konkretes Code-Beispiel für das "Composite Pattern" (z.B. eine Herde von
Elefanten, die sich wie ein einzelner Elefant verhält) erstelle?**
