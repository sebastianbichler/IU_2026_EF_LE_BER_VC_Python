"""Unit tests for services.py – subscription boxes and profit calculation."""

from datetime import datetime, timedelta

from models import Vegetable, Customer, Order
from services import generate_subscription_boxes, calculate_profit


def _make_customer():
    return Customer(name="Max", species="Hase", subscription_type="weekly")


def _make_vegetables(count=3):
    now = datetime.now()
    return [
        Vegetable(
            name=f"Gemüse_{i}",
            sort=f"Sorte_{i}",
            plant_date=now - timedelta(days=60),
            harvest_date=now - timedelta(days=5),
            bed_id=1,
            shelf_life_days=14,
            amount=10.0,
        )
        for i in range(count)
    ]


class TestGenerateSubscriptionBoxes:
    """Tests for generate_subscription_boxes()."""

    def test_returns_generator(self):
        """Should return a generator, not a list."""
        import types

        customer = _make_customer()
        vegs = _make_vegetables()
        result = generate_subscription_boxes(customer, vegs, datetime.now(), weeks=4)
        assert isinstance(result, types.GeneratorType)

    def test_correct_number_of_boxes(self):
        """Should generate exactly `weeks` boxes."""
        customer = _make_customer()
        vegs = _make_vegetables()
        boxes = list(
            generate_subscription_boxes(customer, vegs, datetime.now(), weeks=5)
        )
        assert len(boxes) == 5

    def test_box_has_correct_customer(self):
        """Each box should reference the correct customer."""
        customer = _make_customer()
        vegs = _make_vegetables()
        boxes = list(
            generate_subscription_boxes(customer, vegs, datetime.now(), weeks=2)
        )
        for box in boxes:
            assert box.customer.name == "Max"

    def test_box_vegetables_count(self):
        """First box should have 3 vegetables (3 + (0 % 3))."""
        customer = _make_customer()
        vegs = _make_vegetables(5)
        boxes = list(
            generate_subscription_boxes(customer, vegs, datetime.now(), weeks=3)
        )
        assert len(boxes[0].vegetables) == 3
        assert len(boxes[1].vegetables) == 4
        assert len(boxes[2].vegetables) == 5

    def test_box_price_scales_with_vegetables(self):
        """Price should increase with extra vegetables beyond 3."""
        customer = _make_customer()
        vegs = _make_vegetables(5)
        boxes = list(
            generate_subscription_boxes(
                customer, vegs, datetime.now(), weeks=3, price_per_box=15.0
            )
        )
        assert boxes[0].price == 15.0
        assert boxes[1].price == 17.0
        assert boxes[2].price == 19.0

    def test_delivery_dates_weekly(self):
        """Delivery dates should be one week apart."""
        customer = _make_customer()
        vegs = _make_vegetables()
        start = datetime(2026, 1, 1)
        boxes = list(
            generate_subscription_boxes(customer, vegs, start, weeks=3)
        )
        assert boxes[0].delivery_date == start
        assert boxes[1].delivery_date == start + timedelta(weeks=1)
        assert boxes[2].delivery_date == start + timedelta(weeks=2)


class TestCalculateProfit:
    """Tests for calculate_profit()."""

    def test_profit_with_orders(self):
        """Should calculate revenue, expenses, profit, and margin correctly."""
        now = datetime.now()
        customer = _make_customer()
        vegs = _make_vegetables(1)
        orders = [
            Order(customer=customer, vegetables=vegs, delivery_date=now, price=50.0),
            Order(customer=customer, vegetables=vegs, delivery_date=now, price=30.0),
        ]
        costs = {"Saatgut": 10.0, "Wasser": 5.0}
        result = calculate_profit(orders, costs)

        assert result["revenue"] == 80.0
        assert result["expenses"] == 15.0
        assert result["profit"] == 65.0
        assert round(result["profit_margin"], 2) == 81.25

    def test_profit_no_orders(self):
        """With no orders, revenue and profit should be 0."""
        result = calculate_profit([], {"Saatgut": 10.0})
        assert result["revenue"] == 0.0
        assert result["profit"] == -10.0
        assert result["profit_margin"] == 0.0

    def test_profit_no_costs(self):
        """With no costs, profit equals revenue."""
        now = datetime.now()
        customer = _make_customer()
        vegs = _make_vegetables(1)
        orders = [
            Order(customer=customer, vegetables=vegs, delivery_date=now, price=25.0),
        ]
        result = calculate_profit(orders, {})
        assert result["expenses"] == 0.0
        assert result["profit"] == 25.0
        assert result["profit_margin"] == 100.0
