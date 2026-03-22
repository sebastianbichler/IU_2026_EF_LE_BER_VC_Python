import os
import logging
from datetime import date, timedelta

os.environ["PYTENSOR_FLAGS"] = "cxx="
logging.getLogger("pytensor").setLevel(logging.ERROR)

from flask import Flask, render_template, request, redirect, url_for, flash

from core.penguEats import PenguEats
from models.fish import Fish
from models.recipe import Recipe
from models.menu_item import MenuItem
from models.inventory_item import InventoryItem
from models.order_item import OrderItem
from models.order import Order
from models.bill import Bill
from utils.mcmc_model import perform_bayesian_analysis, get_risk_metrics

app = Flask(__name__)
app.secret_key = "pengueats-dev-key"


SUPPLY_CHAIN_HISTORY = [
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

ANALYSIS_CACHE = None

BASE_MENU_PRICES = {
    "Lachs Teller": 18.0,
    "Hering Spezial": 14.0,
    "Makrelen Platte": 16.0,
    "Krill Snack": 8.0,
}


def create_fish_map() -> dict[str, Fish]:
    return {
        "Lachs": Fish("Lachs", 8.5, 0.15),
        "Hering": Fish("Hering", 5.0, 0.10),
        "Makrele": Fish("Makrele", 6.5, 0.12),
        "Krill": Fish("Krill", 2.0, 0.05),
    }


def add_base_inventory(restaurant: PenguEats, fish_map: dict[str, Fish]) -> None:
    today = date.today()

    restaurant.inventory.extend([
        InventoryItem(fish_map["Lachs"], 12, today + timedelta(days=5)),
        InventoryItem(fish_map["Hering"], 11, today + timedelta(days=5)),
        InventoryItem(fish_map["Makrele"], 8, today + timedelta(days=5)),
        InventoryItem(fish_map["Krill"], 17, today + timedelta(days=5)),
    ])


def add_menu(restaurant: PenguEats, fish_map: dict[str, Fish]) -> None:
    restaurant.add_menu_item(MenuItem("Lachs Teller", Recipe("Lachs Gericht", fish_map["Lachs"], 0.3), 18.0))
    restaurant.add_menu_item(MenuItem("Hering Spezial", Recipe("Hering Gericht", fish_map["Hering"], 0.25), 14.0))
    restaurant.add_menu_item(MenuItem("Makrelen Platte", Recipe("Makrelen Gericht", fish_map["Makrele"], 0.35), 16.0))
    restaurant.add_menu_item(MenuItem("Krill Snack", Recipe("Krill Gericht", fish_map["Krill"], 0.2), 8.0))


def create_restaurant() -> tuple[PenguEats, dict[str, Fish]]:
    restaurant = PenguEats()
    fish_map = create_fish_map()
    add_base_inventory(restaurant, fish_map)
    add_menu(restaurant, fish_map)
    return restaurant, fish_map


restaurant, fish_map = create_restaurant()


def invalidate_analysis_cache() -> None:
    global ANALYSIS_CACHE
    ANALYSIS_CACHE = None


def get_inventory_summary() -> dict[str, float]:
    summary: dict[str, float] = {}

    for batch in restaurant.inventory:
        fish_name = batch.fish.name
        if fish_name not in summary:
            summary[fish_name] = 0.0
        summary[fish_name] += batch.amount_kg

    return summary


def get_recipe_recommendations() -> list[dict]:
    inventory = get_inventory_summary()
    recommendations: list[dict] = []

    for menu_item in restaurant.menu:
        fish_name = menu_item.recipe.fish.name
        required_kg = menu_item.recipe.fish_required_kg
        available_kg = inventory.get(fish_name, 0.0)

        if available_kg >= required_kg:
            recommendations.append({
                "dish": menu_item.name,
                "fish": fish_name,
                "required_kg": required_kg,
                "available_kg": available_kg,
                "max_portions": int(available_kg // required_kg),
                "price": menu_item.price,
            })

    return recommendations


def get_order_history() -> list[dict]:
    result: list[dict] = []

    for order in restaurant.orders:
        order_items = []
        for item in order.items:
            order_items.append({
                "menu_item_name": item.menu_item.name,
                "quantity": item.quantity,
                "single_price": item.menu_item.price,
                "total_price": item.total_price(),
            })

        result.append({
            "customer": order.customer,
            "order_items": order_items,
            "bill_total": order.bill.total_with_tax(),
        })

    return result


def get_supply_chain_totals() -> dict[str, float]:
    totals = {fish_name: 0.0 for fish_name in fish_map.keys()}

    for delivery in SUPPLY_CHAIN_HISTORY:
        for fish_name, amount in delivery.items():
            totals[fish_name] = totals.get(fish_name, 0.0) + amount

    return totals


def get_mcmc_analysis() -> dict[str, dict]:
    global ANALYSIS_CACHE

    if ANALYSIS_CACHE is not None:
        return ANALYSIS_CACHE

    fish_delivery_history: dict[str, list[int | float]] = {}

    for day in SUPPLY_CHAIN_HISTORY:
        for fish_name, amount in day.items():
            fish_delivery_history.setdefault(fish_name, []).append(amount)

    results: dict[str, dict] = {}

    for fish_name, history in fish_delivery_history.items():
        trace = perform_bayesian_analysis(history)
        mean_rate, risk_level, hdi = get_risk_metrics(trace, threshold=3)

        if risk_level > 40:
            multiplier = 1.5
            risk_label = "Kritisch"
        elif risk_level > 25:
            multiplier = 1.3
            risk_label = "Erhöht"
        elif risk_level > 10:
            multiplier = 1.1
            risk_label = "Beobachten"
        else:
            multiplier = 1.0
            risk_label = "Stabil"

        results[fish_name] = {
            "expected_supply": round(float(mean_rate), 2),
            "risk_percent": round(float(risk_level), 2),
            "interval_low": round(float(hdi[0]), 2),
            "interval_high": round(float(hdi[1]), 2),
            "price_multiplier": multiplier,
            "risk_label": risk_label,
        }

    ANALYSIS_CACHE = results
    return ANALYSIS_CACHE


def apply_analysis_prices_to_menu() -> None:
    analysis = get_mcmc_analysis()

    for menu_item in restaurant.menu:
        fish_name = menu_item.recipe.fish.name
        multiplier = analysis.get(fish_name, {}).get("price_multiplier", 1.0)
        base_price = BASE_MENU_PRICES.get(menu_item.name, menu_item.price)
        menu_item.price = round(base_price * multiplier, 2)


apply_analysis_prices_to_menu()


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        saldo=restaurant.balance,
        inventory=get_inventory_summary(),
        menu=restaurant.menu,
        recommendations=get_recipe_recommendations(),
        analysis=get_mcmc_analysis(),
        orders=get_order_history(),
        fish_names=list(fish_map.keys()),
        supply_totals=get_supply_chain_totals(),
    )


@app.route("/add_delivery", methods=["POST"])
def add_delivery():
    today = date.today()
    added_any = False

    for fish_name, fish in fish_map.items():
        raw_value = request.form.get(f"delivery_{fish_name}", "").strip()

        if not raw_value:
            continue

        try:
            amount_kg = float(raw_value)
        except ValueError:
            flash(f"Ungültige Menge für {fish_name}.", "error")
            return redirect(url_for("index"))

        if amount_kg < 0:
            flash(f"Die Menge für {fish_name} darf nicht negativ sein.", "error")
            return redirect(url_for("index"))

        if amount_kg == 0:
            continue

        restaurant.inventory.append(
            InventoryItem(
                fish=fish,
                amount_kg=amount_kg,
                expiry_date=today + timedelta(days=5)
            )
        )
        added_any = True

    if not added_any:
        flash("Bitte mindestens eine Liefermenge größer als 0 eingeben.", "error")
        return redirect(url_for("index"))

    flash("Großlieferung wurde ins Inventar übernommen.", "success")
    return redirect(url_for("index"))


@app.route("/rerun_analysis", methods=["POST"])
def rerun_analysis():
    current_inventory = get_inventory_summary()
    new_day = {}

    for fish_name in fish_map.keys():
        new_day[fish_name] = round(current_inventory.get(fish_name, 0.0), 2)

    SUPPLY_CHAIN_HISTORY.append(new_day)
    invalidate_analysis_cache()
    apply_analysis_prices_to_menu()

    flash("MCMC-Analyse wurde mit den aktuell hinzugefügten Daten neu berechnet und die Menüpreise wurden aktualisiert.", "success")
    return redirect(url_for("index"))


@app.route("/mock", methods=["POST"])
def load_mock_data():
    global restaurant, fish_map

    restaurant, fish_map = create_restaurant()

    try:
        menu_item = next((item for item in restaurant.menu if item.name == "Lachs Teller"), None)
        if menu_item is not None:
            order_item = OrderItem(menu_item, 2)
            bill = Bill([order_item])
            order = Order("Mock-Pinguin", [order_item], bill)
            restaurant.place_order(order)

        menu_item = next((item for item in restaurant.menu if item.name == "Krill Snack"), None)
        if menu_item is not None:
            order_item = OrderItem(menu_item, 3)
            bill = Bill([order_item])
            order = Order("Mock-Seehund", [order_item], bill)
            restaurant.place_order(order)
    except Exception as exc:
        flash(f"Mock-Daten teilweise geladen: {exc}", "error")
        return redirect(url_for("index"))

    invalidate_analysis_cache()
    apply_analysis_prices_to_menu()
    flash("Mock-Daten wurden geladen, Demo-Bestellungen erzeugt und Preise aktualisiert.", "success")
    return redirect(url_for("index"))


@app.route("/order_food", methods=["POST"])
def order_food():
    customer_name = request.form.get("customer_name", "").strip()
    menu_item_name = request.form.get("menu_item_name", "").strip()
    quantity_raw = request.form.get("quantity", "").strip()

    if not customer_name:
        flash("Bitte einen Kundennamen eingeben.", "error")
        return redirect(url_for("index"))

    try:
        quantity = int(quantity_raw)
    except ValueError:
        flash("Bitte eine gültige Anzahl eingeben.", "error")
        return redirect(url_for("index"))

    if quantity <= 0:
        flash("Die Anzahl muss größer als 0 sein.", "error")
        return redirect(url_for("index"))

    menu_item = next((item for item in restaurant.menu if item.name == menu_item_name), None)

    if menu_item is None:
        flash("Gericht nicht gefunden.", "error")
        return redirect(url_for("index"))

    try:
        order_item = OrderItem(menu_item, quantity)
        bill = Bill([order_item])
        order = Order(customer_name, [order_item], bill)
        restaurant.place_order(order)
    except Exception as exc:
        flash(str(exc), "error")
        return redirect(url_for("index"))

    flash(f"Bestellung aufgenommen: {customer_name} – {quantity}x {menu_item_name}.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)