from pathlib import Path

from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.domain.order import Order
from bear_honeyworks.io.json_store import load_json, save_json
from bear_honeyworks.services.inventory_service import InventoryService
from bear_honeyworks.services.order_service import OrderService
from bear_honeyworks.services.production_service import ProductionService


def test_complete_workflow_with_json_persistence(tmp_path: Path) -> None:
    inventory_file = tmp_path / "inventory.json"
    orders_file = tmp_path / "orders.json"

    # Leere Startdateien anlegen
    save_json(str(inventory_file), [])
    save_json(str(orders_file), [])

    # Services initialisieren
    production_service = ProductionService()
    inventory_service = InventoryService()
    order_service = OrderService()

    # Domänenobjekte
    bear = Bear("Balou")
    inventory = Inventory()

    # Honig produzieren
    jar = production_service.produce(bear, "Waldhonig")
    custom_jar = HoneyJar(
        weight=0.5,
        sort=jar.sort,
        quality=5,
        bear_name=bear.name,
    )

    # Ins Lager legen
    inventory_service.store(inventory, custom_jar)
    assert len(inventory.jars) == 1

    # Inventory als JSON speichern
    save_json(str(inventory_file), [h.__dict__ for h in inventory.jars])

    # Inventory wieder laden
    loaded_inventory_data = load_json(str(inventory_file))
    loaded_inventory = Inventory()
    loaded_inventory.jars = [HoneyJar(**item) for item in loaded_inventory_data]

    assert len(loaded_inventory.jars) == 1
    assert loaded_inventory.jars[0].sort == "Waldhonig"
    assert loaded_inventory.jars[0].bear_name == "Balou"

    # Bestellung ausführen
    order = Order(sort="Waldhonig", quantity=1)
    delivered_jars = order_service.process_order(order, loaded_inventory)

    assert len(delivered_jars) == 1
    assert delivered_jars[0].quality == 5
    assert len(loaded_inventory.jars) == 0

    # Bestellung als JSON speichern
    save_json(str(orders_file), [order.__dict__])

    loaded_orders_data = load_json(str(orders_file))
    assert len(loaded_orders_data) == 1
    assert loaded_orders_data[0]["sort"] == "Waldhonig"
    assert loaded_orders_data[0]["quantity"] == 1