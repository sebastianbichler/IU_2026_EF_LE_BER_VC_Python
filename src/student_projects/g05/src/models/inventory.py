from dataclasses import dataclass
from datetime import date
from src.student_projects.g05.src.models.fish import Fish


@dataclass
class InventoryItem:
    fish: Fish
    amount_kg: float
    expiration_date: date

    def is_expired(self, current_date: date) -> bool:
        return current_date > self.expiration_date

    def reduce_stock(self, amount: float) -> None:
        if amount > self.amount_kg:
            raise ValueError("Not enough stock available")
        self.amount_kg -= amount
