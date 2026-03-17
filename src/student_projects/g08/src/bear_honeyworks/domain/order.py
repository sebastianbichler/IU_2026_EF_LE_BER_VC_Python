# Import der benötigten Domänenklasse
from dataclasses import dataclass

# Die Klasse Order repräsentiert eine Bestellung mit der gewünschten Honigsorte und der Menge.
@dataclass
class Order:
    sort: str
    quantity: int