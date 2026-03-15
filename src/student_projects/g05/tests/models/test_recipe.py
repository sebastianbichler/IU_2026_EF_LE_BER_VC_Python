import unittest

from src.student_projects.g05.src.models.fish import Fish
from src.student_projects.g05.src.models.recipe import Recipe


class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.fish = Fish("Lachs", 8.5, 0.15)

    def test_recipe_creation(self):
        recipe = Recipe("Lachs Gericht", self.fish, 0.3)

        self.assertEqual(recipe.name, "Lachs Gericht")
        self.assertEqual(recipe.fish.name, "Lachs")
        self.assertEqual(recipe.fish_required_kg, 0.3)
