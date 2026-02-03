import numpy as np


class DataGenerator:
    @staticmethod
    def generate_dataset(size: int) -> dict:
        rng = np.random.default_rng(42)

        return {
            "id": np.arange(size),
            "coords_x": rng.random(size) * 100,
            "coords_y": rng.random(size) * 100,
            "nut_type": rng.integers(0, 5, size),
            "depth_cm": rng.random(size) * 50,
            "amount": rng.integers(1, 100, size),
            "expected_amount": rng.integers(50, 120, size),
        }
