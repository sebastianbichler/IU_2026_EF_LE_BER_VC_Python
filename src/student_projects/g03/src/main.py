import sys
import os
import json
import time
import tracemalloc
from datetime import datetime, timedelta
from itertools import islice
from functools import reduce

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .models import Vegetable, Bed, Customer, Inventory, Order
    from .sensors import stream_soil_moisture
    from .services import generate_subscription_boxes, calculate_profit
except ImportError:
    from models import Vegetable, Bed, Customer, Inventory, Order
    from sensors import stream_soil_moisture
    from services import generate_subscription_boxes, calculate_profit

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

vegetables = []
beds = []
customers = []
inventory = Inventory()
orders = []


def get_next_bed_id():
    if not beds:
        return 1
    return max(map(lambda b: b.id, beds)) + 1


def datetime_to_str(dt):
    return dt.isoformat()


def str_to_datetime(s):
    return datetime.fromisoformat(s)


def save_data():
    data = {
        "vegetables": [
            {
                "name": v.name,
                "sort": v.sort,
                "plant_date": datetime_to_str(v.plant_date),
                "harvest_date": datetime_to_str(v.harvest_date),
                "bed_id": v.bed_id,
                "shelf_life_days": v.shelf_life_days,
                "amount": v.amount
            }
            for v in vegetables
        ],
        "beds": [
            {
                "id": b.id,
                "name": b.name,
                "size_m2": b.size_m2
            }
            for b in beds
        ],
        "customers": [
            {
                "name": c.name,
                "species": c.species,
                "subscription_type": c.subscription_type
            }
            for c in customers
        ],
        "inventory": [
            {
                "name": v.name,
                "sort": v.sort,
                "plant_date": datetime_to_str(v.plant_date),
                "harvest_date": datetime_to_str(v.harvest_date),
                "bed_id": v.bed_id,
                "shelf_life_days": v.shelf_life_days,
                "amount": v.amount
            }
            for v in inventory.items
        ],
        "orders": [
            {
                "customer_name": o.customer.name,
                "customer_species": o.customer.species,
                "customer_subscription_type": o.customer.subscription_type,
                "vegetables": [
                    {
                        "name": v.name,
                        "sort": v.sort,
                        "plant_date": datetime_to_str(v.plant_date),
                        "harvest_date": datetime_to_str(v.harvest_date),
                        "bed_id": v.bed_id,
                        "shelf_life_days": v.shelf_life_days,
                        "amount": v.amount
                    }
                    for v in o.vegetables
                ],
                "delivery_date": datetime_to_str(o.delivery_date),
                "price": o.price
            }
            for o in orders
        ]
    }
    file_path = os.path.join(DATA_DIR, "rabbitfarm_data.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_data():
    global vegetables, beds, customers, inventory, orders
    file_path = os.path.join(DATA_DIR, "rabbitfarm_data.json")
    if not os.path.exists(file_path):
        return
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        vegetables = [
            Vegetable(
                name=v["name"],
                sort=v["sort"],
                plant_date=str_to_datetime(v["plant_date"]),
                harvest_date=str_to_datetime(v["harvest_date"]),
                bed_id=v["bed_id"],
                shelf_life_days=v["shelf_life_days"],
                amount=v["amount"]
            )
            for v in data.get("vegetables", [])
        ]
        
        beds = [
            Bed(
                id=b["id"],
                name=b["name"],
                size_m2=b["size_m2"]
            )
            for b in data.get("beds", [])
        ]
        
        customers = [
            Customer(
                name=c["name"],
                species=c["species"],
                subscription_type=c["subscription_type"]
            )
            for c in data.get("customers", [])
        ]
        
        inventory = Inventory()
        for v_data in data.get("inventory", []):
            veg = Vegetable(
                name=v_data["name"],
                sort=v_data["sort"],
                plant_date=str_to_datetime(v_data["plant_date"]),
                harvest_date=str_to_datetime(v_data["harvest_date"]),
                bed_id=v_data["bed_id"],
                shelf_life_days=v_data["shelf_life_days"],
                amount=v_data["amount"]
            )
            inventory.items.append(veg)
        
        orders = []
        for o_data in data.get("orders", []):
            customer = Customer(
                name=o_data["customer_name"],
                species=o_data["customer_species"],
                subscription_type=o_data["customer_subscription_type"]
            )
            veg_list = [
                Vegetable(
                    name=v["name"],
                    sort=v["sort"],
                    plant_date=str_to_datetime(v["plant_date"]),
                    harvest_date=str_to_datetime(v["harvest_date"]),
                    bed_id=v["bed_id"],
                    shelf_life_days=v["shelf_life_days"],
                    amount=v["amount"]
                )
                for v in o_data["vegetables"]
            ]
            order = Order(
                customer=customer,
                vegetables=veg_list,
                delivery_date=str_to_datetime(o_data["delivery_date"]),
                price=o_data["price"]
            )
            orders.append(order)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
        print("Fehler beim Laden: " + str(e))


def print_menu():
    print()
    print("RabbitFarm")
    print("1. Gemuese verwalten")
    print("2. Beete verwalten")
    print("3. Lagerbestaende")
    print("4. Kunden und Abos")
    print("5. Einnahmen Ausgaben")
    print("6. Sensordaten")
    print("0. Beenden")


def format_vegetable(veg, idx):
    return (str(idx) + ". " + veg.name + " (" + veg.sort + ")\n" +
            "   Beet: " + str(veg.bed_id) + ", Menge: " + str(veg.amount) + " kg\n" +
            "   Pflanzung: " + veg.plant_date.strftime('%Y-%m-%d') + "\n" +
            "   Ernte: " + veg.harvest_date.strftime('%Y-%m-%d'))


def list_vegetables():
    print()
    if not vegetables:
        print("Keine Gemuese")
        return
    formatted = map(lambda x: format_vegetable(x[1], x[0]), enumerate(vegetables, 1))
    print("\n".join(formatted))


def add_vegetable():
    print()
    print("Neues Gemuese")
    if not beds:
        print("Keine Beete vorhanden. Bitte erstelle zuerst ein Beet.")
        return
    try:
        name = input("Name: ")
        sort = input("Sorte: ")
        print("Verfuegbare Beete:")
        formatted_beds = map(lambda x: str(x[0]) + ". " + x[1].name + " (ID: " + str(x[1].id) + ")", enumerate(beds, 1))
        print("\n".join(formatted_beds))
        bed_idx = int(input("Welches Beet? (Nummer): ")) - 1
        if bed_idx < 0 or bed_idx >= len(beds):
            print("Ungueltige Auswahl")
            return
        bed_id = beds[bed_idx].id
        print("Pflanzdatum (YYYY-MM-DD):")
        plant_date = datetime.strptime(input(), "%Y-%m-%d")
        print("Erntedatum (YYYY-MM-DD):")
        harvest_date = datetime.strptime(input(), "%Y-%m-%d")
        shelf_life = int(input("Haltbarkeit Tage: "))
        amount = float(input("Menge kg: "))
        
        veg = Vegetable(
            name=name, sort=sort, plant_date=plant_date,
            harvest_date=harvest_date, bed_id=bed_id,
            shelf_life_days=shelf_life, amount=amount
        )
        vegetables.append(veg)
        save_data()
        print(name + " hinzugefuegt")
    except ValueError as e:
        print("Fehler:", e)


def manage_vegetables():
    menu_map = {
        "1": add_vegetable,
        "2": list_vegetables,
        "3": lambda: None
    }
    while True:
        print()
        print("Gemuese verwalten")
        print("1. Hinzufuegen")
        print("2. Anzeigen")
        print("3. Zurueck")
        choice = input("Option: ")
        if choice == "3":
            break
        func = menu_map.get(choice)
        if func:
            func()
        else:
            print("Ungueltig")


def add_bed():
    print()
    print("Neues Beet")
    try:
        bed_id = get_next_bed_id()
        name = input("Name: ")
        size = float(input("Groesse m2: "))
        bed = Bed(id=bed_id, name=name, size_m2=size)
        beds.append(bed)
        save_data()
        print(name + " hinzugefuegt (ID: " + str(bed_id) + ")")
    except ValueError:
        print("Fehler")


def get_bed_vegetables(bed_id):
    return filter(lambda v: v.bed_id == bed_id, vegetables)


def format_bed(bed):
    result = "Beet " + str(bed.id) + ": " + bed.name + "\n"
    result += "  Groesse: " + str(bed.size_m2) + " m2\n"
    bed_veg = list(get_bed_vegetables(bed.id))
    if bed_veg:
        result += "  Gemuese:\n"
        veg_lines = map(lambda v: "    " + v.name + " (" + str(v.amount) + " kg)", bed_veg)
        result += "\n".join(veg_lines)
    else:
        result += "  Kein Gemuese"
    return result


def list_beds():
    print()
    if not beds:
        print("Keine Beete")
        return
    formatted = map(format_bed, beds)
    print("\n".join(formatted))


def manage_beds():
    menu_map = {
        "1": add_bed,
        "2": list_beds,
        "3": lambda: None
    }
    while True:
        print()
        print("Beete verwalten")
        print("1. Hinzufuegen")
        print("2. Anzeigen")
        print("3. Zurueck")
        choice = input("Option: ")
        if choice == "3":
            break
        func = menu_map.get(choice)
        if func:
            func()
        else:
            print("Ungueltig")


def format_inventory_item(veg):
    freshness = veg.freshness_ratio() * 100
    return veg.name + ": " + str(veg.amount) + " kg (Frische: " + str(round(freshness, 1)) + "%)"


def format_expired_item(veg):
    return veg.name + ": " + str(veg.amount) + " kg (ABGELAUFEN)"


def show_inventory():
    print()
    print("Lagerbestaende")
    if not inventory.items:
        print("Lager leer")
        return
    print("Gesamtmenge: " + str(inventory.get_total_amount()) + " kg")
    print()
    print("Frische Gemuese:")
    fresh_items = list(inventory.get_fresh_items())
    if fresh_items:
        formatted = map(format_inventory_item, fresh_items)
        print("\n".join(map(lambda s: "  " + s, formatted)))
    else:
        print("  Keine")
    print()
    print("Abgelaufene Gemuese:")
    expired_items = list(inventory.get_expired_items())
    if expired_items:
        formatted = map(format_expired_item, expired_items)
        print("\n".join(map(lambda s: "  " + s, formatted)))
    else:
        print("  Keine")


def add_to_inventory():
    print()
    print("Ernte ins Lager")
    if not vegetables:
        print("Keine Gemuese vorhanden")
        return
    list_vegetables()
    try:
        idx = int(input("Welches Gemuese? (Nummer): ")) - 1
        if 0 <= idx < len(vegetables):
            veg = vegetables[idx]
            amount = float(input("Menge kg: "))
            inventory.add_harvest(veg, amount)
            save_data()
            print(str(amount) + " kg " + veg.name + " ins Lager")
        else:
            print("Ungueltige Nummer")
    except ValueError:
        print("Fehler")


def manage_inventory():
    menu_map = {
        "1": show_inventory,
        "2": add_to_inventory,
        "3": lambda: None
    }
    while True:
        print()
        print("Lagerverwaltung")
        print("1. Anzeigen")
        print("2. Ernte hinzufuegen")
        print("3. Zurueck")
        choice = input("Option: ")
        if choice == "3":
            break
        func = menu_map.get(choice)
        if func:
            func()
        else:
            print("Ungueltig")


def add_customer():
    print()
    print("Neuer Kunde")
    name = input("Name: ")
    species = input("Tierart: ")
    sub_type = input("Abo-Typ: ")
    customer = Customer(name=name, species=species, subscription_type=sub_type)
    customers.append(customer)
    save_data()
    print(name + " hinzugefuegt")


def format_customer(cust, idx):
    return str(idx) + ". " + cust.name + " (" + cust.species + ")"


def format_subscription_box(box, week_num):
    veg_names = ", ".join(map(lambda v: v.name, box.vegetables))
    return ("Woche " + str(week_num) + " (" + box.delivery_date.strftime('%Y-%m-%d') + "):\n" +
            "  Gemuese: " + veg_names + "\n" +
            "  Preis: " + str(box.price) + " Euro")


def create_subscription_box():
    print()
    print("Abo-Kiste erstellen")
    if not customers:
        print("Keine Kunden")
        return
    if not vegetables:
        print("Keine Gemuese")
        return
    print("Kunden:")
    formatted_customers = map(lambda x: format_customer(x[1], x[0]), enumerate(customers, 1))
    print("\n".join(formatted_customers))
    try:
        cust_idx = int(input("Welcher Kunde? (Nummer): ")) - 1
        if 0 <= cust_idx < len(customers):
            customer = customers[cust_idx]
            weeks = int(input("Anzahl Wochen: "))
            start_date = datetime.now()
            subscription_stream = generate_subscription_boxes(
                customer=customer,
                available_vegetables=vegetables,
                start_date=start_date,
                weeks=weeks
            )
            print("Abo-Kisten:")
            boxes = list(islice(subscription_stream, weeks))
            formatted_boxes = map(lambda x: format_subscription_box(x[1], x[0]), enumerate(boxes, 1))
            print("\n".join(formatted_boxes))
        else:
            print("Ungueltige Nummer")
    except ValueError:
        print("Fehler")


def parse_vegetable_indices(indices_str):
    return map(lambda s: int(s.strip()) - 1, indices_str.split(","))


def create_order():
    print()
    print("Neue Bestellung")
    if not customers:
        print("Keine Kunden")
        return
    if not vegetables:
        print("Keine Gemuese")
        return
    print("Kunden:")
    formatted_customers = map(lambda x: format_customer(x[1], x[0]), enumerate(customers, 1))
    print("\n".join(formatted_customers))
    try:
        cust_idx = int(input("Welcher Kunde? (Nummer): ")) - 1
        if 0 <= cust_idx < len(customers):
            customer = customers[cust_idx]
            list_vegetables()
            veg_indices = input("Welche Gemuese? (Nummern durch Komma): ")
            indices = list(parse_vegetable_indices(veg_indices))
            veg_list = list(filter(lambda x: x[0] in indices and 0 <= x[0] < len(vegetables), enumerate(vegetables)))
            veg_list = list(map(lambda x: x[1], veg_list))
            if not veg_list:
                print("Keine Gemuese ausgewaehlt")
                return
            days = int(input("Lieferung in Tagen: "))
            price = float(input("Preis Euro: "))
            order = Order(
                customer=customer,
                vegetables=veg_list,
                delivery_date=datetime.now() + timedelta(days=days),
                price=price
            )
            orders.append(order)
            save_data()
            print("Bestellung erstellt: " + str(order))
        else:
            print("Ungueltige Nummer")
    except ValueError:
        print("Fehler")


def manage_customers():
    menu_map = {
        "1": add_customer,
        "2": create_subscription_box,
        "3": create_order,
        "4": lambda: print("Kunden:\n" + "\n".join(map(lambda x: format_customer(x[1], x[0]) + " - " + x[1].subscription_type, enumerate(customers, 1)))),
        "5": lambda: None
    }
    while True:
        print()
        print("Kunden und Abos")
        print("1. Kunde hinzufuegen")
        print("2. Abo-Kiste erstellen")
        print("3. Bestellung erstellen")
        print("4. Kunden anzeigen")
        print("5. Zurueck")
        choice = input("Option: ")
        if choice == "5":
            break
        func = menu_map.get(choice)
        if func:
            func()
        else:
            print("Ungueltig")


def show_finances():
    print()
    print("Einnahmen Ausgaben")
    if not orders:
        print("Keine Bestellungen")
        return
    print("Bestellungen:")
    formatted_orders = map(lambda x: str(x[0]) + ". " + str(x[1]), enumerate(orders, 1))
    print("\n".join(formatted_orders))
    total_revenue = reduce(lambda acc, order: acc + order.price, orders, 0.0)
    print("Gesamteinnahmen: " + str(total_revenue) + " Euro")
    print()
    print("Ausgaben eingeben:")
    cost_types = ["Saatgut", "Duenger", "Wasser", "Arbeitszeit"]
    
    def get_cost(cost_type):
        try:
            amount = input(cost_type + " (Euro, Enter fuer 0): ")
            return float(amount) if amount else 0.0
        except ValueError:
            return 0.0
    
    costs = dict(map(lambda ct: (ct, get_cost(ct)), cost_types))
    profit_data = calculate_profit(orders, costs)
    print()
    print("Ergebnis:")
    print("  Einnahmen: " + str(profit_data['revenue']) + " Euro")
    print("  Ausgaben: " + str(profit_data['expenses']) + " Euro")
    print("  Gewinn: " + str(profit_data['profit']) + " Euro")
    print("  Gewinnmarge: " + str(profit_data['profit_margin']) + "%")


def process_eager(data_list, threshold_low=35.0):
    filtered = [d for d in data_list if d["moisture"] < threshold_low or d["moisture"] > 80.0]
    irrigation = [{"bed_id": d["bed_id"], "moisture": d["moisture"], 
                   "irrigation_need": max(0, min(100, 100 - d["moisture"]))} 
                  for d in filtered]
    return irrigation


def process_lazy(data_gen, threshold_low=35.0, max_items=None):
    filtered = filter(lambda d: d["moisture"] < threshold_low or d["moisture"] > 80.0, data_gen)
    irrigation = map(lambda d: {
        "bed_id": d["bed_id"],
        "moisture": d["moisture"],
        "irrigation_need": max(0, min(100, 100 - d["moisture"]))
    }, filtered)
    if max_items:
        irrigation = islice(irrigation, max_items)
    return list(irrigation)


def benchmark_eager(bed_id, num_readings, base_moisture=50.0):
    tracemalloc.start()
    start_time = time.perf_counter()
    
    moisture_stream = stream_soil_moisture(bed_id=bed_id, base_moisture=base_moisture)
    data_list = list(islice(moisture_stream, num_readings))
    result = process_eager(data_list)
    
    elapsed_time = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    data_size = sys.getsizeof(data_list)
    for item in data_list[:100]:
        data_size += sys.getsizeof(item)
    
    return {
        "time": elapsed_time,
        "peak_memory_mb": peak / 1024 / 1024,
        "data_size_mb": data_size / 1024 / 1024,
        "result_count": len(result)
    }


def benchmark_lazy(bed_id, num_readings, base_moisture=50.0):
    tracemalloc.start()
    start_time = time.perf_counter()
    
    moisture_stream = stream_soil_moisture(bed_id=bed_id, base_moisture=base_moisture)
    limited_stream = islice(moisture_stream, num_readings)
    result = process_lazy(limited_stream)
    
    elapsed_time = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    gen_size = sys.getsizeof(limited_stream)
    
    return {
        "time": elapsed_time,
        "peak_memory_mb": peak / 1024 / 1024,
        "data_size_mb": gen_size / 1024 / 1024,
        "result_count": len(result)
    }


def show_sensor_data():
    print()
    print("Sensordaten - Eager vs Lazy Vergleich")
    if not beds:
        print("Keine Beete vorhanden")
        return
    try:
        bed_id = int(input("Beet-ID: "))
        num_readings = int(input("Anzahl Messwerte: "))
        
        print()
        print("Teste EAGER Evaluation (Listen im Speicher)...")
        result_eager = benchmark_eager(bed_id, num_readings)
        
        print("Teste LAZY Evaluation (Generatoren)...")
        result_lazy = benchmark_lazy(bed_id, num_readings)
        
        print()
        print("=" * 50)
        print("ERGEBNISSE")
        print("=" * 50)
        print()
        print("EAGER (Listen):")
        print("  Laufzeit: " + str(round(result_eager["time"], 4)) + " Sekunden")
        print("  RAM Peak: " + str(round(result_eager["peak_memory_mb"], 2)) + " MB")
        print("  Daten-Groesse: " + str(round(result_eager["data_size_mb"], 2)) + " MB")
        print("  Gefilterte Eintraege: " + str(result_eager["result_count"]))
        print()
        print("LAZY (Generatoren):")
        print("  Laufzeit: " + str(round(result_lazy["time"], 4)) + " Sekunden")
        print("  RAM Peak: " + str(round(result_lazy["peak_memory_mb"], 2)) + " MB")
        print("  Daten-Groesse: " + str(round(result_lazy["data_size_mb"], 4)) + " MB")
        print("  Gefilterte Eintraege: " + str(result_lazy["result_count"]))
        print()
        print("VERGLEICH:")
        time_diff = result_eager["time"] - result_lazy["time"]
        memory_diff = result_eager["peak_memory_mb"] - result_lazy["peak_memory_mb"]
        if time_diff > 0:
            print("  Lazy ist " + str(round(time_diff / result_eager["time"] * 100, 1)) + "% schneller")
        else:
            print("  Eager ist " + str(round(abs(time_diff) / result_lazy["time"] * 100, 1)) + "% schneller")
        print("  Lazy spart " + str(round(memory_diff, 2)) + " MB RAM")
        print("=" * 50)
        
    except ValueError:
        print("Fehler")


def main():
    load_data()
    menu_map = {
        "1": manage_vegetables,
        "2": manage_beds,
        "3": manage_inventory,
        "4": manage_customers,
        "5": show_finances,
        "6": show_sensor_data,
        "0": lambda: None
    }
    print("RabbitFarm")
    print("Daten werden gespeichert in: " + DATA_DIR)
    while True:
        print_menu()
        choice = input("Option: ")
        if choice == "0":
            save_data()
            print("Tschuess")
            sys.exit(0)
        func = menu_map.get(choice)
        if func:
            func()
        else:
            print("Ungueltig")


if __name__ == "__main__":
    main()
