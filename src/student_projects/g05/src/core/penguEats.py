from datetime import date

from src.student_projects.g05.src.models.order_item import OrderItem
from src.student_projects.g05.src.models.bill import Bill


class PenguEats:

    def __init__(self):

        self.inventory = []        # list[InventoryItem]
        self.menu = []             # list[MenuItem]
        self.orders = []           # list[Order]

        self.balance = 0.0
        self.rent = 15.0

    # --------------------------------------------------
    # Scientific pricing model
    # --------------------------------------------------

    def apply_scientific_forecast(self, mean_supply, supply_risk):

        print("\n--- Strategische Analyse der Lieferkette ---")
        print(f"Erwarteter Lieferumfang: {mean_supply:.2f} | Risiko-Level: {supply_risk:.2f}%")

        if supply_risk > 30:
            print("Status: Kritisches Lieferrisiko – Preise werden erhöht.")
            return 1.2
        else:
            print("Status: Lieferkette stabil – Standardpreise.")
            return 1.0

    # --------------------------------------------------
    # Menu management
    # --------------------------------------------------

    def add_menu_item(self, menu_item):
        self.menu.append(menu_item)

    # --------------------------------------------------
    # Inventory management
    # --------------------------------------------------

    def remove_expired_inventory(self):

        today = date.today()

        valid_batches = []

        for batch in self.inventory:

            if batch.expiry_date < today:
                print(f"⚠ WARNUNG: {batch.fish.name} Charge abgelaufen und entfernt.")
            else:
                valid_batches.append(batch)

        self.inventory = valid_batches

    # --------------------------------------------------
    # Inventory consumption
    # --------------------------------------------------

    def _consume_inventory(self, fish, required_kg):

        remaining = required_kg

        for batch in self.inventory:

            if batch.fish.name != fish.name:
                continue

            if batch.amount_kg <= 0:
                continue

            usable = min(batch.amount_kg, remaining)

            batch.amount_kg -= usable
            remaining -= usable

            if remaining <= 0:
                return True

        return False

    # --------------------------------------------------
    # Order processing
    # --------------------------------------------------

    def place_order(self, order):

        self.remove_expired_inventory()

        for order_item in order.items:

            recipe = order_item.menu_item.recipe

            fish = recipe.fish
            required_kg = recipe.fish_required_kg * order_item.quantity

            success = self._consume_inventory(fish, required_kg)

            if not success:
                raise Exception(f"Nicht genug {fish.name} im Inventar")

        self.orders.append(order)

        revenue = order.bill.total_with_tax()
        self.balance += revenue

    # --------------------------------------------------
    # Financial statistics
    # --------------------------------------------------

    def get_total_revenue(self):

        total = 0.0

        for order in self.orders:
            total += order.bill.total_with_tax()

        return total

    # --------------------------------------------------
    # Inventory overview
    # --------------------------------------------------

    def get_inventory_status(self):

        status = {}

        for batch in self.inventory:

            fish_name = batch.fish.name

            if fish_name not in status:
                status[fish_name] = 0

            status[fish_name] += batch.amount_kg

        return status
