from dataclasses import dataclass
from src.student_projects.g05.src.models.order import Order


@dataclass
class Bill:
    order: Order
    tax_rate: float = 0.19

    def total_with_tax(self) -> float:
        return self.order.total_amount() * (1 + self.tax_rate)
