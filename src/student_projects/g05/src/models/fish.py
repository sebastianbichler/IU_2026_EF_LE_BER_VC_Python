from dataclasses import dataclass


@dataclass
class Fish:
    name: str
    base_cost_per_kg: float
    supplier_price_variance: float

    def __post_init__(self):
        if self.base_cost_per_kg <= 0:
            raise ValueError("base_cost_per_kg must be positive")
        if self.supplier_price_variance < 0:
            raise ValueError("supplier_price_variance cannot be negative")
        