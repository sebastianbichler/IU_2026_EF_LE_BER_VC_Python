from bear_honeyworks.domain.order import Order
from bear_honeyworks.domain.inventory import Inventory


class OrderService:
    def process_order(self, order: Order, inventory: Inventory) -> bool:
        if len(inventory.jars) >= order.quantity:
            inventory.remove(order.quantity)
            return True
        return False