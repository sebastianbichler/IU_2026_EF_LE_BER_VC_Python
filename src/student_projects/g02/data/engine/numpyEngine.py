import numpy as np
from engine.mathKernel import MathKernel

class NumpyVectorizedEngine(MathKernel):

    def find_stolen_nuts(self, data):
        expected = data["expected_amount"]
        actual = data["amount"]

        return np.sum(actual < expected)
