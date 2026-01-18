### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Part 4 und 5: Testing & Mocking (Qualitätssicherung)

### 1. Einleitung & Kontext

Während Java `JUnit` und C# `xUnit/NUnit` nutzt, ist in Python **`pytest`** der Industriestandard. Es nutzt einfache
`assert`-Statements und mächtige "Fixtures" (Setup-Code). Mocking wird genutzt, um z.B. einen echten
Elefanten-GPS-Sender zu simulieren, den wir im Labor nicht physisch vorliegen haben.

### 2. Wissenschaftliche Fragestellung

> *"Effektivität von Mocking-Frameworks bei der Isolation von Seiteneffekten: Eine Evaluation der Testabdeckung in
hardwarenahen IoT-Umgebungen."*

### 3. Code-Demonstration (Testdatei `test_tracker.py`)

Python

```python
import pytest
from unittest.mock import Mock


# Die zu testende Logik
def analyze_movement(sensor):
    pos = sensor.get_current_position()
    if pos == (0, 0):
        return "Stationär"
    return "In Bewegung"


# Der Test
def test_analyze_movement_with_mock():
    # MOCKING: Wir erstellen einen Fake-Sensor
    mock_sensor = Mock()

    # Wir sagen dem Mock, was er zurückgeben soll
    mock_sensor.get_current_position.return_value = (0, 0)

    # Test ausführen
    result = analyze_movement(mock_sensor)

    assert result == "Stationär"
    # Prüfen, ob die Methode überhaupt aufgerufen wurde
    mock_sensor.get_current_position.assert_called_once()
```

---

### Zusammenfassende Übersicht für die Folien

| Merkmal         | Exception Handling     | Asserts                 | Logging             | Testing           |
|:----------------|:-----------------------|:------------------------|:--------------------|:------------------|
| **Zielgruppe**  | Der Endnutzer / System | Der Entwickler          | Der Admin / DevOps  | Die QA / CI-CD    |
| **Zeitpunkt**   | Laufzeit (Runtime)     | Entwicklung/Test        | Laufzeit (Historie) | Vor Deployment    |
| **Verhalten**   | Programm läuft weiter  | Programm bricht hart ab | Keine Auswirkung    | Report-Erstellung |
| **C# Analogie** | `try-catch`            | `Debug.Assert`          | `NLog`, `Serilog`   | `xUnit`, `Moq`    |

### Anwendung im Projekt "Elephant Memory Cloud"

In unserem Archivsystem greifen diese Zahnräder ineinander:

1. **Pytest & Mocking:** Bevor wir eine neue Version der Cloud releasen, simulieren Mocks tausende von
   Elefanten-Sensoren, um die Datenbank-Last zu testen.
2. **Asserts:** Im Code stellen wir sicher, dass ein Elefant niemals ein negatives Alter hat. Passiert das doch, stoppt
   das System sofort, bevor falsche Daten die Statistik verfälschen.
3. **Logging:** Im laufenden Betrieb loggen wir jeden erfolgreichen Daten-Upload auf `INFO`.
4. **Exception Handling:** Wenn das Internet im afrikanischen Nationalpark ausfällt, fängt eine `ConnectionError`
   -Exception dies ab und speichert die Daten lokal zwischen (Retry-Logik), statt die App abstürzen zu lassen.

> **Merksatz:** "Exceptions fangen das Unvermeidbare ab. Asserts verhindern das Unmögliche. Logging
> erklärt das Unbegreifliche. Tests beweisen das Erwünschte."

---
