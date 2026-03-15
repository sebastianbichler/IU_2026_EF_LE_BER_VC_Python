import unittest
from datetime import date, timedelta

from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.inventory_item import InventoryItem


class TestInventoryItem(unittest.TestCase):

    def setUp(self):
        fish = Fish("Lachs", 8.5, 0.15)
        expiry = date.today() + timedelta(days=5)
        self.item = InventoryItem(fish, 10, expiry)

    def test_inventory_creation(self):
        self.assertEqual(self.item.amount_kg, 10)
        self.assertEqual(self.item.fish.name, "Lachs")
