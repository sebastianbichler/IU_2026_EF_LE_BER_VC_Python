### Use Case Diagram: Elephant Memory Cloud

```mermaid
graph LR
    %% Actors
    Ella((Ella Elephant<br/>User))
    Admin((System Admin<br/>Developer))

    %% System Boundary
    subgraph Memory_Cloud [Memory Cloud System]
        direction TB
        UC1([Index Events])
        UC2([Visualize Family Tree])
        UC3([Receive Anniversary Reminder])
        UC4([Perform Memory Audit])
        UC5([Trigger GC Manually])
    end

    %% Relationships
    Ella --- UC1
    Ella --- UC2
    UC3 -.-> Ella
    
    Admin --- UC4
    Admin --- UC5

    %% Dependency Link
    UC2 -.->|Creates circular<br/>references| UC4

    %% Styling
    style Memory_Cloud fill:#ffffff,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style Ella fill:#e1f5fe,stroke:#01579b
    style Admin fill:#fff3e0,stroke:#e65100
    style UC2 fill:#f9f9f9,stroke:#d32f2f,stroke-width:2px
```

<u>**Primary Actors:**</u>
* **Ella Elephant** (End User): focuses on functional interaction with the savanna data
* **System Admin** (Developer/Analyst): focuses on technical stability and memory efficiency

<u>**Key Use Cases & Interactions:**</u>
* **Data Management:** Ella indexes events (water sources, herd migrations) to build the "Memory Cloud"
* **Family Tree Visualization:**
  * **Functional Goal:** querying kinships and ancestry
  * **Technical Impact:** process generates complex object graphs with circular references (Parent $\leftrightarrow$ Child)
* **Automated Reminders:** system pushes notifications to Ella for significant anniversaries
* **Memory Audit & GC Control:**
  * admin monitors system health under heavy data loads
  * manual Garbage Collection (GC) triggers allow for testing how the system handles the cleanup of unreachable cycles

<u>**System Logic:**</u>
* **The Dependency:**
  * direct link between "Visualize Family Tree" and "Memory Audit"
  * the deeper the ancestry data, the higher the risk of memory leaks, necessitating robust automated management