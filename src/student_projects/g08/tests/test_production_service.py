# Test für die ProductionService-Klasse, um sicherzustellen, dass die Produktion von Honig korrekt funktioniert, insbesondere in Bezug auf die Erstellung eines HoneyJar-Objekts mit den richtigen Attributen basierend auf den Eingaben.
from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.honey import HoneyJar
from bear_honeyworks.services.production_service import ProductionService


def test_produce_honey_returns_honeyjar() -> None:
    bear = Bear("Balou")
    service = ProductionService()

    jar = service.produce(bear, "Waldhonig")

    assert isinstance(jar, HoneyJar)
    assert jar.sort == "Waldhonig"
    assert jar.bear_name == "Balou"