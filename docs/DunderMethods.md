### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Diese "Dunder"-Methoden (Double Underscore) sind das Rückgrat des **Protocol-based Programming** in Python. Während man
in C# oder Java Interfaces implementiert (`IComparable`, `IDisposable`, `IEnumerable`), überschreibt man in Python diese
speziellen Methoden, um das Verhalten des Interpreters zu steuern.

Hier ist die Übersicht der wichtigsten Dunder-Methoden, kategorisiert nach ihrem Einsatzbereich.

---

# Dunder-Methoden – Die Magie der Objekte

### 1. Lebenszyklus & Initialisierung

Diese Methoden steuern, wie Objekte entstehen und vergehen.

| Methode                   | Zweck                                                       | C# / Java Pendant         |
|:--------------------------|:------------------------------------------------------------|:--------------------------|
| **`__init__(self, ...)`** | Initialisiert die Instanz (nach der Erzeugung).             | Konstruktor-Rumpf         |
| **`__new__(cls, ...)`**   | Erzeugt die Instanz (eigentlicher Konstruktor).             | `new`-Operator            |
| **`__del__(self)`**       | Destruktor; wird aufgerufen, wenn der GC das Objekt löscht. | `Finalize()` / Destruktor |

### 2. Repräsentation (String-Konvertierung)

Wie wird das Objekt dargestellt, wenn man `print()` nutzt oder es im Debugger sieht?

| Methode                     | Zweck                                                   | C# / Java Pendant              |
|:----------------------------|:--------------------------------------------------------|:-------------------------------|
| **`__str__(self)`**         | Benutzerfreundliche Darstellung (für `print()`).        | `ToString()`                   |
| **`__repr__(self)`**        | "Offizielle" Darstellung für Entwickler (Debugger).     | `ToString()` / DebuggerDisplay |
| **`__format__(self, ...)`** | Steuert das Verhalten in f-Strings (`f"{obj:format}"`). | `IFormattable`                 |

### 3. Container & Kollektionen (Duck Typing)

Hiermit lässt man eigene Objekte wie Listen oder Dictionaries aussehen.

| Methode                        | Zweck                                     | C# / Java Pendant     |
|:-------------------------------|:------------------------------------------|:----------------------|
| **`__len__(self)`**            | Gibt die Länge zurück (`len(obj)`).       | `Count` / `Length`    |
| **`__getitem__(self, key)`**   | Zugriff via Index/Key (`obj[key]`).       | Indexer `this[int i]` |
| **`__setitem__(self, k, v)`**  | Wert setzen via Index/Key (`obj[k] = v`). | Indexer Setter        |
| **`__contains__(self, item)`** | Prüfung via `in`-Operator.                | `Contains()`          |
| **`__iter__(self)`**           | Gibt einen Iterator zurück.               | `GetEnumerator()`     |

### 4. Vergleich & Arithmetik (Operator Overloading)

Wie reagiert das Objekt auf Operatoren wie `+`, `-`, `<`, `==`?

| Methode                    | Zweck                     | C# / Java Pendant           |
|:---------------------------|:--------------------------|:----------------------------|
| **`__eq__(self, other)`**  | Gleichheit prüfen (`==`). | `Equals()`                  |
| **`__lt__(self, other)`**  | Kleiner als (`<`).        | `IComparable` / `CompareTo` |
| **`__add__(self, other)`** | Addition (`+`).           | Operator Overloading `+`    |
| **`__bool__(self)`**       | Verhalten in `if obj:`.   | `true`/`false` Operator     |

### 5. Die Spezialisten

Methoden, die Python seine einzigartige Dynamik verleihen.

| Methode                       | Zweck                                               | C# / Java Pendant          |
|:------------------------------|:----------------------------------------------------|:---------------------------|
| **`__call__(self, ...)`**     | Macht das Objekt **aufrufbar** wie eine Funktion.   | `Invoke()` / Delegate      |
| **`__enter__` / `__exit__`**  | Kontext-Manager (für `with`-Blöcke).                | `IDisposable` (`using`)    |
| **`__getattr__(self, name)`** | Wird aufgerufen, wenn ein Attribut nicht existiert. | DynamicObject / Reflection |

---

### 4. Code-Demonstration: Alles in einem Objekt

In der **Elephant Memory Cloud** nutzen wir einen `TrackerStream`, der sich wie eine Liste verhält, aber gleichzeitig
wie eine Funktion aufgerufen werden kann, um neue Daten zu pushen.

```python
class TrackerStream:
    def __init__(self, device_id):
        self.device_id = device_id
        self.buffer = []

    # 1. Repräsentation
    def __str__(self):
        return f"Stream für Gerät {self.device_id} ({len(self.buffer)} Punkte)"

    # 2. Container-Verhalten (Länge und Zugriff)
    def __len__(self):
        return len(self.buffer)

    def __getitem__(self, index):
        return self.buffer[index]

    # 3. Das Objekt als Funktion (Callable)
    def __call__(self, gps_point):
        self.buffer.append(gps_point)
        print(f"Datenpunkt {gps_point} empfangen.")

    # 4. Kontext-Manager (Aufräumen)
    def __enter__(self):
        print("Stream-Verbindung wird geöffnet...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Stream-Verbindung wird sicher geschlossen.")


# --- Anwendung ---
with TrackerStream("GPS_001") as stream:
    stream((7.12, 38.45))  # __call__ wird genutzt
    stream((7.13, 38.46))
    print(stream)  # __str__ wird genutzt
    print(f"Letzter Punkt: {stream[-1]}")  # __getitem__ wird genutzt
```

---

### Zusammenfassung

* **Dunder-Methoden** ermöglichen es eigenen Objekten, sich wie Built-in Typen (int, list, function) zu verhalten.
* **`__init__`** ist nicht der Konstruktor, sondern der Initialisierer.
* **`__call__`** ist extrem wichtig für Dekoratoren und API-Design, da Objekte wie Funktionen agieren können.
* **`__str__` vs `__repr__`**: `str` ist für Enduser (schön), `repr` ist für Entwickler (eindeutig, oft wie der
  Erzeugungscode).

> **Merksatz:** "Dunder-Methoden sind die Schnittstellen von Python zum Interpreter. Wenn man weiß,
> welche Dunder-Methode man überschreiben muss, kann man die gesamte Sprache an seine eigenen Bedürfnisse anpassen."

---
