# src/student_projects/g05/src/models/order.py
# order.py
from dataclasses import dataclass
from typing import List
from src.student_projects.g05.src.models.order_item import OrderItem
from src.student_projects.g05.src.models.bill import Bill

@dataclass
class Order:
    customer: str
    items: List[OrderItem]
    bill: Bill

    def total_items(self) -> int:
        """
        Returns the total number of individual items in this order.
        """
        return sum(item.quantity for item in self.items)

    def total_amount(self) -> float:
        """
        Returns the total price of all items in this order, using the bill.
        """
        return self.bill.total_with_tax()
