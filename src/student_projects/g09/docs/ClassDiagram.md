```mermaid
classDiagram
    direction TB

    %% --- 1. LOGIC SERVICES (Module) ---
    class BookingSystem {
        +validate_duration(nights) bool
    }

    class MovementTracker {
        +calculate_discount(steps) float
    }

    class WakeUpService {
        +calculate_real_alarm(target_time) time
    }

    %% --- 2. CONTEXT (Der Gast) ---
    class SlothGuest {
        +String name
        -GuestState _state
        +set_state(GuestState)
        +request_booking(nights)
        +input_steps(steps)
        +set_alarm(time)
        +eat(food_item)
    }

    %% --- 3. STATE PATTERN (Verhalten) ---
    class GuestState {
        <<Interface>>
        +handle_activity(guest)
    }

    class SleepingState {
        +handle_activity()
    }

    class RestingState {
        +handle_activity()
    }

    class EatingState {
        +handle_activity()
    }

    %% --- 4. DUCK TYPING OBJECTS ---
    class Eucalyptus {
        +int maturity_days
        +check_maturity() bool
    }

    class PalmLeaf {
        +int maturity_days
        +check_maturity() bool
    }

    %% --- BEZIEHUNGEN ---
    
    %% Guest nutzt Services (Dependency)
    SlothGuest ..> BookingSystem
    SlothGuest ..> MovementTracker
    SlothGuest ..> WakeUpService

    %% Guest hat einen State (Association/Aggregation)
    SlothGuest o-- GuestState

    %% State Implementierung (Inheritance)
    GuestState <|.. SleepingState
    GuestState <|.. RestingState
    GuestState <|.. EatingState

    %% Duck Typing: Guest nutzt diese Objekte dynamisch
    SlothGuest ..> Eucalyptus
    SlothGuest ..> PalmLeaf
