from pydantic import ValidationError
from models import HammockBooking, MovementTracker


def run_app():
    print("--- Sloth's Slow-Motion Hotel System (MVP) ---")
    print("Loading Modules... Done.\n")

    # --- Feature 1: Movement Tracker Test ---
    print(">>> Testing Requirement: Movement Tracker (Discount)")
    # Test Case A: Very lazy sloth
    tracker_lazy = MovementTracker(steps_today=50)
    print(f"Guest 'Sid' walked {tracker_lazy.steps_today} steps.")
    print(f"Discount granted: {tracker_lazy.calculate_discount() * 100}%\n")

    # Test Case B: Active sloth (Error case)
    tracker_active = MovementTracker(steps_today=600)
    print(f"Guest 'Flash' walked {tracker_active.steps_today} steps.")
    print(f"Discount granted: {tracker_active.calculate_discount() * 100}%\n")

    # --- Feature 2: Hammock Booking Test ---
    print(">>> Testing Requirement: Hammock Booking (Min 7 Days)")

    # Test Case C: Valid Booking
    try:
        booking = HammockBooking(guest_name="Sid", nights=10)
        print(
            f"SUCCESS: Booking for {booking.guest_name} confirmed for {booking.nights} nights."
        )
    except ValidationError as e:
        print(f"ERROR: {e}")

    # Test Case D: Invalid Booking (Too short)
    try:
        print("Attempting to book for 3 nights...")
        booking_short = HammockBooking(guest_name="Flash", nights=3)
        print("SUCCESS: Booking confirmed.")
    except ValidationError as e:
        # We expect this error!
        print("BLOCKED: System correctly rejected the booking.")
        # Pydantic returns a detailed error list, we grab the message
        print(f"Reason: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    run_app()
