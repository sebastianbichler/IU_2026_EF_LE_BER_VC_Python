# Import der benötigten Module und Typen für die Datenverarbeitung
from typing import List

from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory

# Die InventoryService-Klasse bietet Methoden zum Verwalten des Inventars, einschließlich des Speicherns von Honiggläsern und des Entfernens von Honiggläsern aus dem Inventar.
class InventoryService:
    def store(self, inventory: Inventory, jar: HoneyJar) -> None:
        inventory.add(jar)
    # Die take-Methode entfernt eine bestimmte Anzahl von Honiggläsern aus dem Inventar und gibt sie als Liste zurück.
    def take(self, inventory: Inventory, amount: int) -> List[HoneyJar]:
        return inventory.remove(amount)