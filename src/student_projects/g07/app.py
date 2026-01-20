#!/usr/bin/env python3
"""
Elephant Memory Cloud - Streamlit Dashboard
Real-time memory monitoring, large-scale data generation, and efficient search.
"""

import streamlit as st
import gc
from datetime import datetime
from collections import Counter
from models import Elephant, Herd, Event, WaterSource
from models.event import EventType
from memory import MemoryMonitor, GarbageCollectionAnalyzer
from memory.store import get_store
from data.generator import DataGenerator
from search.engine import ElephantSearchEngine

# Page config
st.set_page_config(
    page_title="🐘 Elephant Memory Cloud",
    page_icon="🐘",
    layout="wide"
)

# Initialize session state
if 'monitor' not in st.session_state:
    st.session_state.monitor = MemoryMonitor()
    st.session_state.analyzer = GarbageCollectionAnalyzer()
    st.session_state.store = get_store()
    st.session_state.search_engine = ElephantSearchEngine()
    st.session_state.large_dataset_generated = False

# Header
st.title("🐘 Elephant Memory Cloud")
st.markdown("**Archiv-Management mit Circular Reference Demonstration & Efficient Search**")
st.divider()

# Create tabs for different functionality
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Dashboard", 
    "🗄️ Data Generation", 
    "🔍 Search Engine",
    "📊 Analytics"
])

# ============================================================================
# TAB 1: Dashboard Overview
# ============================================================================
with tab1:
    st.header("🏠 Archive Overview")
    st.markdown("Real-time statistics of the Elephant Memory Cloud archive")
    
    # Main dashboard metrics
    col1, col2, col3, col4 = st.columns(4)

    # Get current stats
    gc.collect()
    gc_count = gc.get_count()
    memory_mb = st.session_state.monitor.get_process_memory_mb()
    store_stats = st.session_state.store.get_stats()
    
    with col1:
        st.metric("💾 Process Memory", f"{memory_mb:.2f} MB")
        st.metric("🐘 Total Elephants", f"{store_stats['total_elephants']:,}")

    with col2:
        st.metric("🔗 Python Objects", f"{len(gc.get_objects()):,}")
        st.metric("👥 Herds", store_stats['total_herds'])

    with col3:
        st.metric("🗑️ GC Gen 0", gc_count[0])
        st.metric("📅 Historical Events", f"{store_stats['total_events']:,}")
    
    with col4:
        st.metric("♻️ Circular Refs", f"{store_stats['circular_references']:,}")
        st.metric("💧 Water Sources", store_stats['total_water_sources'])

    st.divider()
    
    # Quick actions
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🗑️ Clear All Data & Run GC", 
                     disabled=not st.session_state.large_dataset_generated,
                     use_container_width=True,
                     type="primary"):
            snapshot_before = st.session_state.monitor.take_snapshot("Before cleanup")
            count_before = Elephant.get_instance_count()
            
            # Clear store
            st.session_state.store.clear()
            st.session_state.large_dataset_generated = False
            
            # Force GC
            collected = gc.collect()
            
            snapshot_after = st.session_state.monitor.take_snapshot("After cleanup")
            count_after = Elephant.get_instance_count()
            
            st.success("🧹 Cleanup complete!")
            st.info(f"📊 Elephants: {count_before:,} → {count_after:,}")
            st.info(f"🗑️ Objects collected: {collected:,}")
            st.info(f"💾 Memory freed: {snapshot_before['process_memory_mb'] - snapshot_after['process_memory_mb']:.2f} MB")
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Refresh Statistics", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Status and instructions
    if not st.session_state.large_dataset_generated:
        st.info("👉 **Get Started:** Go to the 'Data Generation' tab to create a large dataset with circular references")
    else:
        st.success(f"✅ **Archive Active:** {store_stats['total_elephants']:,} elephants with {store_stats['circular_references']:,} circular references in memory")
        
        # Show memory efficiency metrics
        if store_stats['total_elephants'] > 0:
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                memory_per_elephant = (memory_mb / store_stats['total_elephants']) * 1024  # KB
                st.metric("Memory per Elephant", f"{memory_per_elephant:.2f} KB")
            
            with col_b:
                st.metric("Avg Children per Elephant", f"{store_stats['avg_children']:.2f}")
            
            with col_c:
                refs_per_elephant = store_stats['circular_references'] / store_stats['total_elephants']
                st.metric("Circular Refs per Elephant", f"{refs_per_elephant:.2f}")
        
        # Quick stats overview
        with st.expander("📊 Detailed Memory Analysis"):
            st.markdown("### Garbage Collection Details")
            gc_stats = gc.get_stats()
            st.json({
                "GC Generation 0": gc_count[0],
                "GC Generation 1": gc_count[1],
                "GC Generation 2": gc_count[2],
                "Total Objects in Memory": len(gc.get_objects()),
                "Circular References": store_stats['circular_references']
            })
            
            st.markdown("### Archive Statistics")
            st.json({
                "Total Elephants": store_stats['total_elephants'],
                "Total Herds": store_stats['total_herds'],
                "Total Events": store_stats['total_events'],
                "Total Water Sources": store_stats['total_water_sources'],
                "Average Children": round(store_stats['avg_children'], 2)
            })

