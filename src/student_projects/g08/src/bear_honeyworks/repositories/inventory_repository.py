# Import der benötigten Module und Typen für die Datenverarbeitung
from typing import List

from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.io.json_store import save_json
from bear_honeyworks.io.loaders import load_inventory

# Konstante für den Pfad zur Inventardatei, die von der Repository-Klasse verwendet wird.
FILE_PATH = "data/inventory.json"

# Die InventoryRepository-Klasse bietet Methoden zum Laden und Speichern des Inventars, das aus HoneyJar
class InventoryRepository:
    def load(self) -> List[HoneyJar]:
        return load_inventory(FILE_PATH)
    # Die save-Methode speichert die übergebenen HoneyJar-Objekte im JSON-Format, indem sie die Daten in ein Dictionary umwandelt und die save_json-Funktion verwendet.
    def save(self, jars: List[HoneyJar]) -> None:
        data = [jar.__dict__ for jar in jars]
        save_json(FILE_PATH, data)