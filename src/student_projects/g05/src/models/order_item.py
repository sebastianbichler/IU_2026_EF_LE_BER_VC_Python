from dataclasses import dataclass
from src.student_projects.g05.src.models.menu_item import MenuItem


@dataclass
class OrderItem:
    menu_item: MenuItem
    quantity: int

    def total_price(self) -> float:
        return self.menu_item.price * self.quantity

    def required_fish_kg(self) -> float:
        return self.menu_item.fish_required_kg * self.quantity
