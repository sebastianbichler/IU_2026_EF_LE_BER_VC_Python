# Project Storybook

This Storybook tracks our development journey, organized into thematic Epics and technical Milestones.

### Epic 1: The Biological Blueprint
**Focus:** class structure and basic simulation logic
* [ ] **Task:** implement `Elephant` base class with tracking decorators
* [ ] **Task:** create `Herd` management logic (matriarch selection, membership)
* [ ] **Task:** build `Event` indexing for historical water source data

### Epic 2: The Memory Trap
**Focus:** intentional creation of memory leaks through cycles
* [ ] **Task:** implement bidirectional Parent-Child references
* [ ] **Task:** document the failure of standard `del` operations in cyclic graphs
* [ ] **Task:** integrate `objgraph` or manual tracking to visualize "unreachable" objects

### Epic 3: Scientific Analysis
**Focus:** testing Hypotheses H1 and H2
* [ ] **Task:** create "Stress Test" scripts to generate 10,000+ cyclic objects
* [ ] **Task:** implement the Garbage Collection toggle (enable / disable / manual trigger)
* [ ] **Task:** data collection: export memory consumption curves to Matplotlib

### Epic 4: Optimization & Refactoring
**Focus:** implementing the `weakref` solution
* [ ] **Task:** refactor Parent-references to use `weakref.ref`
* [ ] **Task:** compare performance and determinism between GC-cleanup and Weakref-cleanup
* [ ] **Task:** finalize Streamlit dashboard for the presentation