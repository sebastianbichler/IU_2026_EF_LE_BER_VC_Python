### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---


# Part 3: Logging & Observability (Diagnostik)

### 1. Einleitung & Kontext

`print()` ist kein Logging. Logging erlaubt verschiedene Stufen (DEBUG, INFO, ERROR), kann in Dateien rotieren und
Metadaten (Zeitstempel, Thread-ID) automatisch hinzufügen, ohne die Anwendung für den Nutzer mit Text zu überfluten.

### 2. Wissenschaftliche Fragestellung

> *"Impact von strukturiertem Logging auf die Mean Time to Recovery (MTTR) in komplexen Cloud-Architekturen: Korrelation
von Log-Granularität und Diagnosegeschwindigkeit."*

### 3. Code-Demonstration

Python

```python
import logging

# Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ElephantCloud")


def sync_data():
    logger.info("Starte Datensynchronisation mit der Cloud...")
    try:
        # Simulierter Fehler
        raise ConnectionError("Server nicht erreichbar")
    except Exception as e:
        logger.error(f"Synchronisation fehlgeschlagen: {e}", exc_info=True)


sync_data()
```

---
