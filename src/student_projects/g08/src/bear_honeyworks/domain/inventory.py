# Import der benötigten Domänenklassen und Services
from typing import List
from bear_honeyworks.domain.honey import HoneyJar

# Die Klasse Inventory repräsentiert das Inventar der Honiggläser, das Funktionen zum Hinzufügen und Entfernen von Gläsern bietet.
class Inventory:
    # Konstruktor, der eine leere Liste von Honiggläsern initialisiert.
    def __init__(self) -> None:
        self.jars: List[HoneyJar] = []

    # Methode zum Hinzufügen eines Honigglases zum Inventar.
    def add(self, jar: HoneyJar) -> None:
        self.jars.append(jar)

    # Methode zum Entfernen einer bestimmten Anzahl von Honiggläsern aus dem Inventar.
    def remove(self, amount: int) -> List[HoneyJar]:
        removed = self.jars[:amount]
        self.jars = self.jars[amount:]
        return removed