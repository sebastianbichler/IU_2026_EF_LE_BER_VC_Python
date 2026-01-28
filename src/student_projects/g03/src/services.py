from datetime import datetime, timedelta
from typing import List, Generator, Dict
from itertools import islice, cycle

from models import Vegetable, Customer, SubscriptionBox, Order, Inventory

def generate_subscription_boxes(
    customer: Customer,
    available_vegetables: List[Vegetable],
    start_date: datetime,
    weeks: int = 12,
    price_per_box: float = 15.0
) -> Generator[SubscriptionBox, None, None]:
    veg_cycle = cycle(available_vegetables)
    
    for week in range(weeks):
        delivery_date = start_date + timedelta(weeks=week)
        
        num_vegetables = 3 + (week % 3)
        box_vegetables = list(islice(veg_cycle, num_vegetables))
        
        actual_price = price_per_box + (len(box_vegetables) - 3) * 2.0
        
        yield SubscriptionBox(
            customer=customer,
            vegetables=box_vegetables,
            delivery_date=delivery_date,
            price=actual_price
        )


def calculate_profit(orders: List[Order], costs: Dict[str, float]) -> Dict[str, float]:
    revenue = sum(map(lambda order: order.price, orders))
    expenses = sum(costs.values())
    profit = revenue - expenses
    
    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit,
        "profit_margin": (profit / revenue * 100) if revenue > 0 else 0.0
    }