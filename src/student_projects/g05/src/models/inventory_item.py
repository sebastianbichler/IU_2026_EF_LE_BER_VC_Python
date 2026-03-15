from dataclasses import dataclass
from datetime import date

from src.student_projects.g05.src.models.fish import Fish


@dataclass
class InventoryItem:
    fish: Fish
    amount_kg: float
    expiry_date: date

    def reduce_stock(self, amount: float):
        """
        Reduces inventory by a given amount.
        """

        if amount > self.amount_kg:
            raise ValueError(
                f"Not enough {self.fish.name} in inventory"
            )

        self.amount_kg -= amount

    def is_expired(self, today: date) -> bool:
        """
        Returns True if the item is expired.
        """

        return today > self.expiry_date
