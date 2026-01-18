### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Hier ist die Übersicht über die Kontrollstrukturen in Python. Python unterscheidet sich hier in einigen Punkten
fundamental von C-basierten Sprachen (C#, Java, C++), insbesondere durch das Fehlen bestimmter Konstrukte und die
Einführung von mächtigem **Pattern Matching**.

---

# Control Flow – Steuerung des Programmablaufs

### 1. Bedingte Anweisungen (`if-elif-else`)

In Python gibt es kein `switch` für einfache Bedingungen und kein `then`. Das C#-Ternary-Format
`condition ? true : false` wird in Python anders geschrieben.

```python
# Standard if-else
status = "moving"
if status == "moving":
    speed = 5
elif status == "sleeping":  # 'elif' statt 'else if'
    speed = 0
else:
    speed = 1

# Ternary Operator (Python-Stil)
# [Wert wenn True] if [Bedingung] else [Wert wenn False]
description = "Schnell" if speed > 3 else "Langsam"
```

---

### 2. Das neue "Switch": Structural Pattern Matching (`match-case`)

Seit Python 3.10 gibt es `match`. Es ist viel mächtiger als ein klassisches `switch`, da es **Destructuring**
beherrscht (Objekte direkt zerlegen).

```python
def process_command(command):
    match command:
        case "START":
            print("System startet")
        case "STOP" | "HALT":  # Mehrere Werte (OR)
            print("System stoppt")
        case ["MOVE", x, y]:  # List-Pattern: Matcht wenn command eine Liste mit 3 Elementen ist
            print(f"Bewege zu Koordinate {x}/{y}")
        case {"status": "error", "code": c}:  # Dict-Pattern
            print(f"Fehler mit Code {c} gefunden")
        case _:  # Default (wie 'default' in C#)
            print("Unbekannter Befehl")
```

---

### 3. Schleifen (Loops)

#### A. Die `for`-Schleife (Eigentlich ein `foreach`)

In Python ist `for` immer ein Iterator. Es gibt keine C-Style-Schleife `for(int i=0; i<10; i++)`. Man nutzt stattdessen
`range()`.

```python
# Zählschleife 0 bis 9
for i in range(10):
    print(i)

# Über eine Liste (foreach)
elephants = ["Tuffi", "Dumbo", "Babar"]
for name in elephants:
    print(name)

# Mit Index (enumerate)
for idx, name in enumerate(elephants):
    print(f"Elefant {idx}: {name}")
```

#### B. Die `while`-Schleife

Funktioniert wie gewohnt.

```python
energy = 100
while energy > 0:
    energy -= 10
```

#### C. Das "Do-While" Problem

Python hat **kein natives `do-while`**. Man simuliert es mit einer Endlosschleife und einem `break` am Ende.

```python
while True:
    # Code wird mindestens einmal ausgeführt
    action = input("Noch einmal? (j/n)")
    if action == "n":
        break
```

---

### 4. Jump Statements & Besonderheiten

* **`break` / `continue`**: Wie in C# / Java.
* **`pass`**: Ein Platzhalter. Da Python keine geschweiften Klammern hat, kann ein Block nicht leer sein. `pass` sagt: "
  Hier passiert absichtlich nichts".
* **`goto`**: Existiert in Python **nicht**. Es widerspricht der Philosophie von sauberem, lesbarem Code.
* **`else` bei Schleifen (Exklusiv in Python!)**: Ein Block, der ausgeführt wird, wenn die Schleife **normal beendet**
  wurde (d.h. *nicht* durch ein `break` abgebrochen wurde).

```python
for e in elephants:
    if e == "Gesuchter Elefant":
        print("Gefunden!")
        break
else:
    # Dieser Teil wird NUR ausgeführt, wenn die Liste komplett durchlaufen wurde
    # ohne dass das 'break' getroffen wurde.
    print("Nicht in der Herde gefunden.")
```

---

### 5. Vergleichstabelle

| Struktur          | C# / Java             | Python              | Besonderheit                            |
|:------------------|:----------------------|:--------------------|:----------------------------------------|
| **Bedingung**     | `if (cond) { ... }`   | `if cond:`          | Einrückung (Indentation) ist Pflicht.   |
| **Mehrfach-Wahl** | `switch / case`       | `match / case`      | Kann Strukturen und Typen prüfen.       |
| **Zählschleife**  | `for(i=0;... )`       | `for i in range():` | Nutzt Generatoren (`range`).            |
| **Do-While**      | `do { ... } while();` | *nicht vorhanden*   | Simulation via `while True + break`.    |
| **Ternary**       | `cond ? a : b`        | `a if cond else b`  | Liest sich wie ein englischer Satz.     |
| **Sprungmarken**  | `goto`                | *nicht vorhanden*   | Strukturierte Programmierung erzwungen. |
| **Leerer Block**  | `{ }`                 | `pass`              | Notwendig wegen Syntax-Struktur.        |

---

### Anwendung im Projekt "Elephant Memory Cloud"

Beim Verarbeiten der Sensordaten nutzen wir das **Pattern Matching**, um verschiedene Datenformate (JSON, Binär, CSV)
elegant zu unterscheiden:

```python
def handle_sensor_data(data):
    match data:
        case {"type": "GPS", "lat": l, "lon": r}:
            update_position(l, r)
        case {"type": "BIO", "heart_rate": h} if h > 100:  # Case mit Guard (if)
            trigger_alarm("Hoher Puls!")
        case _:
            log_error("Unbekanntes Datenformat")
```

> **Merksatz für Studierende:** "In Python ist weniger oft mehr. Wir haben kein `goto` und kein `do-while`, weil man
> diese fast immer durch sauberere `while`- oder `for`-Strukturen ersetzen kann. Das `match-case` ist kein einfacher
> Switch, sondern ein Schweizer Taschenmesser für Datenstrukturen."

---
