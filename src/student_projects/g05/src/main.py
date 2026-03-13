import os
import logging
from datetime import datetime, timedelta

from core.restaurant import PenguEats

from models.fish import Fish
from models.recipe import Recipe
from models.menu_item import MenuItem
from models.inventory import InventoryItem
from models.order_item import OrderItem
from models.order import Order
from models.bill import Bill

from utils.mcmc_model import perform_bayesian_analysis, get_risk_metrics


# Disable C++ compiler (important for Windows without conda)
os.environ["PYTENSOR_FLAGS"] = "cxx="
logging.getLogger("pytensor").setLevel(logging.ERROR)


def main():
    print("=== PENGUEATS ENTERPRISE: ANALYTICS & OPERATIONS ===")

    # ---------------------------------------------------
    # Phase 1 – Supply Chain History (species deliveries)
    # ---------------------------------------------------

    supply_chain_history = [
        {"Lachs": 3, "Hering": 5, "Makrele": 2, "Krill": 10},
        {"Lachs": 4, "Hering": 3, "Makrele": 3, "Krill": 9},
        {"Lachs": 2, "Hering": 6, "Makrele": 2, "Krill": 8},
        {"Lachs": 5, "Hering": 4, "Makrele": 3, "Krill": 11},
        {"Lachs": 3, "Hering": 5, "Makrele": 2, "Krill": 9},
        {"Lachs": 4, "Hering": 4, "Makrele": 3, "Krill": 10},
        {"Lachs": 2, "Hering": 5, "Makrele": 2, "Krill": 8},
        {"Lachs": 5, "Hering": 3, "Makrele": 3, "Krill": 12},
        {"Lachs": 3, "Hering": 6, "Makrele": 2, "Krill": 9},
        {"Lachs": 4, "Hering": 4, "Makrele": 3, "Krill": 10},
    ]

    delivery_history = [sum(day.values()) for day in supply_chain_history]

    print("\n[Phase 1] Initiierung der Bayesianischen Inferenz")

    try:

        # ---------------------------------------------------
        # Phase 2 – Bayesian Demand Model (per fish)
        # ---------------------------------------------------

        print("\n[Phase 2] Analyse der Fischarten:")

        fish_delivery_history = {}

        for day in supply_chain_history:
            for fish, amount in day.items():
                fish_delivery_history.setdefault(fish, []).append(amount)

        fish_forecasts = {}

        for fish, history in fish_delivery_history.items():
            trace = perform_bayesian_analysis(history)

            mean_rate, risk_level, hdi = get_risk_metrics(
                trace,
                threshold=3
            )

            fish_forecasts[fish] = {
                "expected_supply": mean_rate,
                "risk_percent": risk_level,
                "interval": hdi
            }

            print(
                f" - {fish}: Erwartet {mean_rate:.2f} "
                f"(95% HDI {hdi}) | "
                f"Knappheitsrisiko {risk_level:.2f}%"
            )

        # ---------------------------------------------------
        # Price multiplier per fish
        # ---------------------------------------------------

        price_multipliers = {}

        for fish, data in fish_forecasts.items():

            risk = data["risk_percent"]

            if risk > 40:
                multiplier = 1.5
            elif risk > 25:
                multiplier = 1.3
            elif risk > 10:
                multiplier = 1.1
            else:
                multiplier = 1.0

            price_multipliers[fish] = multiplier

        print("\n[Preisstrategie basierend auf Versorgungsrisiken]")

        for fish, mult in price_multipliers.items():
            print(f" - {fish}: Preisfaktor {mult:.2f}")

        # ---------------------------------------------------
        # Phase 3 – Restaurant Setup
        # ---------------------------------------------------

        management = PenguEats()

        # ---------------------------------------------------
        # Fish Species
        # ---------------------------------------------------

        salmon = Fish("Lachs", 8.5, 0.15)
        herring = Fish("Hering", 5.0, 0.10)
        mackerel = Fish("Makrele", 6.5, 0.12)
        krill = Fish("Krill", 2.0, 0.05)

        # fish mapping
        fish_map = {
            "Lachs": salmon,
            "Hering": herring,
            "Makrele": mackerel,
            "Krill": krill,
        }
        # Inventory Setup
        today = datetime.now().date()

        management.inventory.extend([
            InventoryItem(salmon, 12, today + timedelta(days=5)),
            InventoryItem(herring, 11, today + timedelta(days=5)),
            InventoryItem(mackerel, 8, today + timedelta(days=5)),
            InventoryItem(krill, 17, today + timedelta(days=5)),
        ])

        # ---------------------------------------------------
        # Recipes
        # ---------------------------------------------------

        salmon_recipe = Recipe("Lachs Gericht", salmon, 0.3)
        herring_recipe = Recipe("Hering Gericht", herring, 0.25)
        mackerel_recipe = Recipe("Makrelen Gericht", mackerel, 0.35)
        krill_recipe = Recipe("Krill Gericht", krill, 0.2)

        # ---------------------------------------------------
        # Menu
        # ---------------------------------------------------

        management.add_menu_item(
            MenuItem("Lachs Teller", salmon_recipe, 18.0)
        )

        management.add_menu_item(
            MenuItem("Hering Spezial", herring_recipe, 14.0)
        )

        management.add_menu_item(
            MenuItem("Makrelen Platte", mackerel_recipe, 16.0)
        )

        management.add_menu_item(
            MenuItem("Krill Snack", krill_recipe, 8.0)
        )

        # ---------------------------------------------------
        # Order Simulation
        # ---------------------------------------------------

        print("\n[Phase 3] Operatives Tagesgeschäft und Auftragsabwicklung:")

        def simulate_order(customer_name, menu_item_name, quantity):

            menu_item = next(
                (item for item in management.menu if item.name == menu_item_name),
                None
            )

            if menu_item is None:
                print(f"Menüpunkt '{menu_item_name}' existiert nicht.")
                return

            fish_name = menu_item.recipe.fish.name

            multiplier = price_multipliers.get(fish_name, 1.0)

            adjusted_price = menu_item.price * multiplier

            print(
                f" - Preisberechnung: {menu_item.price:.2f} "
                f"x {multiplier:.2f} → {adjusted_price:.2f}"
            )

            order_item = OrderItem(menu_item, quantity)

            bill = Bill([order_item])

            order = Order(customer_name, [order_item], bill)

            management.place_order(order)

            print(
                f" Bestellung verarbeitet: "
                f"{customer_name} → {menu_item_name} "
                f"(x{quantity})"
            )

        simulate_order("Eisbär", "Lachs Teller", 2)
        simulate_order("Seehund", "Hering Spezial", 1)
        simulate_order("Walross", "Makrelen Platte", 1)
        simulate_order("Pinguin", "Krill Snack", 3)

        # ---------------------------------------------------
        # Phase 4 – Financial Summary
        # ---------------------------------------------------

        print("\n[Phase 4] Finanzübersicht:")

        print(
            f" - Gesamtumsatz: "
            f"{management.get_total_revenue():.2f}"
        )

        print(
            f" - Inventarstatus: "
            f"{management.get_inventory_status()}"
        )

        print("\n[Status] Simulation erfolgreich abgeschlossen.")

    except Exception as e:

        print(
            f"\n[Kritischer Fehler] Systemabbruch während "
            f"der Verarbeitung: {e}"
        )


if __name__ == "__main__":
    main()
