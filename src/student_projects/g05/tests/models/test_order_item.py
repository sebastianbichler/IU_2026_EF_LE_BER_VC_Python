import unittest

from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.recipe import Recipe
from src.student_projects.g05.src.models.menu_item import MenuItem
from src.student_projects.g05.src.models.order_item import OrderItem


class TestOrderItem(unittest.TestCase):

    def setUp(self):
        fish = Fish("Lachs", 8.5, 0.15)
        recipe = Recipe("Lachs Gericht", fish, 0.3)
        menu_item = MenuItem("Lachs Teller", recipe, 18.0)

        self.order_item = OrderItem(menu_item, 2)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.menu_item.name, "Lachs Teller")
        