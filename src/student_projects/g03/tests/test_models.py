"""Unit tests for models.py – Vegetable, Bed, Customer, Inventory."""

from datetime import datetime, timedelta

from models import Vegetable, Bed, Customer, Inventory, Order, SubscriptionBox


class TestVegetable:
    """Tests for Vegetable dataclass."""

    def _make_vegetable(self, harvest_days_ago=5, shelf_life_days=10):
        """Helper: create a Vegetable harvested N days ago."""
        now = datetime.now()
        return Vegetable(
            name="Karotte",
            sort="Nantaise",
            plant_date=now - timedelta(days=60),
            harvest_date=now - timedelta(days=harvest_days_ago),
            bed_id=1,
            shelf_life_days=shelf_life_days,
            amount=10.0,
        )

    def test_is_fresh_true(self):
        """Freshly harvested vegetable should be fresh."""
        veg = self._make_vegetable(harvest_days_ago=2, shelf_life_days=10)
        assert veg.is_fresh() is True

    def test_is_fresh_false(self):
        """Vegetable past shelf life should not be fresh."""
        veg = self._make_vegetable(harvest_days_ago=15, shelf_life_days=10)
        assert veg.is_fresh() is False

    def test_is_fresh_boundary(self):
        """Vegetable exactly at shelf life boundary should not be fresh."""
        veg = self._make_vegetable(harvest_days_ago=10, shelf_life_days=10)
        assert veg.is_fresh() is False

    def test_freshness_ratio_fresh(self):
        """Fresh vegetable should have ratio > 0."""
        veg = self._make_vegetable(harvest_days_ago=2, shelf_life_days=10)
        ratio = veg.freshness_ratio()
        assert 0.0 < ratio <= 1.0

    def test_freshness_ratio_expired(self):
        """Expired vegetable should have ratio == 0."""
        veg = self._make_vegetable(harvest_days_ago=20, shelf_life_days=10)
        assert veg.freshness_ratio() == 0.0

    def test_freshness_ratio_half(self):
        """Vegetable at half shelf life should have ratio ~0.5."""
        veg = self._make_vegetable(harvest_days_ago=5, shelf_life_days=10)
        ratio = veg.freshness_ratio()
        assert 0.4 <= ratio <= 0.6

    def test_freshness_ratio_before_harvest(self):
        """Vegetable with future harvest date should have ratio 1.0."""
        now = datetime.now()
        veg = Vegetable(
            name="Tomate",
            sort="Cherry",
            plant_date=now - timedelta(days=30),
            harvest_date=now + timedelta(days=5),
            bed_id=1,
            shelf_life_days=10,
            amount=5.0,
        )
        assert veg.freshness_ratio() == 1.0


class TestBed:
    """Tests for Bed dataclass."""

    def test_bed_creation(self):
        bed = Bed(id=1, name="Karottenbeet", size_m2=12.5)
        assert bed.id == 1
        assert bed.name == "Karottenbeet"
        assert bed.size_m2 == 12.5


class TestCustomer:
    """Tests for Customer dataclass."""

    def test_customer_str(self):
        customer = Customer(name="Max", species="Hase", subscription_type="weekly")
        assert "Max" in str(customer)
        assert "Hase" in str(customer)


class TestInventory:
    """Tests for Inventory dataclass."""

    def _make_fresh_vegetable(self):
        now = datetime.now()
        return Vegetable(
            name="Gurke",
            sort="Schlangengurke",
            plant_date=now - timedelta(days=30),
            harvest_date=now - timedelta(days=1),
            bed_id=1,
            shelf_life_days=14,
            amount=5.0,
        )

    def _make_expired_vegetable(self):
        now = datetime.now()
        return Vegetable(
            name="Salat",
            sort="Kopfsalat",
            plant_date=now - timedelta(days=60),
            harvest_date=now - timedelta(days=30),
            bed_id=2,
            shelf_life_days=7,
            amount=3.0,
        )

    def test_add_harvest(self):
        """add_harvest should add a Vegetable copy to inventory."""
        inv = Inventory()
        veg = self._make_fresh_vegetable()
        inv.add_harvest(veg, 10.0)
        assert len(inv.items) == 1
        assert inv.items[0].amount == 10.0
        assert inv.items[0].name == veg.name

    def test_get_fresh_items_returns_generator(self):
        """get_fresh_items should return a generator."""
        inv = Inventory()
        result = inv.get_fresh_items()
        import types

        assert isinstance(result, types.GeneratorType)

    def test_get_fresh_items(self):
        """get_fresh_items should yield only fresh items."""
        inv = Inventory()
        fresh = self._make_fresh_vegetable()
        expired = self._make_expired_vegetable()
        inv.items.extend([fresh, expired])

        fresh_list = list(inv.get_fresh_items())
        assert len(fresh_list) == 1
        assert fresh_list[0].name == "Gurke"

    def test_get_expired_items(self):
        """get_expired_items should yield only expired items."""
        inv = Inventory()
        fresh = self._make_fresh_vegetable()
        expired = self._make_expired_vegetable()
        inv.items.extend([fresh, expired])

        expired_list = list(inv.get_expired_items())
        assert len(expired_list) == 1
        assert expired_list[0].name == "Salat"

    def test_get_total_amount(self):
        """get_total_amount should sum all item amounts."""
        inv = Inventory()
        veg1 = self._make_fresh_vegetable()
        veg2 = self._make_expired_vegetable()
        inv.items.extend([veg1, veg2])

        total = inv.get_total_amount()
        assert total == veg1.amount + veg2.amount

    def test_get_total_amount_empty(self):
        """Empty inventory should have total amount 0."""
        inv = Inventory()
        assert inv.get_total_amount() == 0.0


class TestOrderStr:
    """Tests for Order and SubscriptionBox string representation."""

    def test_order_str(self):
        now = datetime.now()
        customer = Customer(name="Felix", species="Fuchs", subscription_type="monthly")
        veg = Vegetable(
            name="Tomate",
            sort="Cherry",
            plant_date=now,
            harvest_date=now,
            bed_id=1,
            shelf_life_days=7,
            amount=2.0,
        )
        order = Order(
            customer=customer,
            vegetables=[veg],
            delivery_date=now,
            price=9.99,
        )
        text = str(order)
        assert "Felix" in text
        assert "Tomate" in text

    def test_subscription_box_str(self):
        now = datetime.now()
        customer = Customer(name="Lina", species="Eule", subscription_type="weekly")
        veg = Vegetable(
            name="Paprika",
            sort="Rot",
            plant_date=now,
            harvest_date=now,
            bed_id=1,
            shelf_life_days=10,
            amount=3.0,
        )
        box = SubscriptionBox(
            customer=customer,
            vegetables=[veg],
            delivery_date=now,
            price=15.0,
        )
        text = str(box)
        assert "Lina" in text
        assert "Paprika" in text
