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
        """Move logic for the current state."""
        pass


class RestingState(SlothState):
    """
    Represents the default resting state of a slotted guest.
    From here, the guest can transition to eating or sleeping.
    """

    name = "Resting"

    def eat(self) -> str:
        """Transitions the guest to the Eating state."""
        return "Slowly munching on a leaf... Delicious."

    def sleep(self) -> str:
        """Transitions the guest to the Sleeping state."""
        return "Eyes closing... transitioning to sleep."

    def move(self) -> str:
        """Allows the guest to move slowly to the hammock."""
        return "Moving very slowly to the hammock."


class SleepingState(SlothState):
    """
    Represents the sleeping state of a slotted guest.
    In this state, eating is strictly prohibited.
    """

    name = "Sleeping"

    def eat(self) -> str:
        """Blocks eating and returns an error message."""
        return "Cannot eat while sleeping! Wake up first."

    def sleep(self) -> str:
        """Remains in the sleeping state."""
        return "Already asleep... Zzzzz..."

    def move(self) -> str:
        """Blocks physical movement while sleeping."""
        return "Dreaming of moving... but staying put."


class EatingState(SlothState):
    """
    Represents the eating state of a slotted guest.
    In this state, sleeping and moving are restricted.
    """

    name = "Eating"

    def eat(self) -> str:
        """Remains in the eating state."""
        return "Already eating. Don't rush me."

    def sleep(self) -> str:
        """Blocks sleeping until the guest finishes eating."""
        return "Too full to sleep yet."

    def move(self) -> str:
        """Blocks physical movement while chewing."""
        return "Cannot move while chewing. Safety first."
