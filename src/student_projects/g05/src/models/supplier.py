from dataclasses import dataclass
from typing import Dict
import random
from src.student_projects.g05.src.models.fish import Fish


@dataclass
class Supplier:
    name: str
    fish_price_list: Dict[str, float]
    price_volatility: float
    reliability: float
    average_delay_days: float
    quality_factor: float

    def get_price(self, fish: Fish) -> float:
        if fish.name not in self.fish_price_list:
            raise ValueError(f"{fish.name} not supplied by {self.name}")

        base_price = self.fish_price_list[fish.name]
        stochastic_price = random.gauss(base_price, self.price_volatility)
        return max(0.0, stochastic_price)

    def delivery_successful(self) -> bool:
        return random.random() < self.reliability

    def delivery_delay(self) -> int:
        delay = random.gauss(self.average_delay_days, 1)
        return max(0, int(delay))
