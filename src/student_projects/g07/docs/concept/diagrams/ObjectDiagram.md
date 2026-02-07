# Object Diagram: Hypothesis H1 - The Circular Reference Leak

This diagram visualizes the system state after a local reference is deleted, demonstrating why standard reference counting fails in cyclic structures.

```mermaid
graph LR
    %% Scopes
    subgraph Stack [Variable Scope / Stack]
        direction TB
        DeletedVar["<s>ella_ref</s>"]
        Note1["[del ella_ref executed]"]
    end

    %% Heap Memory
    subgraph Heap [Heap Memory: 'The Dead Island']
        direction LR
        E1["<b>E1 : Elephant (Ella)</b><br/>Status: UNREACHABLE<br/>Ref-Count: 1"]
        E2["<b>E2 : Elephant (child Kibo)</b><br/>Status: UNREACHABLE<br/>Ref-Count: 1"]
        
        %% Circular References
        E1 ===>|".children (strong ref)"| E2
        E2 ===>|".parent (strong ref)"| E1
    end

    %% The broken connection
    DeletedVar -. "external link removed" .-> E1

    %% Scientific Annotation
    H1_Note{{<b>Hypothesis H1:</b><br/>Without Cyclic GC, these<br/>objects stay in RAM forever.}}

    %% Styling
    style DeletedVar fill:#fdd,stroke:#f00,color:#f00
    style Heap fill:#fffcf5,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5
    style E1 fill:#fff,stroke:#333
    style E2 fill:#fff,stroke:#333
    style H1_Note fill:#e1f5fe,stroke:#01579b
    
    linkStyle 1 stroke:#e65100,stroke-width:2px
    linkStyle 2 stroke:#e65100,stroke-width:2px
```

### Memory Segmentation:

* **Stack:** variable `ella_ref` has been removed from the scope and the application can no longer access the objects
* **Heap:** instances `E1` and `E2` still occupy memory and form a "Dead Island"

### The Failure of Reference Counting:

* internal reference count is 1 for both objects because they point to each other via `.children` and `.parent` although no external variable points to the island
* Python's simple reference counter refuses to delete them, leading to a Memory Leak

### Scientific Context:

* state confirms Hypothesis H1 memory consumption increases with the size of the unreachable graph if the cyclic GC is inactive



# Object Diagram: Hypothesis H2 - Cycle Resolution

This diagram visualizes the state after the cyclic GC or a `weakref` implementation has successfully cleared the "Dead Island".

```mermaid
graph LR
    %% Scopes
    subgraph Stack [Variable Scope / Stack]
        direction TB
        DeletedVar["<s>ella_ref</s>"]
    end

    %% Heap Memory
    subgraph Heap_Clean [Heap Memory: Reclaimed]
        direction LR
        Empty["[ memory cleared ]"]
    end

    %% The Action
    GC((Python GC /<br/>Weakref)) -- "1. identifies cycle<br/>2. breaks link<br/>3. reclaims memory" --> Heap_Clean

    %% Scientific Annotation
    H2_Note{{<b>Hypothesis H2:</b><br/>Active GC or Weakrefs<br/>successfully resolve<br/>circular dependencies.}}

    %% Styling
    style DeletedVar fill:#fdd,stroke:#f00,color:#f00
    style Heap_Clean fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style GC fill:#e1f5fe,stroke:#01579b
    style H2_Note fill:#e8f5e9,stroke:#2e7d32
```

### The Resolution Process:

* **Cyclic GC:** GC identifies that the objects are only referencing each other and are unreachable from the stack $\rightarrow$ GC force-calls `__del__` and clears the heap
* **Weakref Alternative:** if `weakref` was used for the `.parent` attribute, the reference count of `E1` would have hit 0 immediately upon deleting `ella_ref`, triggering a deterministic cleanup without GC intervention

### Scientific Context:

* state confirms Hypothesis H2 circular references are successfully resolved once the external reference is removed and the GC is active

### Verification:

* `Elephant.get_instance_count()` now returns `0`, proving a clean memory state