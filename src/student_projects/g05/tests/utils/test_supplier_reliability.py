import unittest

from src.student_projects.g05.src.utils.supplier_reliability import SupplierReliabilityModel


class TestSupplierReliabilityModel(unittest.TestCase):

    def setUp(self):
        self.model = SupplierReliabilityModel(
            successes=8,
            total=10
        )

    def test_model_build(self):

        self.model.build_model()

        self.assertIsNotNone(self.model.model)

    def test_run_mcmc(self):

        self.model.build_model()

        # small sample size for fast test
        self.model.run_mcmc(
            draws=50,
            tune=50,
            chains=1
        )

        self.assertIsNotNone(self.model.trace)

    def test_get_reliability(self):

        self.model.build_model()

        self.model.run_mcmc(
            draws=50,
            tune=50,
            chains=1
        )

        mean, hdi = self.model.get_reliability()

        self.assertIsInstance(mean, float)
        self.assertTrue(0 <= mean <= 1)

        self.assertEqual(len(hdi), 2)
