class SlothAntiPattern:
    """
    Anti-Pattern for Guest States.
    This class uses a single state variable and multiple if/else branches to manage state transitions.
    This represents the typical "spaghetti code" approach before applying the State Pattern.
    """

    def __init__(self) -> None:
        """Initializes the object with the default Resting state (0)."""
        # 0 = Resting, 1 = Sleeping, 2 = Eating
        self.state: int = 0

    def get_state_name(self) -> str:
        """Returns the string representation of the current numerical state."""
        if self.state == 0:
            return "Resting"
        elif self.state == 1:
            return "Sleeping"
        elif self.state == 2:
            return "Eating"
        else:
            return "Unknown"

    def eat(self) -> str:
        """
        Attempts to transition to the Eating state.
        Demonstrates complex if/elif branching (Anti-Pattern).
        """
        if self.state == 0:
            # Can eat when resting
            self.state = 2
            return "Slowly munching on a leaf... Delicious."
        elif self.state == 1:
            # Cannot eat when sleeping
            return "ERROR: Cannot eat while sleeping! Wake up first."
        elif self.state == 2:
            # Already eating
            return "Already eating. Don't rush me."
        else:
            return "ERROR: Invalid state"

    def sleep(self) -> str:
        """
        Attempts to transition to the Sleeping state.
        Demonstrates complex if/elif branching (Anti-Pattern).
        """
        if self.state == 0:
            # Can sleep when resting
            self.state = 1
            return "Eyes closing... transitioning to sleep."
        elif self.state == 1:
            # Already sleeping
            return "Already asleep... Zzzzz..."
        elif self.state == 2:
            # Cannot sleep when full/eating
            return "Too full to sleep yet."
        else:
            return "ERROR: Invalid state"

    def move(self) -> str:
        """
        Executes move logic depending on the current active state.
        Demonstrates complex if/elif branching (Anti-Pattern).
        """
        if self.state == 0:
            return "Moving very slowly to the hammock."
        elif self.state == 1:
            return "Dreaming of moving... but staying put."
        elif self.state == 2:
            return "Cannot move while chewing. Safety first."
        else:
            return "ERROR: Invalid state"

    def wake_up(self) -> str:
        """Forces the state back to Resting (0)."""
        # Always return to resting on wake up/relax
        self.state = 0
        return "Ah, awake and resting."
