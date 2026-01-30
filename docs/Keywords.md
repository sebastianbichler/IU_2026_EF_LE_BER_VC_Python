### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Hier ist eine vollständige Übersicht der Python-Schlüsselwörter (Keywords). In Python sind diese Begriffe reserviert und
können nicht als Bezeichner (Variablen- oder Funktionsnamen) verwendet werden.

### Übersicht der Python-Schlüsselwörter

| Schlüsselwort  | Kategorie     | Kurzbeschreibung                                                          |
|:---------------|:--------------|:--------------------------------------------------------------------------|
| **`False`**    | Logik         | Der boolesche Wert "Falsch".                                              |
| **`True`**     | Logik         | Der boolesche Wert "Wahr".                                                |
| **`None`**     | Datentyp      | Repräsentiert die Abwesenheit eines Wertes (wie `null` in C#).            |
| **`and`**      | Logik         | Logisches UND.                                                            |
| **`or`**       | Logik         | Logisches ODER.                                                           |
| **`not`**      | Logik         | Logische Negation.                                                        |
| **`is`**       | Identität     | Prüft, ob zwei Variablen auf dasselbe Objekt im Speicher zeigen.          |
| **`in`**       | Zugehörigkeit | Prüft, ob ein Wert in einer Collection (Liste, Set, etc.) enthalten ist.  |
| **`if`**       | Kontrolle     | Startet eine bedingte Anweisung.                                          |
| **`elif`**     | Kontrolle     | "Else if" – weitere Bedingung, wenn `if` falsch war.                      |
| **`else`**     | Kontrolle     | Alternativer Block, wenn alle Bedingungen davor falsch waren.             |
| **`for`**      | Schleife      | Iteriert über ein iterierbares Objekt (Liste, Range, etc.).               |
| **`while`**    | Schleife      | Wiederholt einen Block, solange eine Bedingung wahr ist.                  |
| **`break`**    | Schleife      | Beendet die aktuelle Schleife sofort.                                     |
| **`continue`** | Schleife      | Springt zum nächsten Durchlauf der Schleife.                              |
| **`return`**   | Funktion      | Beendet eine Funktion und gibt optional einen Wert zurück.                |
| **`yield`**    | Generator     | Pausiert eine Funktion und gibt einen Wert zurück (Iterator-Erzeugung).   |
| **`def`**      | Struktur      | Definiert eine neue Funktion oder Methode.                                |
| **`class`**    | Struktur      | Definiert eine neue Klasse.                                               |
| **`lambda`**   | Funktion      | Erstellt eine anonyme Einzeiler-Funktion.                                 |
| **`pass`**     | Platzhalter   | Ein leerer Befehl (tut nichts), nötig wegen der Einrückungssyntax.        |
| **`import`**   | Modul         | Lädt ein Modul oder eine Bibliothek.                                      |
| **`from`**     | Modul         | Importiert spezifische Teile eines Moduls.                                |
| **`as`**       | Modul/Kontext | Erstellt einen Alias (Namensersatz) bei Imports oder Context-Managern.    |
| **`try`**      | Fehler        | Startet einen Block mit Fehlerüberwachung.                                |
| **`except`**   | Fehler        | Fängt Ausnahmen (Exceptions) ab.                                          |
| **`finally`**  | Fehler        | Block, der immer ausgeführt wird (aufräumen).                             |
| **`raise`**    | Fehler        | Löst manuell eine Exception aus (wie `throw` in C#).                      |
| **`assert`**   | Debugging     | Prüft eine Bedingung und wirft einen Fehler, wenn sie falsch ist.         |
| **`with`**     | Kontext       | Nutzt einen Context-Manager (automatisches Setup/Teardown, z.B. Dateien). |
| **`global`**   | Scope         | Deklariert eine Variable innerhalb einer Funktion als global.             |
| **`nonlocal`** | Scope         | Deklariert eine Variable im äußeren (aber nicht globalen) Bereich.        |
| **`del`**      | Speicher      | Löscht eine Referenz auf ein Objekt oder ein Element aus einer Liste.     |
| **`async`**    | Asynchron     | Definiert eine asynchrone Funktion (Coroutine).                           |
| **`await`**    | Asynchron     | Wartet auf das Ergebnis einer asynchronen Operation.                      |

---

### Besonderheit: Soft Keywords (Ab Python 3.10)

Einige Wörter sind nur in bestimmten Kontexten reserviert, um die Abwärtskompatibilität nicht zu gefährden:

| Schlüsselwort | Kontext          | Kurzbeschreibung                                     |
|:--------------|:-----------------|:-----------------------------------------------------|
| **`match`**   | Pattern Matching | Startet eine Strukturprüfung (ähnlich `switch`).     |
| **`case`**    | Pattern Matching | Definiert ein Muster innerhalb eines `match`-Blocks. |
| **`_`**       | Pattern Matching | Wildcard-Symbol (passt auf alles) im `match`-Block.  |
| **`type`**    | Typing (3.12+)   | Definiert Typ-Aliase (`type Vector = list[float]`).  |

---

### Ein kleiner "Pro-Tipp":

Die aktuelle Liste der Keywords kann jederzeit direkt in Python abgefragt werden:

```python
import keyword

print(keyword.kwlist)
print(f"Anzahl der Keywords: {len(keyword.kwlist)}")
```
---
