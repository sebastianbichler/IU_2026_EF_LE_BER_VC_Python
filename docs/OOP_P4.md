### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Für den Konstruktur gibt es kein Method Overlading wie in Java oder C#.

In Java oder C# können Sie mehrere Konstruktoren mit unterschiedlichen Parameterlisten definieren (**Method Overloading
**). In Python kann es pro Klasse nur **genau eine** `__init__`-Methode geben. Wenn Sie eine zweite `__init__`-Methode
definieren, überschreibt die letzte die vorherige.

Aber: Python ist so flexibel, dass wir dieses Ziel auf drei andere Arten erreichen. Hier ist die Übersicht:

---

# Thema 8.4: Konstruktoren-Patterns in Python

### 1. Der Standardweg: Optionale Parameter

Da Python Standardwerte für Argumente unterstützt, kann ein einziger Konstruktor viele Rollen übernehmen. Dies ersetzt
oft 80 % der überladenen Konstruktoren in C#.

```python
class Elephant:
    def __init__(self, name, age=0, species="Afrikanisch"):
        self.name = name
        self.age = age
        self.species = species


# Verschiedene Arten des Aufrufs:
e1 = Elephant("Tuffi")  # Nur Name
e2 = Elephant("Dumbo", 10)  # Name und Alter
e3 = Elephant("Babar", species="Indisch")  # Name und Keyword-Argument
```

---

### 2. Der idiomatische Weg: Class Methods als Factory Methods

Dies ist die eleganteste Lösung in Python. Wenn Sie verschiedene "Arten" haben, ein Objekt zu erstellen (z. B. aus einer
Datei, aus einer Datenbank oder mit Standardwerten), nutzen Sie `@classmethod`.

In C# entspräche das dem **Factory Pattern**.

```python
import json


class Elephant:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_json(cls, json_string):
        """Erstellt einen Elefanten aus einem JSON-String."""
        data = json.loads(json_string)
        # cls(...) ruft den eigentlichen Konstruktor auf
        return cls(name=data["name"], age=data["age"])

    @classmethod
    def create_baby(cls, name):
        """Erstellt einen Elefanten mit Alter 0."""
        return cls(name, 0)


# Anwendung:
e1 = Elephant("Tuffi", 25)  # Normaler Weg
e2 = Elephant.from_json('{"name": "Bob", "age": 12}')  # Factory Method
e3 = Elephant.create_baby("Lilly")  # Spezial-Konstruktor
```

---

### 3. Der dynamische Weg: Typ-Prüfung in `__init__`

Man kann innerhalb von `__init__` prüfen, welche Datentypen übergeben wurden. Das ist zwar "magic" und manchmal schwerer
zu lesen, aber sehr mächtig.

```python
class SmartData:
    def __init__(self, data):
        if isinstance(data, str):
            self.value = data.upper()
        elif isinstance(data, int):
            self.value = data * 10
        else:
            self.value = None


d1 = SmartData("hallo")  # value wird "HALLO"
d2 = SmartData(5)  # value wird 50
```

---

### 4. Technischer Hintergrund: `__new__` vs `__init__`

Wenn Studierende fragen: "Was ist der echte Konstruktor?", ist die Antwort technisch gesehen `__new__`.

* **`__new__`**: Ist der **Creator**. Er erstellt die Instanz im Speicher und gibt sie zurück. Er entspricht am ehesten
  dem `new` in C#. (Wird selten überschrieben, außer bei Singletons oder unveränderlichen Typen).
* **`__init__`**: Ist der **Initializer**. Das Objekt existiert bereits, und `__init__` füllt es nur mit Werten.

---

### Zusammenfassung

| Feature                | Java / C#                   | Python                            |
|:-----------------------|:----------------------------|:----------------------------------|
| **Überladen**          | Ja (mehrere Konstruktoren)  | **Nein** (nur ein `__init__`)     |
| **Alternative**        | Überladene Signaturen       | Default-Werte & Keyword-Arguments |
| **Named Constructors** | Nicht nativ (Factory nötig) | **Ja** (via `@classmethod`)       |
| **Erzeugung**          | `new Class()`               | `__new__` (intern) + `__init__`   |

**Merksatz für Studierende:**
> "In Python gibt es keine überladenen Konstruktoren. Wir nutzen stattdessen **sprechende Namen** über `@classmethod`.
> Das macht den Code oft sogar lesbarer als in Java, da man sofort sieht, *wie* das Objekt erzeugt wird (z.B.
`Elephant.from_csv(...)` statt nur `new Elephant(...)`)."

---
