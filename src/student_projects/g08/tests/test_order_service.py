# Test für die OrderService-Klasse, um sicherzustellen, dass die Verarbeitung von Bestellungen korrekt funktioniert, insbesondere in Bezug auf die Auswahl der Gläser mit der höchsten Qualität und die Handhabung von unzureichendem Lagerbestand.
from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.domain.order import Order
from bear_honeyworks.services.order_service import OrderService

# Testfunktion, die überprüft, ob die process_order-Methode der OrderService-Klasse die Gläser mit der höchsten Qualität zuerst ausliefert und diese korrekt aus dem Lager entfernt.
def test_process_order_removes_highest_quality_first() -> None:
    inventory = Inventory()
    inventory.jars = [
        HoneyJar(weight=0.5, sort="Waldhonig", quality=2, bear_name="Balou"),
        HoneyJar(weight=0.5, sort="Waldhonig", quality=5, bear_name="Benny"),
        HoneyJar(weight=0.5, sort="Waldhonig", quality=3, bear_name="Balou"),
    ]

    service = OrderService()
    order = Order(sort="Waldhonig", quantity=1)

    delivered_jars = service.process_order(order, inventory)

    assert len(delivered_jars) == 1
    assert delivered_jars[0].quality == 5
    assert delivered_jars[0].bear_name == "Benny"
    assert len(inventory.jars) == 2

# Testfunktion, die überprüft, ob die process_order-Methode der OrderService-Klasse eine leere Liste zurückgibt, wenn nicht genügend Gläser der gewünschten Sorte im Lager vorhanden sind, und dass das Lager in diesem Fall unverändert bleibt.
def test_process_order_returns_empty_list_if_not_enough_stock() -> None:
    inventory = Inventory()
    inventory.jars = [
        HoneyJar(weight=0.5, sort="Waldhonig", quality=2, bear_name="Balou"),
    ]

    service = OrderService()
    order = Order(sort="Waldhonig", quantity=2)

    delivered_jars = service.process_order(order, inventory)

    assert delivered_jars == []
    assert len(inventory.jars) == 1