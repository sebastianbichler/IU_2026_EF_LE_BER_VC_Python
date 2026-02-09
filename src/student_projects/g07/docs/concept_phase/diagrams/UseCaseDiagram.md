# Use Case Diagram: Elephant Memory Cloud

This diagram illustrates the functional and scientific requirements of the system, distinguishing between standard user interactions and technical research activities.

```mermaid
graph LR
    %% Actors
    Ella((Ella Elephant<br/>End User))
    Admin((System Admin<br/>Researcher))

    %% System Boundary
    subgraph Memory_Cloud [Elephant Memory Cloud System]
        direction TB
        
        subgraph Functional_Layer [Functional Layer]
            UC1([F01/F02: index & search events])
            UC2([F04/F06: visualize family tree])
            UC3([F08: receive reminders])
        end
        
        subgraph Research_Layer [Scientific Layer]
            UC4([F05: create circular references])
            UC5([F09/F10: measure memory & GC comparison])
            UC6([validate hypotheses H1 & H2])
        end
    end

    %% Ella's Interactions
    Ella --- UC1
    Ella --- UC2
    UC3 -.-> Ella

    %% Admin Interactions
    Admin --- UC4
    Admin --- UC5
    Admin --- UC6

    %% Cross-Layer Dependencies
    UC2 -.->|triggers complex<br/>object graphs| UC4
    UC5 -.->|provides data for| UC6

    %% Styling
    style Memory_Cloud fill:#ffffff,stroke:#333,stroke-dasharray: 5 5
    style Ella fill:#e1f5fe,stroke:#01579b
    style Admin fill:#fff3e0,stroke:#e65100
    style UC2 fill:#f9f9f9,stroke:#d32f2f
```

### Primary Actors

* **Ella Elephant (End User):**
  * interacts with the savanna data model
  * main goal: manage historical events and understand her ancestry
* **System Admin (Researcher/Analyst):**
  * uses the system as a laboratory
  * focus is on technical stability, performance monitoring, and memory auditing

### Key Use Cases

* **Event Management (F01, F02):** storing and retrieving historical data based on year and location
* **Family Tree Visualization (F04, F06):** mapping kinship relations, primary driver for creating deep object graphs
* **Memory Research (F05, F09, F10):**
  * **Cycle Injection:** purposefully creating circular references (e.g., Parent ↔ Child) to test memory limits
  * **GC Comparison:** running identical scenarios with and without Python's cyclic Garbage Collector
* **Hypothesis Validation:** testing H1 (leaking behavior without GC) and H2 (cycle resolution with GC) based on quantitative metrics

### Technical Logic & Dependencies

* **The Bridge:**
  * there is a direct link between the functional "Family Tree" and the scientific "Memory Audit"
  * complexity of biological ancestry data is used as a real-world proxy for the technical problem of circular references
* **Memory Profiling:** system provides specialized tools to observe unreachable objects in real-time