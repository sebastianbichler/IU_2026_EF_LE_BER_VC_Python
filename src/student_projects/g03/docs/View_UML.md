```mermaid
classDiagram
    direction TB
    %% Layer 1: View
    RabbitFarmView : -controller
    RabbitFarmView : +render_menu()
    RabbitFarmView : +get_user_input()
    
    %% Layer 2: Controller  
    RabbitFarmController : -model
    RabbitFarmController : -view
    RabbitFarmController : +handle_action()
    
    %% Layer 3: Model
    RabbitFarmModel : -inventory
    RabbitFarmModel : +add_vegetable()
    RabbitFarmModel : +run_benchmark()
    
    %% Domain
    Vegetable : +name
    Vegetable : +isfresh()
    Inventory : +items
    Bed : +id
    
    %% DTOs
    UserInput : +action
    BenchmarkResult : +eager_time
    
    %% Service
    SensorService : +benchmark()
    
    %% === SAUBERE HIERARCHIE ===
    RabbitFarmView ..> RabbitFarmController : ruft auf
    RabbitFarmController *-- RabbitFarmModel : verwendet
    
    RabbitFarmView --> UserInput : erstellt
    RabbitFarmController --> UserInput : empfängt  
    
    RabbitFarmModel --> SensorService : delegiert an
    SensorService --> BenchmarkResult : liefert zurück
    RabbitFarmModel --> BenchmarkResult : liefert zurück
    RabbitFarmController --> BenchmarkResult : weitergeleitet
    RabbitFarmView --> BenchmarkResult : zeigt an
    
    RabbitFarmModel o-- Inventory : enthält
    Inventory o-- Vegetable : enthält
    Vegetable --> Bed : gehört zu