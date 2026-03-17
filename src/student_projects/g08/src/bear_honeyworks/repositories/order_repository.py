# Import der benötigten Module und Typen für die Datenverarbeitung
from typing import List
from bear_honeyworks.domain.order import Order
from bear_honeyworks.io.json_store import load_json, save_json

# Konstante für den Pfad zur Bestelldatei, die von der Repository-Klasse verwendet wird.
FILE_PATH = "data/orders.json"

# Die OrderRepository-Klasse bietet Methoden zum Laden und Speichern von Bestellungen, die aus Order-Objekten bestehen.
class OrderRepository:
    def load(self) -> List[Order]:
        data = load_json(FILE_PATH)
        return [Order(**item) for item in data]

    def save(self, orders: List[Order]) -> None:
        data = [order.__dict__ for order in orders]
        save_json(FILE_PATH, data)