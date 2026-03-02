from dataclasses import dataclass, field
from typing import List
from src.student_projects.g05.src.models.order_item import OrderItem


@dataclass
class Order:
    order_id: int
    items: List[OrderItem] = field(default_factory=list)

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)

    def total_amount(self) -> float:
        return sum(item.total_price() for item in self.items)
