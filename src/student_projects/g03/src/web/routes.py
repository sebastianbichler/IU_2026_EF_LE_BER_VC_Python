"""Routen für die Web-App: Views und Formulare."""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for

import data_manager
from models import Vegetable, Bed, Customer, Order

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Zeigt die Startseite an."""
    return render_template("index.html")


@bp.route("/vegetables", methods=["GET", "POST"])
def vegetables():
    """Verarbeitet die Eingabe und Anzeige von Gemüse."""
    if request.method == "POST":
        try:
            name = request.form["name"]
            sort = request.form["sort"]
            bed_id = int(request.form["bed_id"])
            plant_date = datetime.strptime(request.form["plant_date"], "%Y-%m-%d")
            harvest_date = datetime.strptime(request.form["harvest_date"], "%Y-%m-%d")
            shelf_life = int(request.form["shelf_life"])
            amount = float(request.form["amount"])

            veg = Vegetable(
                name=name,
                sort=sort,
                plant_date=plant_date,
                harvest_date=harvest_date,
                bed_id=bed_id,
                shelf_life_days=shelf_life,
                amount=amount,
            )
            data_manager.vegetables.append(veg)
            data_manager.save_data()
            return redirect(url_for("main.vegetables"))
        except ValueError as e:
            return f"Error: {e}", 400

    return render_template(
        "vegetables.html",
        vegetables=data_manager.vegetables,
        beds=data_manager.beds,
    )


@bp.route("/beds", methods=["GET", "POST"])
def beds():
    """Verwaltet das Anlegen und Auslesen der Beete."""
    if request.method == "POST":
        try:
            if not data_manager.beds:
                new_id = 1
            else:
                new_id = max(b.id for b in data_manager.beds) + 1

            name = request.form["name"]
            size = float(request.form["size"])

            bed = Bed(id=new_id, name=name, size_m2=size)
            data_manager.beds.append(bed)
            data_manager.save_data()
            return redirect(url_for("main.beds"))
        except ValueError as e:
            return f"Error: {e}", 400

    return render_template("beds.html", beds=data_manager.beds)


@bp.route("/inventory", methods=["GET", "POST"])
def inventory():
    """Steuert die Einlagerung und Bestandsprüfung."""
    if request.method == "POST":
        try:
            veg_idx = int(request.form["veg_idx"])
            amount = float(request.form["amount"])

            if 0 <= veg_idx < len(data_manager.vegetables):
                veg = data_manager.vegetables[veg_idx]
                data_manager.inventory.add_harvest(veg, amount)
                data_manager.save_data()
            return redirect(url_for("main.inventory"))
        except ValueError:
            return "Error", 400

    fresh_items = list(data_manager.inventory.get_fresh_items())
    expired_items = list(data_manager.inventory.get_expired_items())
    total_amount = data_manager.inventory.get_total_amount()

    return render_template(
        "inventory.html",
        fresh_items=fresh_items,
        expired_items=expired_items,
        total_amount=total_amount,
        vegetables=data_manager.vegetables,
    )


@bp.route("/customers", methods=["GET", "POST"])
def customers():
    """Nimmt neue Kunden auf und listet Bestandskunden."""
    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        sub_type = request.form["subscription_type"]

        customer = Customer(name=name, species=species, subscription_type=sub_type)
        data_manager.customers.append(customer)
        data_manager.save_data()
        return redirect(url_for("main.customers"))

    return render_template("customers.html", customers=data_manager.customers)


@bp.route("/orders", methods=["GET", "POST"])
def orders():
    """Erstellt Bestellungen und berechnet Lieferdaten."""
    if request.method == "POST":
        try:
            cust_idx = int(request.form["customer_idx"])
            veg_indices = request.form.getlist("veg_indices")
            days = int(request.form["days"])
            price = float(request.form["price"])

            if 0 <= cust_idx < len(data_manager.customers):
                customer = data_manager.customers[cust_idx]

                selected_vegs = []
                for idx_str in veg_indices:
                    idx = int(idx_str)
                    if 0 <= idx < len(data_manager.vegetables):
                        selected_vegs.append(data_manager.vegetables[idx])

                order = Order(
                    customer=customer,
                    vegetables=selected_vegs,
                    delivery_date=datetime.now() + timedelta(days=days),
                    price=price,
                )
                data_manager.orders.append(order)
                data_manager.save_data()
                return redirect(url_for("main.orders"))
        except ValueError:
            return "Error", 400

    return render_template(
        "orders.html",
        orders=data_manager.orders,
        customers=data_manager.customers,
        vegetables=data_manager.vegetables,
    )


@bp.route("/finances")
def finances():
    """Kalkuliert den Umsatz aus den Bestellungen."""
    revenue = sum(o.price for o in data_manager.orders)
    return render_template(
        "finance.html",
        revenue=revenue,
        orders=data_manager.orders,
    )


@bp.route("/sensors", methods=["GET", "POST"])
def sensors():
    """Führt den Leistungsvergleich der Sensordaten aus."""
    result_eager = None
    result_lazy = None
    error = None

    if request.method == "POST":
        try:
            from sensor_benchmark import benchmark_eager, benchmark_lazy

            bed_id_raw = request.form.get("bed_id", "1").strip() or "1"
            bed_id = int(bed_id_raw)

            num_raw = (request.form.get("num_readings") or "10000").strip().replace(".", "").replace(",", "").replace(" ", "") or "10000"
            num_readings = int(num_raw)
            num_readings = max(1, min(num_readings, 500_000))

            result_eager = benchmark_eager(bed_id, num_readings)
            result_lazy = benchmark_lazy(bed_id, num_readings)
        except ValueError as e:
            error = f"Ungültiger Wert. Bitte nur Zahlen eingeben (z. B. 10000). Fehler: {e}"
        except Exception as e:
            error = str(e)

    return render_template(
        "sensors.html",
        beds=data_manager.beds,
        result_eager=result_eager,
        result_lazy=result_lazy,
        error=error,
    )
