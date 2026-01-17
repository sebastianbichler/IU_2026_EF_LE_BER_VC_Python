### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Thema 1: Memory Management

## Reference Counting vs. Cyclic Garbage Collection

### 1. Einleitung & Kontext

In einer Welt, in der wir mit Big Data und komplexen Objektbeziehungen arbeiten (wie in unserem Projekt **Elephant
Memory Cloud**), ist effizientes Speichermanagement entscheidend. Während Sprachen wie C eine manuelle
Speicherverwaltung (malloc/free) erfordern, nutzen Python und C# automatische Systeme.

Der entscheidende Unterschied:

* **C# (.NET):** Nutzt primär einen **Generational Mark-and-Sweep** Algorithmus. Der Garbage Collector (GC) läuft
  periodisch, stoppt die Anwendung ("Stop-the-World") und sucht nach nicht mehr erreichbaren Objekten.
* **Python:** Nutzt ein **Hybrid-System**. Das Herzstück ist das **Reference Counting**. Nur wenn dieses System an seine
  Grenzen stößt (bei zirkulären Referenzen), springt der **Cyclic Garbage Collector** ein.

---

### 2. Wissenschaftliche Fragestellung

> *"Analyse der Latenzzeiten und Speichereffizienz bei der Verarbeitung großskaliger Objekt-Graphen: Ein Vergleich
zwischen Pythons deterministischer Referenzzählung und C# nicht-deterministischer Garbage Collection."*

**Kernfokus:** Wie wirkt sich die sofortige Freigabe durch Reference Counting auf die Echtzeit-Performance aus im
Vergleich zu den "GC-Pausen" in C#?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *Lany et al.*: *Relevance of Garbage Collection in Python* und https://dl.acm.org/doi/abs/10.5555/3566055.3566071

Die Forschung zeigt, dass Pythons Ansatz auf **Determinismus** setzt. Ein Objekt wird im Idealfall in dem Moment
zerstört, in dem die letzte Referenz verschwindet. Das schont den Cache und sorgt für eine gleichmäßige CPU-Auslastung.

**Das Problem der Zyklen:**
Wenn Objekt A auf Objekt B verweist und B zurück auf A, sinkt der Reference Count nie auf Null, selbst wenn kein anderer
Teil des Programms mehr Zugriff auf A oder B hat. Hierfür implementiert Python den `gc`-Modul-Algorithmus, der den
Objekt-Graphen nach isolierten Inseln (Zyklen) durchsucht.

---

### 4. Code-Demonstration (Notebook-Stil)

Hier ist ein strukturiertes Beispiel, das direkt in einem Jupyter Notebook vorgeführt werden kann. Wir nutzen das Modul
`sys`, um Referenzen zu zählen, und `gc`, um den Garbage Collector zu steuern.

#### Schritt 1: Einfaches Reference Counting

```python
import sys
import gc


# Ein einfaches Objekt erstellen
class Elephant:
    def __init__(self, name):
        self.name = name


e1 = Elephant("Tuffi")
# Hinweis: getrefcount gibt immer 1 höher aus, da die Funktion selbst eine temporäre Referenz hält
print(f"Referenzen für Tuffi: {sys.getrefcount(e1) - 1}")

e2 = e1
print(f"Referenzen nach e2 = e1: {sys.getrefcount(e1) - 1}")

del e2
print(f"Referenzen nach del e2: {sys.getrefcount(e1) - 1}")

```

#### Schritt 2: Das Problem – Die zirkuläre Referenz

Hier simulieren wir eine Verwandtschaftsbeziehung in der "Elephant Memory Cloud", die zu einem Memory Leak führen würde,
gäbe es nur Reference Counting.

```python
# Wir deaktivieren den automatischen GC, um den Effekt zu sehen
gc.disable()


class CircularElephant:
    def __init__(self, name):
        self.name = name
        self.partner = None

    def __del__(self):
        print(f"Speichermanager: {self.name} wird gelöscht!")


def create_cycle():
    ana = CircularElephant("Ana")
    bob = CircularElephant("Bob")
    ana.partner = bob
    bob.partner = ana
    print("Zyklus erstellt. Ana und Bob zeigen aufeinander.")


create_cycle()
# Obwohl 'ana' und 'bob' lokal in der Funktion gelöscht wurden,
# wird __del__ NICHT aufgerufen!
print("Funktion beendet, aber Speicher ist noch belegt.")

```

#### Schritt 3: Die Rettung durch den Cyclic GC

```python
print(f"Nicht abgeholte Objekte im GC: {len(gc.garbage)}")

# Wir erzwingen die zyklische Bereinigung
print("Starte manuellen Garbage Collection Lauf...")
gc.collect()

# Jetzt erst werden die __del__ Methoden aufgerufen!
gc.enable()  # Automatischen GC wieder einschalten
```

---

### 5. Zusammenfassung

| Merkmal         | Reference Counting            | Cyclic Garbage Collector        |
|-----------------|-------------------------------|---------------------------------|
| **Mechanismus** | Zähler pro Objekt             | Verfolgung von Objekt-Graphen   |
| **Vorteil**     | Sofortige Freigabe (Echtzeit) | Findet "tote Inseln" (Zyklen)   |
| **Nachteil**    | Overhead bei jeder Zuweisung  | Rechenintensiv (Stop-the-World) |
| **C# Analogie** | Nicht vorhanden               | Ähnlich dem Mark-and-Sweep      |

> **Merksatz:** "Reference Counting ist der fleißige Hausmeister, der sofort aufräumt. Der Cyclic GC ist
> das Reinigungsteam, das einmal die Woche kommt, um den Müll hinter den Schränken (Zyklen) zu finden."

---
