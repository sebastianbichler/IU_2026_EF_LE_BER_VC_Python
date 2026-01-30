from abc import ABC, abstractmethod


class MathKernel(ABC):
    @abstractmethod
    def find_stolen_nuts(self, expected, actual):
        pass
