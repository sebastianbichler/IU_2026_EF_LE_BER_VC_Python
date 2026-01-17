### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Thema 5: Metaprogrammierung & Introspection

### 1. Einleitung & Kontext

In C# sind Klassenbaupläne nach der Kompilierung weitgehend starr. Man kann sie per Reflection untersuchen, aber nur
schwer "on the fly" verändern. Python hingegen ist eine **dynamische Sprache**, in der Klassen selbst Objekte sind, die
zur Laufzeit erstellt, modifiziert oder gelöscht werden können.

- **Introspection:** Das Programm schaut in den Spiegel und fragt: "Welche Attribute habe ich? Zu welcher Klasse gehöre
  ich?"

- **Metaprogrammierung:** Code schreibt Code. Wir nutzen Werkzeuge wie **Decorators** oder **Metaclasses**, um das
  Verhalten von Klassen und Funktionen automatisch zu erweitern, ohne ihren Quelltext zu ändern.

---

### 2. Wissenschaftliche Fragestellung

> *"Untersuchung der Auswirkungen von Dynamic Meta-Object Protocols auf die Wartbarkeit und Typsicherheit: Eine Analyse
von Decorator-Patterns gegenüber C# Attribut-basierten Systemen."*

**Kernfokus:** Erleichtert die extreme Flexibilität von Pythons Metaprogrammierung die Entwicklung von Frameworks, oder
führt sie zu "Magie", die das Debugging unmöglich macht?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *The Art of the Metaobject Protocol* (Kiczales et al.) – ein Standardwerk der Informatik, das erklärt,
wie Sprachen sich selbst beschreiben.

In Python wird alles über das **Dunder-System** (Double Underscore) gesteuert. Methoden wie `__getattr__` oder
`__call__` sind die Schnittstellen, über die wir in die Mechanik des Interpreters eingreifen. Während C# Attribute meist
nur als Metadaten speichert, die von außen gelesen werden, sind Python-Decorators aktive Wrapper, die den ursprünglichen
Code ersetzen.

---

### 4. Code-Demonstration (Notebook-Stil)

In der "Elephant Memory Cloud" wollen wir jeden API-Aufruf automatisch validieren und loggen, ohne in jede einzelne
Funktion `print()`-Befehle schreiben zu müssen.

#### Schritt 1: Introspection (Hineinschauen)

Python

```
class ElephantArchive:
    def __init__(self):
        self.data_points = 1000
    def get_info(self):
        return "Archiv aktiv"

archive = ElephantArchive()

# Introspection nutzen
print(f"Klassenname: {archive.__class__.__name__}")
print(f"Verfügbare Methoden: {[m for m in dir(archive) if not m.startswith('__')]}")
```

#### Schritt 2: Ein einfacher Decorator (Metaprogrammierung)

Wir bauen einen "Validator", der prüft, ob ein Nutzer berechtigt ist, auf die Elefanten-Daten zuzugreifen.

Python

```
def require_auth(func):
    def wrapper(user, *args, **kwargs):
        if user != "Admin":
            raise PermissionError(f"Zugriff verweigert für {user}!")
        return func(user, *args, **kwargs)
    return wrapper

@require_auth
def delete_elephant_record(user, record_id):
    print(f"Datensatz {record_id} wurde von {user} gelöscht.")

# Test
try:
    delete_elephant_record("Student1", 42)
except PermissionError as e:
    print(e)

delete_elephant_record("Admin", 42)
```

#### Schritt 3: Die "Magie" – Dynamische Attribut-Erstellung

Wir können Attribute erstellen, die gar nicht existieren, indem wir `__getattr__` überschreiben.

Python

```
class DynamicCloudData:
    def __getattr__(self, name):
        # Wenn ein Attribut fehlt, generieren wir es on-the-fly
        return f"Dynamischer Wert für '{name}' wurde generiert."

cloud = DynamicCloudData()
print(cloud.gps_signal)
print(cloud.heart_rate)
```

---

### 5. Zusammenfassung

| **Feature**     | **Python (Metaprogramming)**          | **C# (Reflection)**                    |
|-----------------|---------------------------------------|----------------------------------------|
| **Zeitpunkt**   | Zur Laufzeit (voll dynamisch)         | Zur Laufzeit (meist read-only)         |
| **Mechanismus** | Decorators, Metaclasses, Dunder       | Attributes, Reflection API, Source Gen |
| **Sicherheit**  | "Gefährlich" (Code-Injektion möglich) | Sicherer (stark typisiert)             |
| **Power**       | Kann Sprachelemente umdefinieren      | Kann Code-Struktur analysieren         |

---

### Anwendung im Projekt "Elephant Memory Cloud"

In unserem Projekt nutzen wir Metaprogrammierung für das **Object-Relational Mapping (ORM)**. Wenn wir eine Klasse
`Elephant` definieren, "weiß" Python automatisch, welche Spalten in der Datenbank angelegt werden müssen, indem es die
Klassenattribute zur Laufzeit scannt (Introspection) und die SQL-Befehle generiert.

> **Merksatz für Studierende:** "Metaprogrammierung ist wie der Bau einer Maschine, die selbst Maschinen baut. Es ist
> extrem mächtig für Framework-Entwickler, sollte aber im normalen Anwendungscode sparsam eingesetzt werden, um die
> Lesbarkeit nicht zu opfern."

---
