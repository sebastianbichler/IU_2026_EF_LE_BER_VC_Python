from abc import ABC, abstractmethod

class SlothState(ABC):
    """
    Abstract Base Class for the State Pattern.
    Defines the interface for all sloth states.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def eat(self) -> str:
        pass

    @abstractmethod
    def sleep(self) -> str:
        pass

    @abstractmethod
    def move(self) -> str:
        pass

class RestingState(SlothState):
    name = "Resting 🛋️"

    def eat(self) -> str:
        return "Slowly munching on a leaf... Delicious."

    def sleep(self) -> str:
        return "Eyes closing... transitioning to sleep."

    def move(self) -> str:
        return "Moving very slowly to the hammock."

class SleepingState(SlothState):
    name = "Sleeping 💤"

    def eat(self) -> str:
        # LOGIK: Wer schläft, kann nicht essen!
        return "ERROR: Cannot eat while sleeping! Wake up first."

    def sleep(self) -> str:
        return "Already asleep... Zzzzz..."

    def move(self) -> str:
        return "Dreaming of moving... but staying put."

class EatingState(SlothState):
    name = "Eating 🍃"

    def eat(self) -> str:
        return "Already eating. Don't rush me."

    def sleep(self) -> str:
        return "Too full to sleep yet."

    def move(self) -> str:
        return "Cannot move while chewing. Safety first."