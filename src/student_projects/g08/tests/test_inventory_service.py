# Test für die InventoryService-Klasse, um sicherzustellen, dass das Hinzufügen eines HoneyJar-Objekts zum Inventory korrekt funktioniert.
from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.services.inventory_service import InventoryService

# Testfunktion, die überprüft, ob die store-Methode der InventoryService-Klasse ein HoneyJar-Objekt korrekt zum Inventory hinzufügt.
def test_store_adds_honeyjar_to_inventory() -> None:
    inventory = Inventory()
    service = InventoryService()

    jar = HoneyJar(
        weight=0.5,
        sort="Waldhonig",
        quality=4,
        bear_name="Balou",
    )

    service.store(inventory, jar)

    assert len(inventory.jars) == 1
    assert inventory.jars[0].sort == "Waldhonig"
    assert inventory.jars[0].bear_name == "Balou"