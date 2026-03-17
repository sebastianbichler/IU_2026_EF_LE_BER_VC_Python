# Import der benötigten Module für die JSON-Verarbeitung und Dateipfade
import json
from pathlib import Path
from typing import Any

# Funktionen zum Laden und Speichern von JSON-Daten, die in der Anwendung verwendet werden können.
def load_json(path: str) -> Any:
    file = Path(path)
    if not file.exists():
        return []
    with file.open("r", encoding="utf-8") as f:
        return json.load(f)

# Funktion zum Speichern von Daten im JSON-Format, die sicherstellt, dass der Zielordner existiert.
def save_json(path: str, data: Any) -> None:
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)