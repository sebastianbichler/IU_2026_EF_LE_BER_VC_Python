# Import der benötigten Module und Typen für die Datenverarbeitung
from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.honey import HoneyJar

# Die ProductionService-Klasse bietet eine Methode zur Honigproduktion, die einen Bear und die gewünschte Honigsorte als Eingabe erhält und ein HoneyJar-Objekt zurückgibt, das von dem Bear produziert wurde.
class ProductionService:
    def produce(self, bear: Bear, sort: str) -> HoneyJar:
        return bear.produce_honey(sort)