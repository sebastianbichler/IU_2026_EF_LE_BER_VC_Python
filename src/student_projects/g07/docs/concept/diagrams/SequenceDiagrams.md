### Sequence Diagram: Simple Reference Counting
```mermaid
%% simple reference counting
sequenceDiagram
    participant P as Program Scope
    participant E as Elephant Instance
    participant CL as Elephant Class (Static)
    
    Note over P, E: single reference (no cycle)
    
    P ->> P: del elephant_ref
    
    Note right of P: reference count hits 0
    
    rect rgb(220, 255, 220)
        Note over E: immediate destruction
        
        E ->>+   CL : _instances.discard(id(self))
        CL -->>- E  : updated set
        E -->>   P  : memory freed
    end
    
    Note over CL: Elephant.get_instance_count() returns 0
```

* **Mechanism:**
  * standard Python behavior where an object is destroyed as soon as its reference count drops to zero
* **Key Takeaway:**
  * destruction is deterministic and immediate
  * \_\_del__ method is called the moment del is executed, promptly updating the class instance tracker


### Sequence Diagram: Reference Counting
```mermaid
sequenceDiagram
    participant P as Program Scope
    participant E as Elephant Instance
    participant C as Child (Elephant)
    participant CL as Elephant Class (Static)

    Note over E, C: strong bidirectional reference
    Note right of E: reference count: 2 (scope + child)
    Note right of C: reference count: 1 (parent)

    rect rgb(255, 230, 230)
        P ->> P: del elephant_ref
        Note right of P: scope reference removed
    end

    Note over E: reference count: 1 (still held by child)
    Note right of E: Status: UNREACHABLE but ALIVE
    Note over E, CL: __del__() is NOT called yet!
    Note over CL: Elephant.get_instance_count() still returns 2
    Note over P: program continues...
```

* **Mechanism:**
  * bidirectional strong reference creates a cycle
* **Problem:**
  * deleting the scope variable only reduces the count from 2 to 1
  * since count is not 0, the object remains "alive" in memory
* **Key Takeaway:**
  * object becomes unreachable from the program code but is not destroyed
  * demonstrates why reference counting alone cannot handle circular dependencies

### Sequence Diagram: Garbage Collector
```mermaid
%% garbage collector
sequenceDiagram
    participant P as Program Scope
    participant GC as Python Garbage Collector
    participant E as Elephant Instance
    participant C as Child (Elephant)
    participant CL as Elephant Class (Static)
    
    Note over E, C: strong bidirectional Cycle
    
    P ->> P: del elephant_ref
    
    Note right of P: reference count > 0 due to cycle,<br/>but unreachable from code.

    rect rgb(240, 240, 240)
        Note over GC: GC trigger (threshold reached)
        
        GC ->> GC: identify_unreachable_cycles()
        
        Note over GC, C: GC breaks cycle and starts cleanup
        
        par
            GC ->>+  E  : call __del__()
            E  ->>+  CL : _instances.discard(id(self))
            CL -->>- E  : updated set
            E  -->>- GC : object destroyed
        and
            GC ->>+  C  : call __del__()
            C  ->>+  CL : _instances.discard(id(self))
            CL -->>- C  : updated set
            C  -->>- GC : object destroyed
        end
        
        Note over GC, CL: Note: order of __del__ calls is non-deterministic in cycles
    end

    Note over CL: Elephant.get_instance_count() returns 0
```

* **Mechanism:**
  * Python’s Cyclic Garbage Collector (GC) scans for "islands" of unreachable objects
* **Cleanup:**
  * GC force-breaks the cycle
  * because objects are part of a cycle, the order in which \_\_del__ is called on Parent vs. Child is non-deterministic (unpredictable)
* **Key Takeaway:**
  * GC acts as a backup to prevent permanent memory leaks, but it operates asynchronously (not immediately)

### Sequence Diagram: Garbage Collector with Weakref
```mermaid
sequenceDiagram
    participant P as Program Scope
    participant E as Elephant Instance
    participant C as Child (Elephant)
    participant CL as Elephant Class (Static)
    
    Note over E, C: child uses weakref(parent)
    
    P ->> P: del elephant_ref
    
    Note right of P: reference count<br>hits 0 immediately

    rect rgb(220, 255, 220)
        Note over E: Finalization
        
        E ->>+  CL : _instances.discard(id(self))
        CL -->>- E : updated set
        E -->> P   : Object destroyed
    end

    Note right of C: child._parent() now returns None
    Note over CL: Elephant.get_instance_count() now returns 1 (only child)
```

* **Mechanism:**
  * by using weakref, the child holds a reference to the parent that does not increase the reference count
* **Benefit:**
  * cycle is broken by design
  * when program scope deletes its reference, the parent's count hits 0 immediately
* **Key Takeaway:**
  * combines the best of both worlds: immediate, deterministic memory cleanup without needing to wait for the Garbage Collector