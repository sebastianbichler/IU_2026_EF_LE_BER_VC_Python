# Import der benötigten Domänenklasse
from bear_honeyworks.domain.honey import HoneyJar


class Bear:
    # Konstruktor mit Typannotation
    def __init__(self, name: str) -> None:
        self.name = name

    # Methode zur Honigproduktion mit Rückgabetypannotation
    def produce_honey(self, sort: str) -> HoneyJar:
        return HoneyJar(
            weight=0.5,
            sort=sort,
            quality=3,
            bear_name=self.name,
        )