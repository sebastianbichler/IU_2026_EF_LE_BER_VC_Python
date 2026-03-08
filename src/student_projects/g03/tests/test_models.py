import os
import sys
import pytest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.models import Vegetable, Bed, Customer, SubscriptionBox, Order, Inventory

def test_01_models_vegetable_freshness_calculation():
    """Prüft die korrekte Berechnung der Frische (is_fresh) und des Frische-Verhältnisses (freshness_ratio) eines Gemüses."""
    now = datetime.now()
    # Frisch: Vor 2 Tagen geerntet, 5 Tage haltbar
    fresh_veg = Vegetable(
        name="Karotte", sort="Süß", plant_date=now - timedelta(days=60),
        harvest_date=now - timedelta(days=2), bed_id=1, shelf_life_days=5
    )
    assert fresh_veg.is_fresh(now) is True
    assert fresh_veg.freshness_ratio(now) == 0.6  # (1 - 2/5) = 0.6

    # Abgelaufen: Vor 6 Tagen geerntet, 5 Tage haltbar
    old_veg = Vegetable(
        name="Lauch", sort="Grün", plant_date=now - timedelta(days=60),
        harvest_date=now - timedelta(days=6), bed_id=1, shelf_life_days=5
    )
    assert old_veg.is_fresh(now) is False
    assert old_veg.freshness_ratio(now) == 0.0

def test_02_models_inventory_management_and_filtering():
    """Prüft das Hinzufügen von Ernten zum Inventar sowie das Filtern nach frischen und abgelaufenen Beständen."""
    inventory = Inventory()
    now = datetime.now()
    
    veg1 = Vegetable("Salat", "Eisberg", now, now, 1, 3, 10.0)
    inventory.add_harvest(veg1, 10.0)
    
    assert len(inventory.items) == 1
    assert inventory.get_total_amount() == 10.0
    
    fresh_items = list(inventory.get_fresh_items(now))
    assert len(fresh_items) == 1
    
    expired_items = list(inventory.get_expired_items(now + timedelta(days=5)))
    assert len(expired_items) == 1
