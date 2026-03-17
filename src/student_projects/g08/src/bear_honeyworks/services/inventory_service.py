from typing import List

from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory


class InventoryService:
    def store(self, inventory: Inventory, jar: HoneyJar) -> None:
        inventory.add(jar)

    def take(self, inventory: Inventory, amount: int) -> List[HoneyJar]:
        return inventory.remove(amount)