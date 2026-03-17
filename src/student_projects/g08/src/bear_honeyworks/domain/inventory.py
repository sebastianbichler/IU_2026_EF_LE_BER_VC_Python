from typing import List
from bear_honeyworks.domain.honey import HoneyJar


class Inventory:
    def __init__(self) -> None:
        self.jars: List[HoneyJar] = []

    def add(self, jar: HoneyJar) -> None:
        self.jars.append(jar)

    def remove(self, amount: int) -> List[HoneyJar]:
        removed = self.jars[:amount]
        self.jars = self.jars[amount:]
        return removed