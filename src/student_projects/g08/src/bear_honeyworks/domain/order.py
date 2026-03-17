from dataclasses import dataclass


@dataclass
class Order:
    sort: str
    quantity: int