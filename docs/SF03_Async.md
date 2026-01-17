### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Thema 3: Asynchrone Programmierung & Event Loops (`asyncio`)

### 1. Einleitung & Kontext

In C# nutzen wir `Task` und `async/await`, wobei das .NET-Runtime-System Aufgaben oft geschickt auf einen Thread-Pool
verteilt. Python nutzt für `asyncio` einen **Single-Threaded Event Loop**.

Stellen Sie sich einen Kellner (den Event Loop) in einem Restaurant vor:

- **Synchron:** Der Kellner gibt die Bestellung in der Küche ab und bleibt dort stehen, bis das Essen fertig ist. Alle
  anderen Tische müssen warten.

- **Asynchron (asyncio):** Der Kellner gibt die Bestellung ab, bekommt eine "Marke" (ein *Future* oder *Task*) und
  bedient in der Zwischenzeit andere Tische. Sobald die Küche klingelt, kehrt er zum ersten Tisch zurück.

Das ist der Kern von `asyncio`: Wir nutzen die Wartezeit auf I/O-Operationen (Input/Output), um anderen Code
auszuführen, ohne die Kosten für teure Betriebssystem-Threads zu tragen.

---

### 2. Wissenschaftliche Fragestellung

> *"Performance-Analyse von Single-Threaded Event Loops gegenüber Multi-Threaded I/O-Modellen: Benchmarking der
Skalierbarkeit bei 10.000 simultanen Netzwerkverbindungen (C10k Problem)."*

**Kernfokus:** Warum verbraucht ein asynchrones System deutlich weniger RAM als ein thread-basiertes System, wenn es um
tausende gleichzeitige Verbindungen geht?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *The C10k Problem* (Dan Kegel) oder die Dokumentation zu *libuv* (der Basis von Node.js und teilweise
relevant für Pythons Event-Loop-Implementierungen).

Die Forschung zeigt, dass Threads teuer sind: Jeder OS-Thread benötigt ca. 1–8 MB Stack-Speicher. 10.000 Threads würden
also sofort gigantische Mengen RAM fressen. Ein `asyncio`-Task hingegen ist lediglich ein Python-Objekt im Heap und
benötigt nur wenige Kilobyte.

---

### 4. Code-Demonstration (Notebook-Stil)

In diesem Beispiel simulieren wir das Abfragen von Daten aus unserer "Elephant Memory Cloud" API.

#### Schritt 1: Die "blockierende" vs. "nicht-blockierende" Verzögerung

Python

```
import asyncio
import time

# Simulation eines Netzwerk-Requests
async def fetch_elephant_data(elephant_id):
    print(f"Lade Daten für Elefant {elephant_id}...")
    # WICHTIG: nicht time.sleep() nutzen, da dies den gesamten Thread stoppt!
    await asyncio.sleep(2)
    print(f"Daten für {elephant_id} geladen!")
    return {"id": elephant_id, "status": "active"}

# Hilfsfunktion für Zeitmessung
def timer(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Dauer: {end - start:.2f} Sekunden")
        return result
    return wrapper
```

#### Schritt 2: Sequenzielle Ausführung (Langsam)

Python

```
@timer
async def run_sequential():
    for i in range(3):
        await fetch_elephant_data(i)

# Im Notebook:
# await run_sequential()
```

#### Schritt 3: Asynchrone Parallelität (Schnell)

Python

```
@timer
async def run_concurrent():
    # Wir erstellen eine Liste von Tasks und starten sie gleichzeitig
    tasks = [fetch_elephant_data(i) for i in range(3)]
    # gather wartet auf alle Tasks gleichzeitig
    results = await asyncio.gather(*tasks)
    return results

# Im Notebook:
# await run_concurrent()
```

---

### 5. Zusammenfassung

| **Merkmal**           | **Synchroner Code** | **Multi-Threading**         | **Asyncio (Event Loop)**      |
|-----------------------|---------------------|-----------------------------|-------------------------------|
| **Gleichzeitigkeit**  | Keine               | Präemptiv (OS entscheidet)  | Kooperativ (Code entscheidet) |
| **Speicherverbrauch** | Gering              | **Hoch** (Stack pro Thread) | **Sehr Gering**               |
| **Komplexität**       | Niedrig             | Hoch (Race Conditions!)     | Mittel (async/await Syntax)   |
| **Best Use Case**     | Einfache Skripte    | CPU-bound (eingeschränkt)   | **High-Concurrency I/O**      |

---

### Anwendung im Projekt "Elephant Memory Cloud"

Unsere Cloud muss Sensordaten von hunderten Elefanten gleichzeitig empfangen.

- **Mit Threads:** Jeder Elefant belegt einen Thread. Bei 500 Elefanten wird der Server instabil.

- **Mit Asyncio:** Ein einziger Prozess kann alle 500 Verbindungen mühelos verwalten, da der Prozessor die meiste Zeit
  nur darauf wartet, dass Datenpakete über das WLAN eintreffen.

> **Merksatz für Studierende:** "Asyncio ist kein Parallelismus (wie zwei Leute, die gleichzeitig kochen), sondern
> intelligentes Zeitmanagement (wie ein Koch, der die Zwiebeln schneidet, während das Wasser heiß wird)."

---
