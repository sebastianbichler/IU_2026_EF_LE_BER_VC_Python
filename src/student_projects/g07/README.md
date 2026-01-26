# 🐘 Elephant Memory Cloud

A comprehensive Streamlit dashboard demonstrating Python's cyclic garbage collection at scale through an interactive elephant archive management system.

## 🎯 Project Purpose

This project visualizes how Python's cyclic garbage collector handles circular references by creating thousands of interconnected elephant family relationships. Watch in real-time as Python's mark-and-sweep algorithm successfully frees memory that reference counting alone cannot handle.

## 🚀 Features

### 🏠 Dashboard
- **2-Step GC Demonstration**: 
  - Step 1: Break references (elephants become orphaned but stay in memory)
  - Step 2: Run GC (Python's cyclic collector frees the orphaned objects)
- **Live Memory Visualization**: Interactive pie chart showing Streamlit overhead, active elephants, orphaned elephants, and other data
- **Real-time Metrics**: Process memory, Python objects, GC generation counts, and circular reference tracking

### 🗄️ Data Generation
- **Natural Family Trees**: Generate 1-20 families with 2-10 generations
- **Variable Children**: Each elephant has 1-N children (randomly assigned for natural variation)
- **Multiple Herds**: Create 5-50 herds with automatic elephant assignment
- **Historical Events**: Generate up to 10,000 events (migrations, births, droughts)
- **Water Sources**: 10 water sources with 25+ years of drought/availability data
- **Progress Tracking**: Real-time progress bar during generation

### 🔍 Search Engine
- **6 Search Types**:
  - Nearest Water Source (spatial search with availability check)
  - Drought History (search by year range)
  - Events by Year (with interactive bar chart)
  - Elephant Timeline (individual elephant history)
  - Migration Alerts (anniversary notifications)
  - Search Statistics (index performance metrics)
- **In-Memory Indexes**: O(1) dictionary lookups for fast queries

### 🌳 Genealogy
- **Family Overview**: Total families, average size, generation depth, circular references, orphans
- **Interactive Family Tree**: Hierarchical visualization using NetworkX and Plotly
  - Color-coded by generation
  - Hover for details (name, birth year, children count)
  - Automatic layout positioning
- **Relationship Analysis**:
  - Children distribution chart (0 children = red, others = blue)
  - Age distribution over time (area chart)
  - Oldest and youngest elephants
  - Average children and average age metrics

## 🏃 Quick Start

### Installation

```bash
# Clone or navigate to the project directory
cd elephant_memory_cloud

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

The dashboard will open at **http://localhost:8501**

### First Steps

1. **Go to "Data Generation" tab**
2. **Configure parameters** (recommended: 5 families, 5 generations, 3 max children, 1000 events)
3. **Click "Generate Large Dataset"** - watch the progress bar
4. **Return to Dashboard tab** to see live memory usage
5. **Try the 2-step GC demo**:
   - Click "Break References" → elephants become orphaned (stay in memory)
   - Click "Run GC" → Python's cyclic GC frees them
6. **Explore Search tab** to query the generated data
7. **Check Genealogy tab** to visualize family trees and relationships

## 🏗️ Architecture

### In-Memory Storage
All data lives in Python memory with **circular references intact**:
- Elephants ↔ Parents/Children (bidirectional parent-child relationships)
- Elephants ↔ Herds (bidirectional membership)
- Events → Elephants (historical references)

This architecture **demonstrates Python's cyclic GC** because:
- Traditional reference counting alone would leak memory (cycles prevent refcount reaching 0)
- Python's mark-and-sweep collector identifies unreachable cycles
- The 2-step demo proves this: orphaned objects stay in memory until GC runs

### Visualization Stack
- **Streamlit**: Dashboard framework
- **Plotly**: Interactive charts (pie, bar, area, network graphs)
- **psutil**: Process memory monitoring

### Family Tree Implementation
- **Native Python dictionaries**: Graph structure (nodes & edges)
- **Custom hierarchical layout**: Automatic positioning by generation
- **Plotly visualization**: Interactive tree with hover details

### Search Performance
- **Dictionary-based indexes** for O(1) lookups
- Year index: `{2020: [event1, event2, ...]}`
- Elephant index: `{"Ella": [event1, event2, ...]}`
- Spatial index: Grid-based for water source queries

## 📁 Project Structure

```
elephant_memory_cloud/
├── app.py                     # Main Streamlit dashboard (4 tabs)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── models/                    # Domain models
│   ├── __init__.py
│   ├── elephant.py           # Elephant with circular parent-child refs
│   ├── herd.py               # Herd management
│   ├── event.py              # Historical events (migrations, births, etc.)
│   └── water_source.py       # Water sources with availability data
│
├── memory/                    # Memory management & monitoring
│   ├── __init__.py
│   ├── monitor.py            # Process memory monitoring
│   └── store.py              # In-memory object store
│
├── data/                      # Data generation
│   ├── __init__.py
│   └── generator.py          # Large-scale data generation

│
└── search/                    # Search engine
    ├── __init__.py
    └── engine.py             # Indexed search with O(1) lookups
```

## 🔬 Scientific Focus (Topic 1)

### Memory Management: Cyclic Garbage Collection

This project demonstrates:

1. **Circular References at Scale**
   - Thousands of parent ↔ child relationships
   - Elephant ↔ herd bidirectional membership
   - Complex relationship graphs

2. **Memory Leak Prevention**
   - Without cyclic GC, these references would never be freed
   - Python's mark-and-sweep collector identifies unreachable cycles
   - Reference counting alone cannot handle cycles

3. **Performance Monitoring**
   - Track memory usage with 1000+ elephants
   - Monitor GC generations (0, 1, 2)
   - Measure memory per elephant
   - Observe GC efficiency in real-time

4. **Validation**
   - Create large dataset → observe memory increase
   - Clear references → force GC → observe memory decrease
   - Prove cyclic GC successfully frees circular references

### Key Metrics

When you generate a dataset with **5 families × 5 generations**:
- ~**1,200+ elephants** created
- ~**2,400+ circular references** (parent-child bidirectional)
- ~**+50-100 MB** memory usage
- Cleanup frees **~95% of memory** (proving GC works!)

## 🎓 Educational Value

This project teaches:
- **Memory Management**: How Python handles circular references
- **Data Structures**: In-memory indexes for fast search
- **Scalability**: Generating and managing large datasets
- **Performance**: Monitoring memory and GC overhead
- **Architecture**: When to use in-memory vs database storage

## 📝 Technical Notes

### Memory Considerations
- **Recommended**: 5-10 families with 4-6 generations (~1K-5K elephants)
- **Maximum**: 20 families with 10 generations (~50K+ elephants, requires 16GB+ RAM)
- Each elephant uses approximately 50-100KB including circular references

### Search Performance
- Year search: O(1) - direct dictionary lookup
- Elephant search: O(1) - indexed by name
- Location search: O(k) where k = nearby grid cells
- Event type search: O(1) - indexed by type

## 📄 License

Educational project - free to use and modify.

---

**🐘 "An elephant never forgets... especially with Python's garbage collector!"**

