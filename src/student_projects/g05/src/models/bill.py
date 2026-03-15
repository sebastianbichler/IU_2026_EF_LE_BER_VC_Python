# bill.py
from dataclasses import dataclass
from typing import List

@dataclass
class Bill:
    order_items: "List['OrderItem']"  # string type hint avoids circular import
    tax_rate: float = 0.07

    def total_with_tax(self) -> float:
        return sum(item.total_price() for item in self.order_items) * (1 + self.tax_rate)
