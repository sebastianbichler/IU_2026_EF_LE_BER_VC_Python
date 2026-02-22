### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Thema 8: Structural Design Patterns in dynamischen Sprachen

### 1. Einleitung & Kontext

Dieses Thema schließt den Kreis zwischen klassischer Softwarearchitektur (wie man sie aus C# und Java kennt) und der
pragmatischen Eleganz von Python. In statisch typisierten Sprachen sind Entwurfsmuster (Design Patterns) oft komplexe
Konstrukte aus Interfaces und Vererbungshierarchien. In Python "verschmelzen" viele dieser Muster mit der Sprache
selbst. Strukturmuster (Structural Patterns) befassen sich damit, wie Klassen und Objekte zu größeren Strukturen
zusammengefügt werden. In C# benötigen Muster wie **Adapter**, **Proxy** oder **Decorator** oft explizite Interfaces und
Boilerplate-Code.

In Python machen wir uns zwei Konzepte zunutze, die diese Muster radikal vereinfachen:

1. **Duck Typing:** "Wenn es watschelt wie eine Ente...", brauchen wir kein `IInterface`.
2. **First-Class Functions & Objects:** Da Funktionen und Klassen Objekte sind, können wir sie einfach übergeben,
   einwickeln (wrappen) oder zur Laufzeit modifizieren.

---

### 2. Wissenschaftliche Fragestellung

> *"Die Erosion klassischer Entwurfsmuster: Eine komparative Analyse der Implementierungskomplexität und Wartbarkeit von
GoF-Strukturmustern in statischen vs. dynamischen Laufzeitumgebungen."*

**Kernfokus:** Erhöht der Wegfall von formalen Interfaces die Fehleranfälligkeit (Runtime-Errors), oder überwiegt der
Gewinn an Lesbarkeit und Flexibilität durch weniger "Boilerplate"?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *Design Patterns in Dynamic Languages* (Peter Norvig).

In seinem berühmten Vortrag zeigt Norvig (Director of Research bei Google), dass 16 der 23 klassischen "Gang of Four" (
GoF) Muster in dynamischen Sprachen wie Lisp oder Python entweder unsichtbar oder drastisch vereinfacht sind.
Strukturmuster wie der **Decorator** sind in Python sogar nativer Bestandteil der Syntax.

---

### 4. Code-Demonstration (Notebook-Stil)

Wir nutzen das **Adapter-Muster**, um verschiedene Sensordaten in unserer "Elephant Memory Cloud" zu vereinheitlichen.
Wir haben einen neuen GPS-Sensor, der Daten in einem inkompatiblen Format liefert.

#### Schritt 1: Die Ausgangslage (Inkompatible Klassen)

```python
# Alter Sensor (Standard im Projekt)
class LegacyGPSSensor:
    def get_coordinates(self):
        return {"lat": 51.3, "lon": 12.3}


# Neuer Sensor (andere Schnittstelle, liefert String)
class NewHighTechSensor:
    def fetch_data(self):
        return "51.339, 12.373"  # "Latitude, Longitude"

```

#### Schritt 2: Das Adapter-Muster (Die "Pythonic" Way)

In C# bräuchten wir ein `IGPSSensor`-Interface. In Python nutzen wir einfach eine Wrapper-Klasse oder sogar nur eine
Funktion.

```python
class GPSAdapter:
    """Adapter, der den NewHighTechSensor kompatibel zum Legacy-System macht."""

    def __init__(self, sensor):
        self.sensor = sensor

    def get_coordinates(self):
        # Wir konvertieren das Format "on the fly"
        raw_data = self.sensor.fetch_data()
        lat, lon = map(float, raw_data.split(","))
        return {"lat": lat, "lon": lon}


# Anwendung in der Cloud-Logik
def log_elephant_position(sensor_object):
    # Dank Duck Typing ist es egal, welche Klasse es ist,
    # solange sie get_coordinates() besitzt.
    pos = sensor_object.get_coordinates()
    print(f"Position gespeichert: {pos['lat']}, {pos['lon']}")


# Test
old_s = LegacyGPSSensor()
new_s = GPSAdapter(NewHighTechSensor())

log_elephant_position(old_s)
log_elephant_position(new_s)

```

#### Schritt 3: Das Proxy-Muster (Dynamische Zugriffskontrolle)

Wir nutzen `__getattr__` (Thema 5), um einen Proxy zu bauen, der den Zugriff auf das "Elephant Archive" schützt.

```python
class ArchiveProxy:
    def __init__(self, real_archive, user_role):
        self.real_archive = real_archive
        self.user_role = user_role

    def __getattr__(self, name):
        # Prüfung beim Zugriff auf jede Methode
        if self.user_role != "Admin" and name.startswith("delete"):
            raise PermissionError(f"Rolle {self.user_role} darf nicht löschen!")

        # Delegierung an das echte Objekt
        return getattr(self.real_archive, name)


# Das echte Objekt
class ElephantArchive:
    def get_data(self): return "Sensible Daten"

    def delete_record(self): print("Gelöscht!")


# Test
proxy = ArchiveProxy(ElephantArchive(), user_role="Guest")
print(proxy.get_data())  # Funktioniert
# proxy.delete_record() # Würde PermissionError werfen

```

---

### 5. Zusammenfassung

| Muster        | Zweck                     | Python Realisierung      | Vergleich zu C#          |
|---------------|---------------------------|--------------------------|--------------------------|
| **Decorator** | Funktionalität erweitern  | `@decorator` Syntax      | Benötigt Klassen-Wrapper |
| **Adapter**   | Schnittstellen angleichen | Duck Typing / Wrapper    | Benötigt Interfaces      |
| **Proxy**     | Zugriffskontrolle         | `__getattr__` Magie      | Benötigt `DispatchProxy` |
| **Facade**    | Komplexität verbergen     | Einfache Module / Pakete | Ähnlich, aber starrer    |

---

### Anwendung im Projekt "Elephant Memory Cloud"

Wenn wir verschiedene Cloud-Provider (AWS, Azure, Lokal) anbinden:

* Wir schreiben keine riesigen Interface-Hierarchien.
* Wir bauen kleine **Adapter**, die die API-Calls der Provider auf unsere interne Methode `upload_to_cloud()` mappen.
* Das System bleibt erweiterbar, ohne dass wir bestehenden Code ändern müssen (Open-Closed Principle).

> **Merksatz:** "In Python ist ein Entwurfsmuster oft kein komplizierter Plan, den man mühsam bauen
> muss, sondern eine natürliche Art, die dynamischen Features der Sprache zu nutzen. Weniger Code bedeutet oft weniger
> Bugs."

---
