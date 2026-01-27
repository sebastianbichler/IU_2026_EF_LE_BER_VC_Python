# MVP Definition: Elephant Memory Cloud

The Minimum Viable Product (MVP) defines the mandatory core features required to validate our hypotheses regarding Python's Memory Management.

## 1. Core Functional Scope (Biological Layer)
* **Entity Modeling:** implementation of `Elephant`, `Herd`, and `WaterSource` classes
* **Relationship Engine:** logic to link elephants (Parent/Child) and assign them to herds
* **History Index:** basic registry to store and search events by year and location
* **Basic UI:** Streamlit interface to trigger actions and view results

## 2. Scientific & Technical Scope (Memory Layer)
* **Cycle Injection:** explicit logic to create bidirectional strong references (The "Dead Island" scenario)
* **Telemetry:** real-time tracking of `_instance_count` and total RAM usage (via `tracemalloc`)
* **Comparison Suite:** toggle to run cleanup scenarios with `gc.collect()` vs. `weakref` implementations
* **Visual Proof:** generation of an object graph to confirm the existence / deletion of cycles

## 3. Out of Scope for MVP
* advanced AI / vector database integration
* persistent database storage (all data remains in-memory)
* complex geographic map rendering