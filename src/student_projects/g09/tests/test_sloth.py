import pytest
from pydantic import ValidationError
from models import HammockBooking, MovementTracker, MaturityCalculator, Sloth, Turtle
from states import RestingState, SleepingState, EatingState

# --- UNIT TESTS ---


def test_hammock_booking_valid():
    """REQ-FR-01: Booking >= 7 days should be accepted"""
    booking = HammockBooking(guest_name="Sid", nights=10)
    assert booking.guest_name == "Sid"
    assert booking.nights == 10


def test_hammock_booking_invalid():
    """REQ-FR-01: Booking < 7 days should raise ValidationError"""
    with pytest.raises(ValidationError) as exc_info:
        HammockBooking(guest_name="Flash", nights=3)

    # Verify the specific error message is present
    assert "Too stressful! Min 7 nights required." in str(exc_info.value)


def test_movement_tracker_gold_tier():
    """REQ-FR-04: Inverse Discount. <= 100 steps should give 50% discount"""
    tracker = MovementTracker(steps_today=50)
    assert tracker.calculate_discount() == 0.50


def test_movement_tracker_silver_tier():
    """REQ-FR-04: Inverse Discount. 101-500 steps should give 20% discount"""
    tracker = MovementTracker(steps_today=250)
    assert tracker.calculate_discount() == 0.20


def test_movement_tracker_no_discount():
    """REQ-FR-04: Inverse Discount. > 500 steps should give 0% discount"""
    tracker = MovementTracker(steps_today=600)
    assert tracker.calculate_discount() == 0.00


def test_movement_tracker_duck_typing_sloth():
    """Duck Typing: A sloth has a slowness factor of 1.0."""
    tracker = MovementTracker(steps_today=50, guest=Sloth())
    assert tracker.calculate_discount() == 0.50 * 1.0


def test_movement_tracker_duck_typing_turtle():
    """Duck Typing: A turtle has a slowness factor of 0.8."""
    tracker = MovementTracker(steps_today=50, guest=Turtle())
    # 0.50 base discount * 0.8 factor = 0.40
    assert tracker.calculate_discount() == 0.40


def test_resting_state_transitions():
    """State Pattern: Validating the RestingState actions"""
    state = RestingState()
    assert "Slowly munching" in state.eat()
    assert "Eyes closing" in state.sleep()
    assert "Moving very slowly" in state.move()


def test_maturity_calculator_ripe():
    """REQ-FR-05: Food is strictly ripe when days_on_branch >= optimal_maturity_days."""
    leaf = MaturityCalculator(
        item_name="Eucalyptus", days_on_branch=15, optimal_maturity_days=14
    )
    assert leaf.is_ripe() is True


def test_maturity_calculator_unripe():
    """REQ-FR-05: Food is unripe when days_on_branch < optimal_maturity_days."""
    leaf = MaturityCalculator(
        item_name="Eucalyptus", days_on_branch=10, optimal_maturity_days=14
    )
    assert leaf.is_ripe() is False


def test_sleeping_state_transitions():
    """REQ-FR-08: State Transition. Cannot eat while sleeping."""
    state = SleepingState()
    result = state.eat()
    assert "Cannot eat while sleeping" in result


# --- INTEGRATION TESTS ---


def test_integration_full_guest_lifecycle():
    """
    Integration Test 1: Simulates a full guest lifecycle.
    1. Guest books a hammock (REQ-FR-01)
    2. Guest records steps for the day (REQ-FR-03, REQ-FR-04)
    3. Guest goes to sleep (REQ-FR-07, REQ-FR-08)
    """
    # 1. Booking
    booking = HammockBooking(guest_name="Manny", nights=8)
    assert booking.nights >= 7

    # 2. Tracking Activity
    tracker = MovementTracker(steps_today=90)
    discount = tracker.calculate_discount()
    assert discount == 0.50  # Very lazy -> high discount

    # 3. State Management
    current_state = RestingState()
    assert isinstance(current_state, RestingState)

    # Manny goes to sleep
    current_state = SleepingState()
    # While sleeping, Manny tries to eat (should fail)
    response = current_state.eat()
    assert "Cannot eat" in response


def test_integration_active_guest_rejection():
    """
    Integration Test 2: Simulates a hyperactive guest failing the hotel's vibe check.
    1. Guest tries to book for a weekend (3 days) -> Fails
    2. Guest tries to get a discount after running 10,000 steps -> 0%
    """
    # 1. Booking fails
    with pytest.raises(ValidationError):
        HammockBooking(guest_name="Sonic", nights=3)

    # 2. No discount
    tracker = MovementTracker(steps_today=10000)
    assert tracker.calculate_discount() == 0.00


def test_integration_state_machine_flow():
    """
    Integration Test 3: Tests the proper flow of state changes.
    Resting -> Eating -> Sleeping -> Resting
    """
    state = RestingState()

    # Eat
    eat_result = state.eat()
    assert "Cannot eat" not in eat_result
    state = EatingState()

    # Sleep
    sleep_result = state.sleep()
    assert "Cannot sleep" not in sleep_result
    state = SleepingState()

    # Try Eating again (while sleeping)
    eat_result = state.eat()
    assert "Cannot eat" in eat_result
