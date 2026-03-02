from datetime import date
from typing import List
from src.student_projects.g05.src.models.inventory import InventoryItem
from src.student_projects.g05.src.models.order import Order
from src.student_projects.g05.src.models.delivery import Delivery
from src.student_projects.g05.src.models.supplier import Supplier


class Restaurant:

    def __init__(self, name: str):
        self.name = name
        self.inventory: List[InventoryItem] = []
        self.orders: List[Order] = []
        self.suppliers: List[Supplier] = []
        self.deliveries: List[Delivery] = []

    def add_supplier(self, supplier: Supplier) -> None:
        self.suppliers.append(supplier)

    def register_delivery(self, delivery: Delivery) -> None:
        delivery.execute_delivery()
        self.deliveries.append(delivery)
        self.inventory.extend(delivery.items)

    def add_inventory(self, item: InventoryItem) -> None:
        self.inventory.append(item)

    def place_order(self, order: Order) -> None:
        self._consume_inventory(order)
        self.orders.append(order)

    def _consume_inventory(self, order: Order) -> None:
        for order_item in order.items:
            required = order_item.required_fish_kg()

            for inventory_item in self.inventory:
                if (
                    inventory_item.fish == order_item.menu_item.fish
                    and not inventory_item.is_expired(date.today())
                    and inventory_item.amount_kg >= required
                ):
                    inventory_item.reduce_stock(required)
                    break
            else:
                raise Exception("Not enough inventory available")