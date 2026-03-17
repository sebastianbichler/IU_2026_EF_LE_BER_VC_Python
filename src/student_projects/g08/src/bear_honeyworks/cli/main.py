# Import der benötigten Domänenklassen und Services
from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.services.production_service import ProductionService
from bear_honeyworks.services.inventory_service import InventoryService


def main() -> None:
    
    #Erzeugung eines Bären und eines Inventars
    bear = Bear("Balou")
    inventory = Inventory()

    # Produktion eines Honigglases und Lagerung im Inventar
    production = ProductionService()
    inventory_service = InventoryService()

    # Honig produzieren und im Inventar speichern
    jar = production.produce(bear, "Waldhonig")
    inventory_service.store(inventory, jar)

    # Ausgabe der Ergebnisse
    print(f"Produziert: {jar}")
    print(f"Lagerbestand: {len(inventory.jars)}")


if __name__ == "__main__":
    main()