import unittest

from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.recipe import Recipe
from src.student_projects.g05.src.models.menu_item import MenuItem
from src.student_projects.g05.src.models.order_item import OrderItem
from src.student_projects.g05.src.models.order import Order
from src.student_projects.g05.src.models.bill import Bill


class TestOrder(unittest.TestCase):

    def setUp(self):
        fish = Fish("Lachs", 8.5, 0.15)
        recipe = Recipe("Lachs Gericht", fish, 0.3)
        menu_item = MenuItem("Lachs Teller", recipe, 18.0)

        order_item = OrderItem(menu_item, 2)
        bill = Bill([order_item])

        self.order = Order("Pinguin", [order_item], bill)

    def test_total_items(self):
        self.assertEqual(self.order.total_items(), 2)

    def test_total_amount(self):
        self.assertGreater(self.order.total_amount(), 0)
        