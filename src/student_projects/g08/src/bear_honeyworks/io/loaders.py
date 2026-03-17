# Import der benötigten Module und Typen für die Datenverarbeitung
from typing import List
from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.order import Order
from bear_honeyworks.io.json_store import load_json

# Funktionen zum Laden von Inventar und Bestellungen aus JSON-Dateien, die die Daten in die entsprechenden Domänenobjekte umwandeln.
def load_inventory(path: str) -> List[HoneyJar]:
    data = load_json(path)
    return [HoneyJar(**item) for item in data]

# Funktion zum Laden von Bestellungen aus einer JSON-Datei, die die Daten in Order-Objekte umwandelt.
def load_orders(path: str) -> List[Order]:
    data = load_json(path)
    return [Order(**item) for item in data]