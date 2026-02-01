from datetime import datetime
from typing import List, Optional, Generator
from dataclasses import dataclass, field


@dataclass
class Vegetable:
    name: str
    sort: str
    plant_date: datetime
    harvest_date: datetime
    bed_id: int
    shelf_life_days: int
    amount: float = 1.0
    
    def is_fresh(self, current_date: Optional[datetime] = None) -> bool:
        if current_date is None:
            current_date = datetime.now()
        days_since_harvest = (current_date - self.harvest_date).days
        return days_since_harvest < self.shelf_life_days
    
    def freshness_ratio(self, current_date: Optional[datetime] = None) -> float:
        if current_date is None:
            current_date = datetime.now()
        days_since_harvest = (current_date - self.harvest_date).days
        if days_since_harvest < 0:
            return 1.0
        return max(0.0, 1.0 - (days_since_harvest / self.shelf_life_days))


@dataclass
class Bed:
    id: int
    name: str
    size_m2: float


@dataclass
class Customer:
    name: str
    species: str
    subscription_type: str
    
    def __str__(self) -> str:
        return f"{self.name} ({self.species})"


@dataclass
class SubscriptionBox:
    customer: Customer
    vegetables: List[Vegetable]
    delivery_date: datetime
    price: float
    
    def __str__(self) -> str:
        veg_names = ", ".join([v.name for v in self.vegetables])
        return f"Box für {self.customer.name} am {self.delivery_date.strftime('%d.%m.%Y')}: {veg_names} ({self.price:.2f}€)"


@dataclass
class Order:
    customer: Customer
    vegetables: List[Vegetable]
    delivery_date: datetime
    price: float
    
    def __str__(self) -> str:
        veg_names = ", ".join([v.name for v in self.vegetables])
        return f"Bestellung von {self.customer.name}: {veg_names} ({self.price:.2f}€)"


@dataclass
class Inventory:
    items: List[Vegetable] = field(default_factory=list)
    
    def add_harvest(self, vegetable: Vegetable, amount: float) -> None:
        veg = Vegetable(
            name=vegetable.name,
            sort=vegetable.sort,
            plant_date=vegetable.plant_date,
            harvest_date=vegetable.harvest_date,
            bed_id=vegetable.bed_id,
            shelf_life_days=vegetable.shelf_life_days,
            amount=amount
        )
        self.items.append(veg)
    
    def get_fresh_items(self, current_date: Optional[datetime] = None) -> Generator[Vegetable, None, None]:
        if current_date is None:
            current_date = datetime.now()
        for item in self.items:
            if item.is_fresh(current_date):
                yield item
    
    def get_expired_items(self, current_date: Optional[datetime] = None) -> Generator[Vegetable, None, None]:
        if current_date is None:
            current_date = datetime.now()
        for item in self.items:
            if not item.is_fresh(current_date):
                yield item
    
    def get_total_amount(self) -> float:
        return sum(item.amount for item in self.items)
