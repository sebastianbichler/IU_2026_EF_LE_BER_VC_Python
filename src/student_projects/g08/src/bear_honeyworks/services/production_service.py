from bear_honeyworks.domain.bear import Bear
from bear_honeyworks.domain.honey import HoneyJar


class ProductionService:
    def produce(self, bear: Bear, sort: str) -> HoneyJar:
        return bear.produce_honey(sort)