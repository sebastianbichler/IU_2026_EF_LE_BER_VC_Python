from bear_honeyworks.domain.honey import HoneyJar


class Bear:
    def __init__(self, name: str) -> None:
        self.name = name

    def produce_honey(self, sort: str) -> HoneyJar:
        return HoneyJar(weight=0.5, sort=sort, quality=3)