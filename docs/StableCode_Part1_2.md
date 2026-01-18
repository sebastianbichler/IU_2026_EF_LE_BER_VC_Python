### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

Die folgenden Themen bilden das Fundament für **robuste und wartbare Software**. Während Anfänger oft nur "Code schreiben, der
funktioniert", kümmern sich Profis darum, was passiert, wenn der Code *nicht* funktioniert.

---

### Abgrenzung der Konzepte

1. **Exception Handling:** Reaktion auf **erwartbare Fehler zur Laufzeit** (Netzwerk weg, Datei fehlt).
   Programmfluss-Steuerung für den Ernstfall.
2. **Asserts:** **Sanity Checks** für Entwickler. Dokumentation von Annahmen, die niemals falsch sein dürfen. Wenn ein
   Assert fehlschlägt, ist der Code fehlerhaft (Logikfehler).
3. **Logging:** **Chronik des Systems**. Dokumentation von Ereignissen zur nachträglichen Analyse, ohne den
   Programmfluss zu unterbrechen.
4. **Testing (Pytest):** **Verifizierung der Korrektheit** von außen. Automatisiertes Ausführen des Codes gegen
   Erwartungswerte.
5. **Mocking:** **Simulation der Umwelt**. Ersetzen von teuren oder instabilen Abhängigkeiten (Datenbanken, Sensoren)
   durch "Attrappen", um isoliert testen zu können.

---

# Part 1 und 2: Exception Handling & Asserts (Resilienz)

### 1. Einleitung & Kontext

In C# nutzen wir `try-catch-finally`. Python folgt der Philosophie **"EAFP"** (*Easier to Ask for Forgiveness than
Permission*). Wir versuchen eine Operation und fangen den Fehler ab, anstatt vorher alles aufwendig zu prüfen (*LBYL -
Look Before You Leap*).

### 2. Wissenschaftliche Fragestellung

> *"Analyse der Fehlertoleranz-Strategien in verteilten Systemen: Eine Untersuchung der Performance-Differenz zwischen
präventiver Validierung (LBYL) und Ausnahme-basiertem Fehlerhandling (EAFP)."*

### 3. Code-Demonstration

Python

```python
def get_sensor_average(sensor_data):
    # ASSERT: Ein Logik-Check. Wenn das leer ist, hat der Aufrufer einen Fehler gemacht.
    assert len(sensor_data) > 0, "Sensorliste darf nicht leer sein!"

    try:
        total = sum(sensor_data)
        average = total / len(sensor_data)
    except ZeroDivisionError as e:
        print(f"Mathematischer Fehler: {e}")
        return 0
    except TypeError:
        print("Fehler: Daten enthalten keine Zahlen!")
        raise  # Fehler weiterreichen (wie 'throw' in C#)
    else:
        # Wird nur ausgeführt, wenn KEINE Exception auftrat
        print(f"Berechnung erfolgreich: {average}")
        return average
    finally:
        # Wird IMMER ausgeführt (zum Aufräumen)
        print("Bereinigungsarbeiten abgeschlossen.")
```

---
