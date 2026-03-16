"""
Integrationstests für RabbitFarm.

Jeder Test deckt einen modulübergreifenden Workflow ab und ist
den Anforderungen aus dem Bericht (REQ-01 bis REQ-15) zugeordnet.
"""

from datetime import datetime, timedelta
from itertools import islice

from models import Vegetable, Bed, Customer, Inventory, Order
from services import generate_subscription_boxes, calculate_profit
from sensors import stream_soil_moisture
from sensor_benchmark import (
    process_eager,
    process_lazy,
    benchmark_eager,
    benchmark_lazy,
)


class TestIntegration01BedVegetableWorkflow:
    """INT-01: Beet anlegen -> Gemüse anlegen -> bed_id korrekt.

    Deckt ab: REQ-01 (Beet-Verwaltung), REQ-02 (Gemüsekatalog), REQ-03 (Pflanzplanung).
    """

    def test_vegetable_linked_to_bed(self):
        bed = Bed(id=1, name="Karottenbeet", size_m2=10.0)
        now = datetime.now()
        veg = Vegetable(
            name="Karotte",
            sort="Nantaise",
            plant_date=now - timedelta(days=30),
            harvest_date=now - timedelta(days=2),
            bed_id=bed.id,
            shelf_life_days=14,
            amount=20.0,
        )
        assert veg.bed_id == bed.id
        assert veg.name == "Karotte"

    def test_multiple_vegetables_per_bed(self):
        bed = Bed(id=2, name="Mischbeet", size_m2=15.0)
        now = datetime.now()
        vegetables = [
            Vegetable(
                name=f"Gemüse_{i}",
                sort=f"Sorte_{i}",
                plant_date=now - timedelta(days=40),
                harvest_date=now - timedelta(days=3),
                bed_id=bed.id,
                shelf_life_days=10,
                amount=5.0,
            )
            for i in range(3)
        ]
        for v in vegetables:
            assert v.bed_id == bed.id
        assert len(vegetables) == 3


class TestIntegration02InventoryWorkflow:
    """INT-02: Gemüse anlegen -> Ernte einlagern -> Frische prüfen -> Gesamtmenge.

    Deckt ab: REQ-04 (Bestandsüberwachung), REQ-05 (Haltbarkeitslogik), REQ-06 (Bestandsabfrage).
    """

    def test_harvest_and_freshness(self):
        now = datetime.now()
        inv = Inventory()

        fresh_veg = Vegetable(
            name="Gurke",
            sort="Schlangengurke",
            plant_date=now - timedelta(days=40),
            harvest_date=now - timedelta(days=2),
            bed_id=1,
            shelf_life_days=14,
            amount=5.0,
        )
        inv.add_harvest(fresh_veg, 8.0)

        expired_veg = Vegetable(
            name="Salat",
            sort="Kopfsalat",
            plant_date=now - timedelta(days=60),
            harvest_date=now - timedelta(days=30),
            bed_id=2,
            shelf_life_days=7,
            amount=3.0,
        )
        inv.add_harvest(expired_veg, 4.0)

        assert len(inv.items) == 2

        fresh_items = list(inv.get_fresh_items())
        expired_items = list(inv.get_expired_items())

        assert len(fresh_items) == 1
        assert fresh_items[0].name == "Gurke"
        assert fresh_items[0].amount == 8.0

        assert len(expired_items) == 1
        assert expired_items[0].name == "Salat"

        assert inv.get_total_amount() == 12.0


