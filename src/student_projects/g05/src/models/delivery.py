from dataclasses import dataclass, field
from datetime import date
from typing import List
from src.student_projects.g05.src.models.inventory_item import InventoryItem
from src.student_projects.g05.src.models.supplier import Supplier


@dataclass
class Delivery:
    supplier: Supplier
    delivery_date: date
    items: List[InventoryItem] = field(default_factory=list)

    def execute_delivery(self) -> None:
        if not self.supplier.delivery_successful():
            raise Exception("Delivery failed")

    def add_item(self, item: InventoryItem) -> None:
        self.items.append(item)
