import logging
from pydantic import ValidationError
from models import HammockBooking, MovementTracker

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def run_app() -> None:
    """
    Main entry point for the CLI test environment.
    Runs a series of checks against Movement Tracker and Hammock Booking rules.
    """
    logger.info("--- Sloth's Slow-Motion Hotel System (MVP) ---")
    logger.info("Loading Modules... Done.\n")

    # --- Feature 1: Movement Tracker Test ---
    logger.info(">>> Testing Requirement: Movement Tracker (Discount)")
    # Test Case A: Very lazy sloth
    tracker_lazy = MovementTracker(steps_today=50)
    logger.info(f"Guest 'Sid' walked {tracker_lazy.steps_today} steps.")
    logger.info(f"Discount granted: {tracker_lazy.calculate_discount() * 100}%\n")

    # Test Case B: Active sloth (Error case)
    tracker_active = MovementTracker(steps_today=600)
    logger.info(f"Guest 'Flash' walked {tracker_active.steps_today} steps.")
    logger.info(f"Discount granted: {tracker_active.calculate_discount() * 100}%\n")

    # --- Feature 2: Hammock Booking Test ---
    logger.info(">>> Testing Requirement: Hammock Booking (Min 7 Days)")

    # Test Case C: Valid Booking
    try:
        booking = HammockBooking(guest_name="Sid", nights=10)
        logger.info(
            f"SUCCESS: Booking for {booking.guest_name} confirmed for {booking.nights} nights."
        )
    except ValidationError as e:
        logger.error(f"ERROR: {e}")

    # Test Case D: Invalid Booking (Too short)
    try:
        logger.info("Attempting to book for 3 nights...")
        HammockBooking(guest_name="Flash", nights=3)
        logger.info("SUCCESS: Booking confirmed.")
    except ValidationError as e:
        # We expect this error!
        logger.warning("BLOCKED: System correctly rejected the booking.")
        # Pydantic returns a detailed error list, we grab the message
        logger.warning(f"Reason: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    run_app()