class TestIntegration03OrderFinanceWorkflow:
    """INT-03: Kunde anlegen -> Bestellung aufgeben -> Gewinn berechnen.

    Deckt ab: REQ-07 (Kunden-Datenbank), REQ-09 (Bestellabwicklung),
            REQ-10 (Einnahmen-Berechnung), REQ-11 (Gewinn-/Verlustrechnung).
    """

    def test_order_and_profit(self):
        now = datetime.now()

        customer = Customer(name="Felix", species="Fuchs", subscription_type="monthly")

        veg1 = Vegetable(
            name="Tomate",
            sort="Cherry",
            plant_date=now - timedelta(days=50),
            harvest_date=now - timedelta(days=3),
            bed_id=1,
            shelf_life_days=10,
            amount=10.0,
        )
        veg2 = Vegetable(
            name="Paprika",
            sort="Rot",
            plant_date=now - timedelta(days=45),
            harvest_date=now - timedelta(days=2),
            bed_id=1,
            shelf_life_days=12,
            amount=5.0,
        )

        order1 = Order(
            customer=customer,
            vegetables=[veg1, veg2],
            delivery_date=now + timedelta(days=2),
            price=25.0,
        )
        order2 = Order(
            customer=customer,
            vegetables=[veg1],
            delivery_date=now + timedelta(days=5),
            price=12.0,
        )

        orders = [order1, order2]
        costs = {"Saatgut": 5.0, "Wasser": 3.0, "Dünger": 2.0}

        result = calculate_profit(orders, costs)

        assert result["revenue"] == 37.0
        assert result["expenses"] == 10.0
        assert result["profit"] == 27.0
        assert result["profit_margin"] > 0


class TestIntegration04SensorBenchmarkWorkflow:
    """INT-04: Sensordaten streamen -> Eager + Lazy Benchmark -> Ergebnisse vergleichen.

    Deckt ab: REQ-13 (Sensordaten-Stream), REQ-14 (Generatorbasierte Verarbeitung),
            REQ-15 (Performance-Benchmark).
    """

    def test_sensor_stream_and_benchmark(self):
        bed_id = 1
        num_readings = 10_000

        stream = stream_soil_moisture(bed_id=bed_id)
        sample = list(islice(stream, 10))
        assert len(sample) == 10
        assert all("moisture" in s for s in sample)

        eager_result = benchmark_eager(bed_id, num_readings)
        lazy_result = benchmark_lazy(bed_id, num_readings)

        assert eager_result["time"] > 0
        assert lazy_result["time"] > 0
        assert eager_result["result_count"] >= 0
        assert lazy_result["result_count"] >= 0
        assert eager_result["peak_memory_mb"] >= 0
        assert lazy_result["peak_memory_mb"] >= 0

    def test_eager_lazy_produce_comparable_counts(self):
        """Beide Ansätze filtern ungefähr dieselbe Menge an Elementen."""
        bed_id = 1
        num_readings = 5_000

        data = list(islice(stream_soil_moisture(bed_id=bed_id), num_readings))
        eager_result = process_eager(data)
        lazy_result = process_lazy(iter(data))

        assert len(eager_result) == len(lazy_result)


class TestIntegration05SubscriptionBoxWorkflow:
    """INT-05: Abo-Kisten generieren -> Korrekte Zuordnung und Anzahl.

    Deckt ab: REQ-07 (Kunden-Datenbank), REQ-08 (Abo-Kisten-System).
    """

    def test_subscription_box_generation(self):
        now = datetime.now()

        customer = Customer(name="Bella", species="Dachs", subscription_type="weekly")
        vegetables = [
            Vegetable(
                name=f"Gemüse_{i}",
                sort=f"Sorte_{i}",
                plant_date=now - timedelta(days=40),
                harvest_date=now - timedelta(days=2),
                bed_id=1,
                shelf_life_days=14,
                amount=10.0,
            )
            for i in range(5)
        ]

        boxes = list(
            generate_subscription_boxes(
                customer, vegetables, start_date=now, weeks=4, price_per_box=15.0
            )
        )

        assert len(boxes) == 4

        for box in boxes:
            assert box.customer.name == "Bella"
            assert len(box.vegetables) >= 3
            assert box.price >= 15.0

        for i in range(1, len(boxes)):
            delta = boxes[i].delivery_date - boxes[i - 1].delivery_date
            assert delta == timedelta(weeks=1)
