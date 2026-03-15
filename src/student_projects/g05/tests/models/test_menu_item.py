import unittest

from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.recipe import Recipe
from src.student_projects.g05.src.models.menu_item import MenuItem


class TestMenuItem(unittest.TestCase):

    def setUp(self):
        fish = Fish("Lachs", 8.5, 0.15)

        self.recipe = Recipe(
            "Lachs Gericht",
            fish,
            0.3
        )

    def test_menu_item_creation(self):

        item = MenuItem(
            name="Lachs Teller",
            recipe=self.recipe,
            price=18.0
        )

        self.assertEqual(item.name, "Lachs Teller")
        self.assertEqual(item.recipe.name, "Lachs Gericht")
        self.assertEqual(item.price, 18.0)

    def test_price_type(self):

        item = MenuItem(
            name="Test",
            recipe=self.recipe,
            price=10.5
        )

        self.assertIsInstance(item.price, float)
        