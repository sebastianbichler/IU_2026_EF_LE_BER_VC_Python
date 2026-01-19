import streamlit as st
import time
from datetime import datetime, timedelta
from models import HammockBooking, MovementTracker, CONFIG
from states import RestingState, SleepingState, EatingState

# --- Setup & Session State ---
st.set_page_config(page_title="Sloth Resort", page_icon="🦥")

# Initialisiere den State des Gastes in der Session (Speicher)
if "sloth_state" not in st.session_state:
    st.session_state["sloth_state"] = RestingState()


# Hilfsfunktion für State-Wechsel
def set_state(new_state):
    st.session_state["sloth_state"] = new_state
    st.success(f"State changed to: {new_state.name}")
    # Kurzer Rerun, um GUI zu aktualisieren
    time.sleep(0.5)
    st.rerun()


# --- GUI Header ---
st.title("🦥 Sloth's Slow-Motion Hotel")
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
        if st.button("Attempt to Eat 🍃"):
            result = current_state.eat()
            if "ERROR" in result:
                st.error(result)
            else:
                st.success(result)
                # Logik: Wenn wir essen, wechseln wir in EatingState
                if isinstance(current_state, RestingState):
                    set_state(EatingState())

    with col2:
        if st.button("Attempt to Sleep 💤"):
            result = current_state.sleep()
            if "ERROR" in result:
                st.error(result)
            else:
                st.success(result)
                if not isinstance(current_state, SleepingState):
                    set_state(SleepingState())

    with col3:
        if st.button("Wake Up / Relax 🛋️"):
            # Man kann immer relaxen/aufwachen
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
                # Pydantic Validierung feuert hier
                booking = HammockBooking(guest_name=name, nights=nights)
                st.balloons()
                st.success(f"Booking confirmed for {booking.guest_name}!")
            except ValueError as e:
                # Pydantic Fehlermeldung anzeigen (ohne Traceback)
                # Wir holen uns den sauberen Text aus dem Fehler
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

    st.metric(label="Discount Percentage", value=f"{discount*100}%", delta=None)

    if discount >= 0.5:
        st.success("Excellent! You barely moved!")
    elif discount == 0:
        st.warning("Too active! No discount for you.")

# --- PAGE 4: WAKE UP ---
elif menu == "Wake-Up Service":
    st.header("Gentle Wake-Up ⏰")

    # 1. State Management: Initialisiere Standard-Zeit nur EINMAL
    if "wake_up_time" not in st.session_state:
        # Standardmäßig auf 08:00 setzen oder aktuelle Zeit
        st.session_state["wake_up_time"] = datetime.now().time()

    # 2. Input Widget: Liest und schreibt direkt in den Session State
    # Der key='wake_up_time' verbindet das Widget automatisch mit dem Session State
    wanted_time = st.time_input("I want to wake up at:", key="wake_up_time")

    if st.button("Set Alarm"):
        # Logik: Konfiguration laden
        delay = CONFIG.get("wake_up_delay_hours", 3)

        # 3. Logik-Härtung: Datum berechnen (Heute oder Morgen?)
        now = datetime.now()
        target_date = datetime.combine(now.date(), wanted_time)

        # Fallback: Wenn die gewählte Zeit heute schon vorbei ist, nimm an, es ist morgen gemeint.
        # (z.B. Es ist 14:00 Uhr, User wählt 08:00 Uhr -> Morgen 08:00 Uhr)
        if target_date < now:
            target_date += timedelta(days=1)
            day_label = "Tomorrow"
        else:
            day_label = "Today"

        # 4. Die "Sloth-Tax" (Verzögerung) draufrechnen
        real_wake_up_dt = target_date + timedelta(hours=delay)

        # Feedback UI
        st.write(
            f"Request received for: {wanted_time.strftime('%H:%M')} ({day_label})."
        )

        with st.spinner("Calculating sloth physics..."):
            time.sleep(1.5)  # Kurzes Feedback-Delay

        # Ergebnis-Box
        st.success(f"✅ Alarm set!")
        st.info(f"""
            **Requested Time:** {wanted_time.strftime('%H:%M')}\n
            **+ Sloth Delay:** {delay} hours\n
            **ACTUAL Alarm:** {real_wake_up_dt.strftime('%H:%M')} ({real_wake_up_dt.strftime('%A')})
            """)