# ============================================================================
# TAB 2: Data Generation
# ============================================================================
with tab2:
    st.header("🗄️ Large-Scale Data Generation")
    st.markdown("Generate large datasets to demonstrate memory management at scale")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generation Parameters")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            num_families = st.number_input("Number of Families", min_value=1, max_value=20, value=5)
            generations = st.number_input("Generations per Family", min_value=2, max_value=10, value=5)
        
        with col_b:
            children_per_elephant = st.number_input("Children per Elephant", min_value=2, max_value=5, value=3)
            num_herds = st.number_input("Number of Herds", min_value=5, max_value=50, value=10)
        
        with col_c:
            num_events = st.number_input("Number of Events", min_value=100, max_value=10000, value=1000, step=100)
        
        # Estimate stats
        estimated_elephants = num_families * (children_per_elephant ** generations)
        st.info(f"📊 Estimated: ~{estimated_elephants:,} elephants, {num_events:,} events, {num_herds} herds")
        
        if st.button("🚀 Generate Large Dataset", type="primary", use_container_width=True):
            # Clear existing data
            st.session_state.store.clear()
            
            with st.spinner("Generating large dataset..."):
                snapshot_before = st.session_state.monitor.take_snapshot("Before generation")
                
                # Generate data
                progress_bar = st.progress(0)
                
                # Generate families (50% of progress)
                elephants = DataGenerator.generate_multiple_families(
                    num_families=num_families,
                    generations=generations,
                    children_per_elephant=children_per_elephant
                )
                progress_bar.progress(50)
                
                # Generate herds (70%)
                herds = DataGenerator.generate_herds(num_herds)
                progress_bar.progress(70)
                
                # Assign elephants to herds (80%)
                DataGenerator.assign_elephants_to_herds(elephants, herds)
                progress_bar.progress(80)
                
                # Generate water sources (85%)
                water_sources = DataGenerator.generate_water_sources()
                progress_bar.progress(85)
                
                # Generate events (95%)
                events = DataGenerator.generate_events(elephants, herds, num_events)
                progress_bar.progress(95)
                
                # Add to store
                st.session_state.store.add_elephants(elephants)
                st.session_state.store.add_herds(herds)
                st.session_state.store.add_events(events)
                st.session_state.store.add_water_sources(water_sources)
                
                # Build search indexes
                st.session_state.search_engine.index_all(elephants, events, herds)
                progress_bar.progress(100)
                
                snapshot_after = st.session_state.monitor.take_snapshot("After generation")
                st.session_state.large_dataset_generated = True
                
                # Force GC to see circular references
                gc.collect()
                
                st.success(f"""
                ✅ **Dataset Generated Successfully!**
                - **{len(elephants):,}** elephants with circular parent-child references
                - **{len(herds)}** herds
                - **{len(events):,}** historical events
                - **{len(water_sources)}** water sources
                - **Memory used:** +{snapshot_after['process_memory_mb'] - snapshot_before['process_memory_mb']:.2f} MB
                """)
                
                st.rerun()
    
    with col2:
        st.subheader("Current Dataset")
        stats = st.session_state.store.get_stats()
        
        st.metric("Elephants", f"{stats['total_elephants']:,}")
        st.metric("Herds", stats['total_herds'])
        st.metric("Events", f"{stats['total_events']:,}")
        st.metric("Water Sources", stats['total_water_sources'])
        st.metric("Circular References", f"{stats['circular_references']:,}")
        st.metric("Avg Children", f"{stats['avg_children']:.2f}")
        
        if stats['total_elephants'] > 0:
            if st.button("💾 Export to JSON"):
                try:
                    st.session_state.store.export_to_json("data/exported_data.json")
                    st.success("✅ Exported to data/exported_data.json")
                except Exception as e:
                    st.error(f"❌ Export failed: {e}")

