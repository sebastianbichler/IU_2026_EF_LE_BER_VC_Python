from typing import List

from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory


class InventoryRepository:
    def load(self) -> List[HoneyJar]:
        return []

    def save(self, inventory: Inventory) -> List[HoneyJar]:
        return inventory.jars