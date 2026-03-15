import unittest
from datetime import date
from unittest.mock import MagicMock

from src.student_projects.g05.src.models.delivery import Delivery
from src.student_projects.g05.src.models.inventory_item import InventoryItem
from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.supplier import Supplier


class TestDelivery(unittest.TestCase):

    def setUp(self):

        self.supplier = Supplier("Test Supplier")

        fish = Fish("Lachs", 8.5, 0.15)

        self.inventory_item = InventoryItem(
            fish,
            5,
            date.today()
        )

        self.delivery = Delivery(
            supplier=self.supplier,
            delivery_date=date.today()
        )

    def test_add_item(self):

        self.delivery.add_item(self.inventory_item)

        self.assertEqual(len(self.delivery.items), 1)

    def test_successful_delivery(self):

        # mock supplier success
        self.supplier.delivery_successful = MagicMock(return_value=True)

        try:
            self.delivery.execute_delivery()
        except Exception:
            self.fail("execute_delivery() raised Exception unexpectedly")

    def test_failed_delivery(self):

        # mock supplier failure
        self.supplier.delivery_successful = MagicMock(return_value=False)

        with self.assertRaises(Exception):
            self.delivery.execute_delivery()
