### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---
Dieses Thema ist der "Gamechanger" für die Performance in Python. Wir haben gelernt, dass das GIL (Thema 2) uns bei
Threads ausbremst. **NumPy** umgeht dieses Problem, indem es rechenintensive Aufgaben in hochoptimierten C- und
Fortran-Code auslagert.

---

# Thema 4: Vectorization & SIMD mit NumPy

### 1. Einleitung & Kontext

In klassischem Python (und oft auch in C#) schreiben wir Schleifen (`for i in range...`), um Operationen auf Listen
auszuführen. In Python ist das extrem langsam, da bei jedem Schleifendurchlauf der Typ geprüft und das Objekt entpackt
werden muss (Boxing/Unboxing).

**NumPy** nutzt **Vektorisierung**. Anstatt Element für Element zu berechnen, werden ganze Blöcke von Daten gleichzeitig
verarbeitet. Dabei nutzt NumPy die **SIMD-Befehle** (Single Instruction, Multiple Data) moderner CPUs.

* **Skalar (Normales Python):** 1 + 1, dann 2 + 2, dann 3 + 3...
* **Vektor (NumPy/SIMD):** [1, 2, 3, 4] + [1, 2, 3, 4] in einem einzigen CPU-Zyklus.

---

### 2. Wissenschaftliche Fragestellung

> *"Quantifizierung des Performance-Gains durch SIMD-gestützte Vektorisierung in Python: Eine vergleichende Analyse von
Cache-Lokalität und Pipeline-Auslastung gegenüber nativen Python-Iteratoren."*

**Kernfokus:** Warum ist ein "langsamer" Interpreter wie Python mit NumPy oft genauso schnell wie nativer C++ oder C#
Code? (Stichwort: Speicher-Layout und CPU-Cache).

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *Array programming with NumPy* (Harris, C.R. et al., Nature 2020). https://www.nature.com/articles/s41586-020-2649-2

Diese fundamentale Arbeit beschreibt, wie NumPy das "Array-Programmiermodell" etabliert hat. Der Erfolg beruht darauf,
dass Daten in **kontinuierlichen Speicherblöcken** (C-Arrays) liegen. Dies ermöglicht es der CPU, Daten effizient vorab
in den Cache zu laden (*Prefetching*), was bei verstreuten Python-Listen-Objekten unmöglich ist.

---

### 4. Code-Demonstration (Notebook-Stil)

Wir vergleichen die Berechnung der Distanz zum Ursprung für 1 Million Elefanten-Positionen in der "Elephant Memory
Cloud".

#### Schritt 1: Setup der Daten

```python
import numpy as np
import time
import math

# 1 Million Positionen (x, y)
n = 1_000_000
x_coords = list(range(n))
y_coords = list(range(n))

# Als NumPy Arrays
x_np = np.array(x_coords)
y_np = np.array(y_coords)

```

#### Schritt 2: Die klassische Python-Schleife

```python
def calculate_dist_python(x_list, y_list):
    res = []
    for i in range(len(x_list)):
        # Jedes math.sqrt und **2 muss vom Interpreter einzeln geprüft werden
        res.append(math.sqrt(x_list[i] ** 2 + y_list[i] ** 2))
    return res


start = time.time()
calculate_dist_python(x_coords, y_coords)
print(f"Python Schleife: {time.time() - start:.4f}s")

```

#### Schritt 3: Die NumPy Vektorisierung

```python
def calculate_dist_numpy(x, y):
    # Die gesamte Operation wird in C ausgeführt
    return np.sqrt(x ** 2 + y ** 2)


start = time.time()
calculate_dist_numpy(x_np, y_np)
print(f"NumPy Vektorisierung: {time.time() - start:.4f}s")

```

*Ergebnis:* NumPy ist meist **50- bis 100-mal schneller**.

---

### 5. Zusammenfassung für die Folien

| Merkmal         | Standard Python Listen                | NumPy Arrays                            |
|-----------------|---------------------------------------|-----------------------------------------|
| **Speicher**    | Liste von Zeigern (verstreut)         | Kontinuierlicher Block (kompakt)        |
| **Typisierung** | Dynamisch (Prüfung bei jedem Schritt) | Statisch (homogen innerhalb des Arrays) |
| **Berechnung**  | Elementweise (Skalar)                 | Parallel (SIMD / Vektor)                |
| **Performance** | O(n) mit hohem Overhead               | O(n) mit Hardware-Optimierung           |

---

### Anwendung im Projekt "Elephant Memory Cloud"

Wenn wir die Bewegungsprofile der Elefanten analysieren:

* **Schlechter Code:** Eine `for`-Schleife über alle GPS-Punkte, um die Durchschnittsgeschwindigkeit zu berechnen.
* **Guter Code:** Die Differenzen der Koordinaten-Arrays bilden (`np.diff`) und die Norm berechnen. Das GIL spielt hier
  keine Rolle, da NumPy das GIL während der schweren C-Berechnungen freigibt!

> **Merksatz für Studierende:** "Wenn du in Python eine `for`-Schleife für mathematische Berechnungen schreibst, hast du
> wahrscheinlich schon verloren. Denk in Vektoren, nicht in Zahlen."

---
