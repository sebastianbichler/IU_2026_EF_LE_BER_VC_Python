# Import der benötigten Module und Typen für die Datenverarbeitung
from typing import List

from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.domain.inventory import Inventory
from bear_honeyworks.domain.order import Order

# Die OrderService-Klasse verwaltet die Verarbeitung von Bestellungen, einschließlich der Überprüfung der Verfügbarkeit von Honiggläsern im Lager und der Priorisierung von Gläsern mit höherer Qualität bei der Auslieferung.
class OrderService:

    # Die can_process_order-Methode überprüft, ob genügend Honiggläser der gewünschten Sorte im Lager vorhanden sind, um die Bestellung zu erfüllen.
    def can_process_order(self, order: Order, inventory: Inventory) -> bool:
        matching_jars = [jar for jar in inventory.jars if jar.sort == order.sort]
        return len(matching_jars) >= order.quantity
    # Die process_order-Methode verarbeitet eine Bestellung, indem sie die passenden Honiggläser aus dem Lager entfernt und zurückgibt. Dabei werden zuerst die Gläser mit der höchsten Qualität ausgeliefert. Wenn die Bestellung nicht erfüllt werden kann, wird eine leere Liste zurückgegeben.
    def process_order(self, order: Order, inventory: Inventory) -> List[HoneyJar]:
        # Zuerst wird überprüft, ob die Bestellung erfüllt werden kann. Wenn nicht, wird eine leere Liste zurückgegeben.
        if not self.can_process_order(order, inventory):
            return []
        # Es werden alle Honiggläser im Lager gefiltert, um diejenigen zu finden, die der gewünschten Sorte entsprechen. Gleichzeitig werden die anderen Gläser separat gehalten.
        matching_jars = [jar for jar in inventory.jars if jar.sort == order.sort]
        other_jars = [jar for jar in inventory.jars if jar.sort != order.sort]

        sorted_matching = sorted(
            matching_jars,
            key=lambda jar: jar.quality,
            reverse=True,
        )
        # Es werden die Gläser mit der höchsten Qualität ausgewählt, um die Bestellung zu erfüllen, und die verbleibenden passenden Gläser werden im Lager behalten.
        delivered_jars = sorted_matching[: order.quantity]
        remaining_matching = sorted_matching[order.quantity :]
        # Das Lager wird aktualisiert, indem die ausgelieferten Gläser entfernt und die anderen Gläser sowie die verbleibenden passenden Gläser wieder hinzugefügt werden.
        inventory.jars = other_jars + remaining_matching
        return delivered_jars