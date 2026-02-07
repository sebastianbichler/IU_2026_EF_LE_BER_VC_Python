# 1. Sequence Diagram: Simple Reference Counting

This scenario demonstrates the ideal, deterministic cleanup of a single object.

```mermaid
sequenceDiagram
    participant P as Program Scope
    participant E as Ella : Elephant
    participant CL as Elephant Class (Static)
    
    Note over E: single reference (no cycle)
    
    P ->> P: del ella_ref
    
    Note right of P: ref count hits 0
    
    rect rgb(220, 255, 220)
        Note over E: trigger __del__()
        
        E ->>+   CL : _instances.discard(id(self))
        CL -->>- E  : updated set
        E -->>   P  : memory freed
    end
    
    Note over CL: Elephant.get_instance_count() returns 0
```

### Mechanism:

* standard Python behavior where an object is destroyed as soon as its ref count drops to zero

### Key Takeaway:

* destruction is deterministic and immediate
* \_\_del__() is called the moment del is executed, promptly updating the class instance tracker



# 2. Sequence Diagram: Reference Counting (The Leak)

Visualization of hypothesis H1: Why circular references prevent memory reclamation.

```mermaid
sequenceDiagram
    participant P as Program Scope
    participant E as Ella : Elephant
    participant K as Kibo : Elephant (Child)
    participant CL as Elephant Class (Static)

    Note over E, K: strong bidirectional reference
    Note right of E: ref count: 2 (scope + Kibo)
    Note right of K: ref count: 1 (Ella)

    rect rgb(255, 230, 230)
        P ->> P: del ella_ref
        Note right of P: scope reference removed
    end

    Note over E: ref count: 1 (still held by Kibo)
    Note right of E: Status: UNREACHABLE but ALIVE
    Note over E, CL: __del__() is NOT called yet!
    Note over CL: Elephant.get_instance_count() still returns 2
    Note over P: program continues despite memory leak...
```

### Mechanism:

* bidirectional strong reference creates a cycle

### Problem:

* deleting the scope variable only reduces the count from 2 to 1
* since count is not 0, the object remains "alive" in memory

### Key Takeaway:

* object becomes unreachable from the program code but is not destroyed
* demonstrates why reference counting alone cannot handle circular dependencies



# 3. Sequence Diagram: Garbage Collector Intervention

Visualization of hypothesis H2: The cyclic GC as a safety net.

```mermaid
sequenceDiagram
    participant P as Program Scope
    participant GC as Python GC
    participant E as Ella : Elephant
    participant K as Kibo : Elephant (Child)
    participant CL as Elephant Class (Static)
    
    Note over E, K: strong bidirectional cycle
    
    P ->> P: del ella_ref
    
    Note right of P: ref count > 0 due to cycle,<br/>but unreachable from code
    
    Note over GC: GC trigger (threshold or manual)
    
    GC ->> GC: identify_unreachable_cycles()
    
    rect rgb(240, 240, 240)
        Note over GC, K: GC breaks cycle and starts cleanup
        
        par Ella Destruction
            GC ->>+  E  : call __del__()
            E  ->>+  CL : _instances.discard(id(self))
            CL -->>- E  : updated set
            E  -->>- GC : Ella destroyed
        and Kibo Destruction
            GC ->>+  K  : call __del__()
            K  ->>+  CL : _instances.discard(id(self))
            CL -->>- K  : updated set
            K  -->>- GC : Kibo destroyed
        end
        
        Note over GC, CL: Note: order of __del__() calls is non-deterministic in cycles
    end

    Note over CL: Elephant.get_instance_count() returns 0
```

### Mechanism:

* Python’s cyclic GC scans for "islands" of unreachable objects

### Cleanup:

* GC force-breaks the cycle
* because objects are part of a cycle, the order in which \_\_del__() is called on parent vs. child is non-deterministic (unpredictable)

### Key Takeaway:

* GC acts as a backup to prevent permanent memory leaks, but it operates asynchronously (not immediately)



# 4. Sequence Diagram: Resolution with Weakref

The proactive solution using `weakref` for deterministic cleanup.

```mermaid
sequenceDiagram
    participant P as Program Scope
    participant E as Ella : Elephant
    participant K as Kibo : Elephant (Child)
    participant CL as Elephant Class (Static)
    
    Note over E, K: Kibo uses weakref(parent)
    Note over E, K: use_weak_refs = True
    
    P ->> P: del ella_ref
    
    Note right of P: Ella's ref count hits 0
    
    rect rgb(220, 255, 220)
        Note over E: immediate finalization
        
        E ->>+  CL : _instances.discard(id(self))
        CL -->>- E : updated set
        E -->> K   : Ella destroyed
    end

    Note right of K: Kibo._parent() now returns None
    Note over CL: Elephant.get_instance_count() returns 1 (only Kibo)
```

### Mechanism:

* by using weakref, the child holds a reference to the parent that does not increase the ref count

### Benefit:

* cycle is broken by design
* when program scope deletes its reference, the parent's count hits 0 immediately

### Key Takeaway:

* combines the best of both worlds: immediate, deterministic memory cleanup without needing to wait for the GC