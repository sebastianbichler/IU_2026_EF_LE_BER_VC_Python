from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.services.production_service import ProductionService
from bear_honeyworks.services.inventory_service import InventoryService


def main() -> None:
    bear = Bear("Balou")
    inventory = Inventory()

    production = ProductionService()
    inventory_service = InventoryService()

    jar = production.produce(bear, "Waldhonig")
    inventory_service.store(inventory, jar)

    print(f"Produziert: {jar}")
    print(f"Lagerbestand: {len(inventory.jars)}")


if __name__ == "__main__":
    main()