# ============================================================================
# TAB 3: Search Engine
# ============================================================================
with tab3:
    st.header("🔍 Search Engine")
    st.markdown("Efficient search using in-memory indexes")
    
    if not st.session_state.large_dataset_generated:
        st.warning("⚠️ No large dataset generated yet. Go to 'Data Generation' tab first!")
    else:
        search_type = st.selectbox(
            "Search Type",
            ["📍 Nearest Water Source", "🏜️ Drought History", "📅 Events by Year", 
             "🐘 Elephant Timeline", "🔔 Migration Alerts", "📊 Search Stats"]
        )
        
        st.divider()
        
        if search_type == "📍 Nearest Water Source":
            st.subheader("Find Nearest Water Source")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                lat = st.number_input("Latitude", value=-19.0, min_value=-25.0, max_value=-15.0, step=0.1)
            with col2:
                lon = st.number_input("Longitude", value=23.0, min_value=20.0, max_value=30.0, step=0.1)
            with col3:
                year = st.number_input("Year (optional)", value=2025, min_value=2000, max_value=2026)
            
            if st.button("🔍 Find Water"):
                source = st.session_state.search_engine.find_nearest_water(lat, lon, year)
                if source:
                    distance = source.distance_to(lat, lon)
                    st.success(f"""
                    **{source.name}** 🌊
                    - Distance: {distance:.2f} units
                    - Capacity: {source.capacity}
                    - Available in {year}: {'✅ Yes' if source.was_available(year) else '❌ No'}
                    """)
                else:
                    st.error("No water sources found")
        
        elif search_type == "🏜️ Drought History":
            st.subheader("Search Drought Years")
            
            col1, col2 = st.columns(2)
            with col1:
                start_year = st.number_input("Start Year", value=2000, min_value=2000, max_value=2025)
            with col2:
                end_year = st.number_input("End Year", value=2025, min_value=2000, max_value=2026)
            
            if st.button("🔍 Search Droughts"):
                results = st.session_state.search_engine.search_droughts(start_year, end_year)
                
                if results:
                    st.warning(f"Found droughts at {len(results)} water sources:")
                    for source_name, years in results.items():
                        st.markdown(f"**{source_name}**: {', '.join(map(str, years))}")
                else:
                    st.success("No droughts found in this period!")
        
        elif search_type == "📅 Events by Year":
            st.subheader("Search Events by Year")
            
            year = st.number_input("Year", value=2020, min_value=2000, max_value=2025)
            
            if st.button("🔍 Search"):
                events = st.session_state.search_engine.search_by_year(year)
                st.info(f"Found {len(events)} events in {year}")
                
                # Group by type
                type_counts = Counter(e.event_type.value for e in events)
                
                for event_type, count in type_counts.most_common():
                    st.markdown(f"- **{event_type}**: {count} events")
                
                # Show first 5
                if events:
                    with st.expander(f"Show first 5 events"):
                        for event in events[:5]:
                            st.markdown(f"**{event.event_type.value}** at {event.location}")
        
        elif search_type == "🐘 Elephant Timeline":
            st.subheader("Elephant Timeline")
            
            elephant_names = [e.name for e in st.session_state.store.elephants[:100]]  # Show first 100
            if elephant_names:
                selected_name = st.selectbox("Select Elephant", elephant_names)
                
                if st.button("🔍 Get Timeline"):
                    timeline = st.session_state.search_engine.get_elephant_timeline(selected_name)
                    
                    if timeline:
                        st.markdown(f"### 🐘 {selected_name}")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Born", timeline['birth_year'])
                        with col2:
                            st.metric("Children", timeline['num_children'])
                        with col3:
                            st.metric("Events", timeline['event_count'])
                        
                        if timeline['parent']:
                            st.info(f"Parent: {timeline['parent']}")
                        
                        if timeline['events']:
                            st.markdown("**Event Timeline:**")
                            for event in timeline['events'][:10]:
                                st.markdown(f"- **{event.year}**: {event.event_type.value} at {event.location}")
        
        elif search_type == "🔔 Migration Alerts":
            st.subheader("Migration Anniversary Alerts")
            
            alerts = st.session_state.search_engine.get_migration_alerts()
            
            if alerts:
                st.info(f"Found {len(alerts)} migration anniversaries:")
                for description, years_ago in alerts:
                    st.markdown(f"🔔 **{description}**")
            else:
                st.warning("No migration anniversaries found")
        
        elif search_type == "📊 Search Stats":
            st.subheader("Search Engine Statistics")
            
            stats = st.session_state.search_engine.get_search_statistics()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Indexed", "✅ Yes" if stats['indexed'] else "❌ No")
                st.metric("Total Events", f"{stats['total_events']:,}")
            with col2:
                st.metric("Years Covered", stats['years_covered'])
                st.metric("Elephants", f"{stats['elephants_indexed']:,}")
            with col3:
                st.metric("Herds", stats['herds_indexed'])
                st.metric("Event Types", stats['event_types'])

