import os
import sys
import pytest
from datetime import datetime

# Füge g03 Root zum Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.models import Vegetable, Customer, Order
from src.services import generate_subscription_boxes, calculate_profit

def test_03_services_subscription_box_generation_with_prices():
    """Prüft die korrekte Generierung von Abo-Boxen (Anzahl Gemüse) und die zugehörige dynamische Preisberechnung."""
    customer = Customer(name="Hase Felix", species="Feldhase", subscription_type="Premium")
    now = datetime.now()
    
    veg1 = Vegetable("Möhre", "Orange", now, now, 1, 10, 1)
    veg2 = Vegetable("Rettich", "Weiß", now, now, 1, 10, 1)
    veg3 = Vegetable("Kohl", "Grün", now, now, 1, 10, 1)
    veg4 = Vegetable("Salat", "Kopf", now, now, 1, 5, 1)
    
    available = [veg1, veg2, veg3, veg4]
    
    boxes = list(generate_subscription_boxes(customer, available, start_date=now, weeks=4, price_per_box=15.0))
    
    assert len(boxes) == 4
    assert boxes[0].price == 15.0  # 3 Gemüse -> Basispreis
    assert len(boxes[0].vegetables) == 3
    assert boxes[1].price == 17.0  # 4 Gemüse -> +2€
    assert len(boxes[1].vegetables) == 4
    assert boxes[2].price == 19.0  # 5 Gemüse -> +4€
    assert len(boxes[2].vegetables) == 5

def test_04_services_profit_and_margin_calculation():
    """Prüft die korrekte Berechnung von Umsatz, Ausgaben, Profit und der Gewinnmarge."""
    customer = Customer(name="Test", species="Test", subscription_type="Basic")
    now = datetime.now()
    
    o1 = Order(customer, [], now, 50.0)
    o2 = Order(customer, [], now, 30.0)
    
    costs = {
        "Samen": 10.0,
        "Wasser": 15.0
    }
    
    profit_data = calculate_profit([o1, o2], costs)
    
    assert profit_data["revenue"] == 80.0
    assert profit_data["expenses"] == 25.0
    assert profit_data["profit"] == 55.0
    assert profit_data["profit_margin"] == (55.0 / 80.0) * 100
