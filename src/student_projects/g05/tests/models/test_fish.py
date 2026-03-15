import sys
import os
import unittest

# Add project root to path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../..")
    )
)

from src.student_projects.g05.src.models.fish import Fish


class TestFish(unittest.TestCase):

    def test_valid_fish_creation(self):
        fish = Fish("Lachs", 8.5, 0.15)

        self.assertEqual(fish.name, "Lachs")
        self.assertEqual(fish.base_cost_per_kg, 8.5)
        self.assertEqual(fish.supplier_price_variance, 0.15)

    def test_negative_base_cost(self):
        with self.assertRaises(ValueError):
            Fish("Lachs", -5, 0.1)

    def test_zero_base_cost(self):
        with self.assertRaises(ValueError):
            Fish("Lachs", 0, 0.1)

    def test_negative_variance(self):
        with self.assertRaises(ValueError):
            Fish("Lachs", 8, -0.2)


if __name__ == "__main__":
    unittest.main()
