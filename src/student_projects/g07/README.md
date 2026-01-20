# 🐘 Elephant Memory Cloud

A comprehensive archive management system demonstrating Python's cyclic garbage collection at scale. Since elephants never forget, they use Python to manage the massive archive of the African savannah.

## 🎯 Project Goals

1. **Large-Scale Data Management**: Index events, family trees (who's related to whom?), and historical water source data
2. **Efficient Search**: "Where's the nearest water source?" based on historical drought data
3. **Memory Management**: Demonstrate Python's cyclic garbage collection handling thousands of circular references
4. **Reminder Bot**: Notify animals of important anniversaries or migration starts

## 🚀 Features

### 📊 Dashboard
- **Real-time Memory Monitoring**: Live statistics showing memory usage, object counts, and GC metrics
- **Circular Reference Tracking**: Monitor thousands of parent-child relationships in memory
- **Performance Metrics**: Memory per elephant, GC efficiency, and more

### 🗄️ Large-Scale Data Generation
- **Configurable Family Trees**: Generate 5-20 families with 2-10 generations each
- **Multiple Herds**: Create 5-50 herds with automatic elephant assignment
- **Historical Events**: Generate up to 10,000 events (migrations, births, droughts)
- **Water Source Database**: 10 water sources with 25+ years of availability data
- **Progress Tracking**: Real-time progress bars during generation

### 🔍 Efficient Search Engine
- **In-Memory Indexes**: O(1) lookup using dictionary-based indexes
- **Nearest Water Source**: Find closest water by coordinates with availability check
- **Drought History**: Search drought years across all water sources
- **Event Timeline**: Search events by year, location, type, or elephant
- **Migration Alerts**: Anniversary notifications for historical migrations
- **Search Statistics**: Monitor index performance and coverage

### 📈 Analytics
- **Memory Impact Analysis**: See memory usage per elephant and per circular reference
- **GC Statistics**: Monitor all 3 generations of Python's garbage collector
- **Dataset Visualization**: Interactive charts showing data distribution
- **Export Capability**: Save current dataset to JSON

## 🏃 Quick Start

### Installation

```bash
# Clone or navigate to the project directory
cd src/student_projects/g07

# Create virtual environment
python -m venv venv
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
2. **Configure parameters** (start with 5 families, 5 generations, 1000 events)
3. **Click "Generate Large Dataset"** and watch the progress
4. **Explore Search tab** to query the data
5. **Check Analytics tab** to see memory impact

## 🏗️ Architecture

### In-Memory Storage
All data lives in Python memory with **circular references intact**:
- Elephants ↔ Parents/Children (circular parent-child relationships)
- Elephants ↔ Herds (bidirectional membership)
- Events → Elephants (historical references)

This architecture is **perfect for demonstrating Python's cyclic GC** because:
- Traditional reference counting would leak memory
- Python's mark-and-sweep collector handles cycles efficiently
- We can monitor GC performance at scale

### Search Performance
- **Dictionary-based indexes** for O(1) lookups
- Year index: `{2020: [event1, event2, ...]}`
- Elephant index: `{"Ella": [event1, event2, ...]}`
- Location index: Grid-based spatial indexing

## 📁 Project Structure

```
elephant_memory_cloud/
├── streamlit_app.py           # Main Streamlit dashboard (4 tabs)
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
│   ├── gc_analyzer.py        # Circular reference detection
│   └── store.py              # In-memory object store
│
├── data/                      # Data generation
│   ├── __init__.py
│   ├── generator.py          # Large-scale data generation
│   └── default_data.json     # Seed data
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

