### Object Diagram

```mermaid
graph LR
    %% Scopes
    subgraph Stack [&nbsp&nbspProgram Stack/ Scope&nbsp&nbsp]
        direction TB
        DeletedVar["<s>ella_ref</s>"]
    end

    %% Heap Memory
    subgraph Heap [Heap Memory: 'The Dead Island']
        direction LR
        E1["<b>ella : Elephant</b><br/>reference count: 1"]
        E2["<b>baby_kai : Elephant</b><br/>reference count: 1"]
        
        %% Circular References mit mehr Abstand durch längere Pfeile
        E1 ===>|".children (strong)"| E2
        E2 ===>|".parent (strong)"| E1
    end

    %% Connection from Stack to Heap
    DeletedVar -. "reference removed" .-> E1

    %% Styling
    style DeletedVar fill: #fdd, stroke: #f00, color: #f00
    style Heap fill: #fffcf5, stroke: #e65100, stroke-width: 2px, stroke-dasharray: 5 5
    style E1 fill: #fff, stroke: #333
    style E2 fill: #fff, stroke: #333
    
    %% Coloring the cycle links specifically
    linkStyle 1 stroke: #e65100, stroke-width: 2px
    linkStyle 2 stroke: #e65100, stroke-width: 2px
```

<u>**Memory Segmentation:**</u>
* **Program Stack:**
  * contains the local variable ella_ref
  * red styling indicates that the variable has been deleted (del ella_ref), meaning the application can no longer access this memory address
* **Heap Memory:**
  * contains the actual Elephant instances
  * orange dashed border represents the "Dead Island" — a group of objects that are isolated from the main program but still occupy memory

<u>**The Circular Reference Problem:**</u>
* even though the external reference is gone, ella and baby_kai maintain strong references to each other (.children and .parent)
* because each object still has an internal reference count of 1, Python's standard memory manager assumes they are still "in use" and refuses to delete them
* this state represents a memory leak (objects are unreachable from the code but stay alive in the heap)
* only the Cyclic Garbage Collector can detect this isolated island, recognize that it has no connection to the stack, and force-clear the cycle to free up memory