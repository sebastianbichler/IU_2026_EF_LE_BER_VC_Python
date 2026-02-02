import json
import logging
from typing import Any
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ValidationInfo

logger = logging.getLogger(__name__)

# --- CONFIG LOADING ---
# Lädt externe Konfigurationen, um Hardcoding zu vermeiden.
# Teil der Architektur-Anforderung für sauberen Code.
CONFIG_PATH = Path("data/config.json")

DEFAULT_CONFIG = {
    "min_booking_days": 7,
    "max_steps_for_discount": 500,
    "discount_high_threshold": 100,
    "wake_up_delay_hours": 3,
    "min_food_maturity_days": 14,
}

try:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            file_content = f.read().strip()
            if not file_content:
                CONFIG = DEFAULT_CONFIG
            else:
                f.seek(0)
                CONFIG = json.load(f)
    else:
        CONFIG = DEFAULT_CONFIG
except json.JSONDecodeError:
    logger.warning("Config file corrupted. Using defaults.")
    CONFIG = DEFAULT_CONFIG


# --- DATA MODELS ---


class HammockBooking(BaseModel):
    """
    Manages booking logic for hammocks.

    Addressed Requirements:
    - REQ-FR-01 - M - Min Duration: Booking must be >= 7 days.
    - REQ-NFR-05 - M - Architecture: Object Oriented Design using Pydantic Models.
    """

    guest_name: str
    nights: int

    @field_validator("nights")
    @classmethod
    def validate_duration(cls, v: int, info: ValidationInfo) -> int:
        """
        Validates that the booking duration meets the 'Laziness Standards'.
        Implementation of REQ-FR-01.
        """
        # Load rule from config
        min_days = CONFIG.get("min_booking_days", 7)

        if v < min_days:
            # Rejection logic for REQ-FR-01
            raise ValueError(
                f"Too stressful! Min {min_days} nights required. (REQ-FR-01)"
            )
        return v


# --- DUCK TYPING (UNIVERSAL GUEST) ---


class Sloth:
    """
    Represents the ultimate slow guest: a Sloth.
    Expected to have the highest slowness factor for maximum discount.
    """

    def get_slowness_factor(self) -> float:
        """
        Returns the slowness factor for a Sloth.

        Returns:
            float: The slowness factor (1.0).
        """
        return 1.0  # The gold standard


class Turtle:
    """
    Represents a slow, shell-carrying guest: a Turtle.
    Has a slightly lower slowness factor than a Sloth.
    """

    def get_slowness_factor(self) -> float:
        """
        Returns the slowness factor for a Turtle.

        Returns:
            float: The slowness factor (0.8).
        """
        return 0.8  # Pretty slow, but has a shell to carry


class Panda:
    """
    Represents a meditating, moderately slow guest: a Panda.
    """

    def get_slowness_factor(self) -> float:
        """
        Returns the slowness factor for a meditating Panda.

        Returns:
            float: The slowness factor (0.6).
        """
        return 0.6  # Meditating takes time


class IUDozent:
    """
    Represents an overworked and tired IU lecturer.
    Very slow due to exhaustion.
    """

    def get_slowness_factor(self) -> float:
        """
        Returns the slowness factor for an IU Dozent.

        Returns:
            float: The slowness factor (0.9).
        """
        return 0.9  # Overworked and very tired


class MovementTracker(BaseModel):
    """
    Calculates discounts based on inactivity.

    Addressed Requirements:
    - REQ-FR-03 - M - Step Input: Step Input (validated >= 0).
    - REQ-FR-04 - M - Inverse Discount: Inverse Discount Logic (less steps = more discount).
    """

    # REQ-FR-03: Input validation ensuring non-negative steps
    steps_today: int = Field(ge=0, description="Steps taken by the guest")
    guest: Any = Field(
        default=Sloth(), description="The guest object associated with the tracking"
    )

    def calculate_discount(self) -> float:
        """
        Determines the discount percentage.
        Implementation of REQ-FR-04 (Inverse Logic) and Duck Typing.
        """
        threshold_high = CONFIG.get("discount_high_threshold", 100)
        threshold_limit = CONFIG.get("max_steps_for_discount", 500)

        # Base Logic Branching (REQ-FR-04)
        if self.steps_today <= threshold_high:
            base_discount = 0.50  # 50% Discount (Gold Tier Laziness)
        elif self.steps_today <= threshold_limit:
            base_discount = 0.20  # 20% Discount (Silver Tier)
        else:
            base_discount = 0.00  # 0% Discount (Too active)

        # Duck Typing Integration: EAFP (Easier to ask for forgiveness than permission)
        # We don't check isinstance or use abstract base classes. We just try the method.
        try:
            factor = self.guest.get_slowness_factor()
            return base_discount * factor
        except AttributeError:
            # If the guest has no slowness factor (or no guest provided), apply standard discount
            return base_discount


class MaturityCalculator(BaseModel):
    """
    Simulates the maturity calculation for food.

    Addressed Requirements:
    - REQ-FR-05 - M - Maturity Calc: Algorithmus zur Berechnung der Blattreife. Nahrungsmittel dürfen erst nach Erreichen des optimalen Reifegrads ausgegeben werden.
    """

    item_name: str
    days_on_branch: int = Field(ge=0, description="Days the food has been ripening")
    optimal_maturity_days: int = Field(
        default_factory=lambda: CONFIG.get("min_food_maturity_days", 14),
        description="Days required for optimal maturity",
    )

    def is_ripe(self) -> bool:
        """
        Calculates if the food is ready to be eaten.
        Implementation of REQ-FR-05.
        """
        return self.days_on_branch >= self.optimal_maturity_days


def check_in_guest(guest: Any) -> str:
    """
    Demonstrates Python's Duck Typing.
    Sid doesn't care what class the guest is. He only cares if the guest
    can respond to `get_slowness_factor()`.

    Args:
        guest (Any): The guest object to be checked in.

    Returns:
        str: A welcome message if the guest is slow enough, or a rejection
             message if the guest is too fast or doesn't implement the method.
    """
    try:
        factor = guest.get_slowness_factor()
        if factor > 0.5:
            return f"Welcome! Your slowness factor is {factor}. Here is your hammock."
        else:
            return "You are too fast for this hotel!"
    except AttributeError:
        return "Security! This entity doesn't know how to be slow!"
