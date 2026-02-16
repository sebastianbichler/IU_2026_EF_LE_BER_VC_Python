import os
import json
from datetime import datetime
from models import Vegetable, Bed, Customer, Inventory, Order

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

vegetables = []
beds = []
customers = []
inventory = Inventory()
orders = []

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
    # We need to access the global variables to modify them
    # But in Python, modifying a list in place (append, clear, extend) doesn't require global keyword
    # However, reassigning the variable does.
    # Here we clear and extend to avoid reassigning the global reference if imported elsewhere
    # But wait, simplified approach: we can just use the globals.
    
    # Actually, to make it robust for imports, we should probably return nothing and just update the module-level variables.
    # But since other modules import 'vegetables' etc., we must mutate the existing objects or rely on the fact that
    # imports are references.
    
    # Let's stick to the current pattern but make sure we target the module-level variables.
    
    global vegetables, beds, customers, inventory, orders
    
    # Clear existing lists to avoid duplicates on reload if that ever happens
    vegetables.clear()
    beds.clear()
    customers.clear()
    inventory.items.clear()
    orders.clear()

    file_path = os.path.join(DATA_DIR, "rabbitfarm_data.json")
    if not os.path.exists(file_path):
        return
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for v in data.get("vegetables", []):
            vegetables.append(Vegetable(
                name=v["name"],
                sort=v["sort"],
                plant_date=str_to_datetime(v["plant_date"]),
                harvest_date=str_to_datetime(v["harvest_date"]),
                bed_id=v["bed_id"],
                shelf_life_days=v["shelf_life_days"],
                amount=v["amount"]
            ))
        
        for b in data.get("beds", []):
            beds.append(Bed(
                id=b["id"],
                name=b["name"],
                size_m2=b["size_m2"]
            ))
        
        for c in data.get("customers", []):
            customers.append(Customer(
                name=c["name"],
                species=c["species"],
                subscription_type=c["subscription_type"]
            ))
        
        for v_data in data.get("inventory", []):
            inventory.items.append(Vegetable(
                name=v_data["name"],
                sort=v_data["sort"],
                plant_date=str_to_datetime(v_data["plant_date"]),
                harvest_date=str_to_datetime(v_data["harvest_date"]),
                bed_id=v_data["bed_id"],
                shelf_life_days=v_data["shelf_life_days"],
                amount=v_data["amount"]
            ))
        
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
            orders.append(Order(
                customer=customer,
                vegetables=veg_list,
                delivery_date=str_to_datetime(o_data["delivery_date"]),
                price=o_data["price"]
            ))
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
        print("Fehler beim Laden: " + str(e))
