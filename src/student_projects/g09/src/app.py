import streamlit as st
import time
from typing import Any
from datetime import datetime, timedelta
from models import HammockBooking, MovementTracker, CONFIG
from states import RestingState, SleepingState, EatingState

# --- Setup & Session State ---
st.set_page_config(page_title="Sloth Resort", page_icon="Sloth")

if "sloth_state" not in st.session_state:
    st.session_state["sloth_state"] = RestingState()


def set_state(new_state: Any) -> None:
    """
    Helper function to change the active State of the guest
    and trigger a UI rerun for Streamlit.
    """
    st.session_state["sloth_state"] = new_state
    st.success(f"State changed to: {new_state.name}")
    time.sleep(0.5)
    st.rerun()


# --- GUI Header ---
st.title("Sloth's Slow-Motion Hotel")
st.markdown("*Where laziness is a virtue.*")

# --- Sidebar: Navigation ---
menu = st.sidebar.radio(
    "Menu",
    ["Dashboard & State", "Hammock Booking", "Movement Tracker", "Wake-Up Service"],
)

# --- PAGE 1: STATE PATTERN DEMO ---
if menu == "Dashboard & State":
    st.header("Guest Status Monitor")

    current_state = st.session_state["sloth_state"]
    st.info(f"Current Status: **{current_state.name}**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Attempt to Eat"):
            result = current_state.eat()
            if "Cannot" in result:
                st.error(result)
            else:
                st.success(result)
                if isinstance(current_state, RestingState):
                    set_state(EatingState())

    with col2:
        if st.button("Attempt to Sleep"):
            result = current_state.sleep()
            if "Too" in result:
                st.error(result)
            else:
                st.success(result)
                if not isinstance(current_state, SleepingState):
                    set_state(SleepingState())

    with col3:
        if st.button("Wake Up / Relax"):
            set_state(RestingState())

# --- PAGE 2: BOOKING ---
elif menu == "Hammock Booking":
    st.header("Book a Hammock")
    st.caption(f"Config: Minimum stay is {CONFIG['min_booking_days']} nights.")

    with st.form("booking_form"):
        name = st.text_input("Guest Name")
        nights = st.number_input("Number of Nights", min_value=1, value=7)
        submitted = st.form_submit_button("Book Now")

        if submitted:
            try:
                booking = HammockBooking(guest_name=name, nights=nights)
                st.balloons()
                st.snow()

            except ValueError as e:
                st.error(
                    str(e).split("Value error, ")[1]
                    if "Value error" in str(e)
                    else str(e)
                )

# --- PAGE 3: MOVEMENT TRACKER ---
elif menu == "Movement Tracker":
    st.header("Discount Calculator")

    steps = st.slider("Steps walked today", 0, 1000, 50)

    tracker = MovementTracker(steps_today=steps)
    discount = tracker.calculate_discount()

    st.metric(label="Discount Percentage", value=f"{discount * 100}%", delta=None)

    if discount >= 0.5:
        st.success("Excellent! You barely moved!")
    elif discount == 0:
        st.warning("Too active! No discount for you.")

# --- PAGE 4: WAKE UP ---
elif menu == "Wake-Up Service":
    st.header("Gentle Wake-Up")

    if "wake_up_time" not in st.session_state:
        st.session_state["wake_up_time"] = datetime.now().time()

    wanted_time = st.time_input("I want to wake up at:", key="wake_up_time")

    if st.button("Set Alarm"):
        delay = CONFIG.get("wake_up_delay_hours", 3)

        now = datetime.now()
        target_date = datetime.combine(now.date(), wanted_time)

        if target_date < now:
            target_date += timedelta(days=1)
            day_label = "Tomorrow"
        else:
            day_label = "Today"

        real_wake_up_dt = target_date + timedelta(hours=delay)

        st.write(
            f"Request received for: {wanted_time.strftime('%H:%M')} ({day_label})."
        )

        with st.spinner("Calculating sloth physics..."):
            time.sleep(1.5)

        st.success("Alarm set!")
        st.info(
            f"**Requested Time:** {wanted_time.strftime('%H:%M')}\n"
            f"**+ Sloth Delay:** {delay} hours\n"
            f"**ACTUAL Alarm:** {real_wake_up_dt.strftime('%H:%M')} ({real_wake_up_dt.strftime('%A')})"
        )
