import unittest
from datetime import date, timedelta

from src.student_projects.g05.src.core.pengueats import PenguEats
from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.recipe import Recipe
from src.student_projects.g05.src.models.menu_item import MenuItem
from src.student_projects.g05.src.models.inventory_item import InventoryItem
from src.student_projects.g05.src.models.order_item import OrderItem
from src.student_projects.g05.src.models.order import Order
from src.student_projects.g05.src.models.bill import Bill


class TestPenguEats(unittest.TestCase):

    def setUp(self):

        self.restaurant = PenguEats()

        fish = Fish("Lachs", 8.5, 0.15)
        recipe = Recipe("Lachs Gericht", fish, 0.3)

        self.menu_item = MenuItem("Lachs Teller", recipe, 18.0)

        self.restaurant.add_menu_item(self.menu_item)

        expiry = date.today() + timedelta(days=5)

        self.restaurant.inventory.append(
            InventoryItem(fish, 10, expiry)
        )

    def test_add_menu_item(self):
        self.assertEqual(len(self.restaurant.menu), 1)

    def test_place_order(self):

        order_item = OrderItem(self.menu_item, 1)
        bill = Bill([order_item])

        order = Order("Pinguin", [order_item], bill)

        self.restaurant.place_order(order)

        self.assertEqual(len(self.restaurant.orders), 1)

    def test_revenue(self):

        order_item = OrderItem(self.menu_item, 1)
        bill = Bill([order_item])
        order = Order("Pinguin", [order_item], bill)

        self.restaurant.place_order(order)

        revenue = self.restaurant.get_total_revenue()

        self.assertGreater(revenue, 0)
