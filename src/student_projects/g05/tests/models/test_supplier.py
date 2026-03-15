import unittest
from unittest.mock import patch

from src.student_projects.g05.src.models.supplier import Supplier
from src.student_projects.g05.src.models.fish import Fish


class TestSupplier(unittest.TestCase):

    def setUp(self):

        self.supplier = Supplier(
            name="Ocean Supplier",
            fish_price_list={
                "Lachs": 10.0,
                "Hering": 5.0
            },
            price_volatility=1.0,
            reliability=0.8,
            average_delay_days=2,
            quality_factor=1.0
        )

        self.salmon = Fish("Lachs", 8.5, 0.15)

    # --------------------------------------------------
    # get_price
    # --------------------------------------------------

    @patch("random.gauss")
    def test_get_price(self, mock_gauss):

        mock_gauss.return_value = 11.0

        price = self.supplier.get_price(self.salmon)

        self.assertEqual(price, 11.0)

    def test_get_price_unknown_fish(self):

        tuna = Fish("Tuna", 9.0, 0.2)

        with self.assertRaises(ValueError):
            self.supplier.get_price(tuna)

    @patch("random.gauss")
    def test_get_price_not_negative(self, mock_gauss):

        mock_gauss.return_value = -5.0

        price = self.supplier.get_price(self.salmon)

        self.assertEqual(price, 0.0)

    # --------------------------------------------------
    # delivery_successful
    # --------------------------------------------------

    @patch("random.random")
    def test_delivery_success(self, mock_random):

        mock_random.return_value = 0.2

        result = self.supplier.delivery_successful()

        self.assertTrue(result)

    @patch("random.random")
    def test_delivery_failure(self, mock_random):

        mock_random.return_value = 0.9

        result = self.supplier.delivery_successful()

        self.assertFalse(result)

    # --------------------------------------------------
    # delivery_delay
    # --------------------------------------------------

    @patch("random.gauss")
    def test_delivery_delay(self, mock_gauss):

        mock_gauss.return_value = 3

        delay = self.supplier.delivery_delay()

        self.assertEqual(delay, 3)

    @patch("random.gauss")
    def test_delivery_delay_not_negative(self, mock_gauss):

        mock_gauss.return_value = -2

        delay = self.supplier.delivery_delay()

        self.assertEqual(delay, 0)


if __name__ == "__main__":
    unittest.main()
