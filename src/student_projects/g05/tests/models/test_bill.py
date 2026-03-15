import unittest

from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.recipe import Recipe
from src.student_projects.g05.src.models.menu_item import MenuItem
from src.student_projects.g05.src.models.order_item import OrderItem
from src.student_projects.g05.src.models.bill import Bill


class TestBill(unittest.TestCase):

    def setUp(self):

        fish = Fish("Lachs", 8.5, 0.15)

        recipe = Recipe(
            "Lachs Gericht",
            fish,
            0.3
        )

        menu_item = MenuItem(
            "Lachs Teller",
            recipe,
            18.0
        )

        order_item = OrderItem(
            menu_item,
            2
        )

        self.bill = Bill([order_item])

    def test_total_with_tax_returns_float(self):

        total = self.bill.total_with_tax()

        self.assertIsInstance(total, float)

    def test_total_with_tax_value(self):

        total = self.bill.total_with_tax()

        # Expected:
        # 2 * 18 = 36
        # 36 * 1.07 = 38.52
        self.assertAlmostEqual(total, 38.52, places=2)

    def test_empty_bill(self):

        bill = Bill([])

        total = bill.total_with_tax()

        self.assertEqual(total, 0)

    def test_custom_tax_rate(self):
        fish = Fish("Lachs", 8.5, 0.15)
        recipe = Recipe("Lachs Gericht", fish, 0.3)
        menu_item = MenuItem("Lachs Teller", recipe, 10)

        order_item = OrderItem(menu_item, 1)

        bill = Bill([order_item], tax_rate=0.20)

        self.assertAlmostEqual(bill.total_with_tax(), 12.0)