# ============================================================================
# TAB 4: Analytics
# ============================================================================
with tab4:
    st.header("📊 Memory & Performance Analytics")
    
    if st.session_state.large_dataset_generated:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Memory Impact")
            
            stats = st.session_state.store.get_stats()
            memory_mb = st.session_state.monitor.get_process_memory_mb()
            
            st.metric("Current Memory", f"{memory_mb:.2f} MB")
            st.metric("Total Objects", f"{len(gc.get_objects()):,}")
            st.metric("Circular References", f"{stats['circular_references']:,}")
            
            # Calculate memory per elephant
            if stats['total_elephants'] > 0:
                memory_per_elephant = (memory_mb / stats['total_elephants']) * 1024  # KB
                st.metric("Memory per Elephant", f"{memory_per_elephant:.2f} KB")
        
        with col2:
            st.subheader("GC Statistics")
            
            gc_count = gc.get_count()
            st.metric("GC Generation 0", gc_count[0])
            st.metric("GC Generation 1", gc_count[1])
            st.metric("GC Generation 2", gc_count[2])
            
            if st.button("🧹 Force Garbage Collection"):
                collected = gc.collect()
                st.success(f"Collected {collected} objects")
                st.rerun()
        
        st.divider()
        
        st.subheader("Dataset Overview")
        overview_data = {
            "Category": ["Elephants", "Herds", "Events", "Water Sources", "Circular Refs"],
            "Count": [
                stats['total_elephants'],
                stats['total_herds'],
                stats['total_events'],
                stats['total_water_sources'],
                stats['circular_references']
            ]
        }
        st.bar_chart(overview_data, x="Category", y="Count")
    
    else:
        st.info("📊 Generate a large dataset first to see analytics")

# Footer
st.divider()
st.caption("🐘 Elephant Memory Cloud - Demonstrating Python's Cyclic Garbage Collection at Scale")
