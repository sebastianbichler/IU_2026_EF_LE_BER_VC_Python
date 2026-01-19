import json
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ValidationInfo

# --- CONFIG LOADING ---
# Lädt externe Konfigurationen, um Hardcoding zu vermeiden.
# Teil der Architektur-Anforderung für sauberen Code.
CONFIG_PATH = Path("data/config.json")

DEFAULT_CONFIG = {
    "min_booking_days": 7,
    "max_steps_for_discount": 500,
    "discount_high_threshold": 100,
    "wake_up_delay_hours": 3,
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
    print("WARNING: Config file corrupted. Using defaults.")
    CONFIG = DEFAULT_CONFIG


# --- DATA MODELS ---


class HammockBooking(BaseModel):
    """
    Manages booking logic for hammocks.

    Addressed Requirements:
    - REQ-FUN-001: Minimum Duration Check (Booking must be >= 7 days).
    - REQ-NFR-005: Object Oriented Design using Pydantic Models.
    """

    guest_name: str
    nights: int

    @field_validator("nights")
    @classmethod
    def validate_duration(cls, v: int, info: ValidationInfo) -> int:
        """
        Validates that the booking duration meets the 'Laziness Standards'.
        Implementation of REQ-FUN-001.
        """
        # Load rule from config
        min_days = CONFIG.get("min_booking_days", 7)

        if v < min_days:
            # Rejection logic for REQ-FUN-001
            raise ValueError(
                f"Too stressful! Min {min_days} nights required. (REQ-FUN-001)"
            )
        return v


class MovementTracker(BaseModel):
    """
    Calculates discounts based on inactivity.

    Addressed Requirements:
    - REQ-FUN-003: Step Input (validated >= 0).
    - REQ-FUN-004: Inverse Discount Logic (less steps = more discount).
    """

    # REQ-FUN-003: Input validation ensuring non-negative steps
    steps_today: int = Field(ge=0, description="Steps taken by the guest")

    def calculate_discount(self) -> float:
        """
        Determines the discount percentage.
        Implementation of REQ-FUN-004 (Inverse Logic).
        """
        threshold_high = CONFIG.get("discount_high_threshold", 100)
        threshold_limit = CONFIG.get("max_steps_for_discount", 500)

        # REQ-FUN-004: Logic Branching
        if self.steps_today <= threshold_high:
            return 0.50  # 50% Discount (Gold Tier Laziness)
        elif self.steps_today <= threshold_limit:
            return 0.20  # 20% Discount (Silver Tier)
        else:
            return 0.00  # 0% Discount (Too active)
