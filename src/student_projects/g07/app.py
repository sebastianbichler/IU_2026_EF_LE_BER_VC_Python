#!/usr/bin/env python3
"""
Elephant Memory Cloud - Streamlit Dashboard
Real-time memory monitoring, large-scale data generation, and efficient search.
"""

import streamlit as st
import gc
import plotly.graph_objects as go
from collections import Counter
from models import Elephant, Herd, Event, WaterSource
from models.event import EventType
from memory import MemoryMonitor
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
    st.session_state.store = get_store()
    st.session_state.search_engine = ElephantSearchEngine()
    st.session_state.large_dataset_generated = False
    st.session_state.references_broken = False  # Track if we've broken references

# Header
st.title("🐘 Elephant Memory Cloud")
st.markdown("**Archiv-Management mit Circular Reference Demonstration & Efficient Search**")
st.divider()

# Create tabs for different functionality
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Dashboard", 
    "🗄️ Data Generation", 
    "🔍 Search Engine",
    "🌳 Genealogy"
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
    
    # Two-step GC demonstration
    st.subheader("🎯 Circular Reference Demonstration")
    
    # Show current state with clear metrics
    if st.session_state.references_broken:
        # After breaking references - show the orphaned state
        st.error("⚠️ **ORPHANED STATE - References Broken!**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("📦 Elephants in Store", "0", delta="Cleared", delta_color="off")
        with col_b:
            orphaned_count = Elephant.get_instance_count()
            st.metric("👻 Orphaned in Memory", f"{orphaned_count:,}", delta="Still alive!", delta_color="inverse")
        with col_c:
            st.metric("♻️ GC Status", "Pending", delta="Not run yet", delta_color="off")
        
        st.warning("💡 **This proves circular references prevent Python's reference counting from working!**")
        st.info("👉 Click 'Run GC' to finally free them →")
    elif st.session_state.large_dataset_generated:
        # Before breaking references - show the active state
        st.success("✅ **ACTIVE STATE - Data in Memory**")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            active_count = store_stats['total_elephants']
            st.metric("📦 Elephants in Store", f"{active_count:,}", delta="Reachable")
        with col_b:
            memory_count = Elephant.get_instance_count()
            st.metric("💾 In Memory", f"{memory_count:,}", delta="Active")
        with col_c:
            st.metric("🔗 Circular Refs", f"{store_stats['circular_references']:,}", delta="Parent↔Child")
        
        st.info("👉 Click 'Break References' to remove from store (but watch them stay in memory!) →")
    
    # Buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("💔 Break References", 
                     disabled=not st.session_state.large_dataset_generated or st.session_state.references_broken,
                     use_container_width=True,
                     type="secondary"):
            # Clear store - makes elephants unreachable but doesn't collect them yet
            st.session_state.store.clear()
            st.session_state.large_dataset_generated = False
            st.session_state.references_broken = True
            st.rerun()
    
    with col_btn2:
        if st.button("♻️ Run GC", 
                     disabled=not st.session_state.references_broken,
                     use_container_width=True,
                     type="primary"):
            # Take snapshot before GC
            count_before = Elephant.get_instance_count()
            memory_before = st.session_state.monitor.get_process_memory_mb()
            
            # Force GC - now it can collect the orphaned cycles
            collected = gc.collect()
            
            # Take snapshot after GC
            count_after = Elephant.get_instance_count()
            memory_after = st.session_state.monitor.get_process_memory_mb()
            
            st.session_state.references_broken = False
            
            st.success("✅ **Garbage Collection Complete!**")
            st.metric("🐘 Elephants Freed", f"{count_before - count_after:,}")
            st.metric("🗑️ Total Objects Collected", f"{collected:,}")
            st.metric("💾 Memory Freed", f"{memory_before - memory_after:.2f} MB")
            st.balloons()
            st.success("🎯 **Cyclic GC successfully cleaned up circular references that reference counting couldn't handle!**")
            st.rerun()
    
    with col_btn3:
        if st.button("🔄 Refresh Statistics", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Live Memory Distribution Pie Chart - Always visible
    st.subheader("📊 Live Memory Distribution")
    
    col_chart, col_metrics = st.columns([2, 1])
    
    with col_chart:
        gc.collect()
        
        # Calculate memory breakdown
        baseline_memory = 60  # Streamlit baseline overhead in MB
        total_memory = memory_mb
        
        # Determine elephant count based on state
        if st.session_state.references_broken:
            elephant_count = Elephant.get_instance_count()
        elif store_stats['total_elephants'] > 0:
            elephant_count = store_stats['total_elephants']
        else:
            elephant_count = 0
        
        # Calculate memory usage
        elephants_memory = elephant_count * 0.05
        events_memory = store_stats['total_events'] * 0.002
        other_data_memory = (store_stats['total_herds'] + store_stats['total_water_sources']) * 0.01
        
        # Calculate remaining memory (Python overhead, GC structures, etc.)
        data_memory = elephants_memory + events_memory + other_data_memory
        other_memory = max(0, total_memory - baseline_memory - data_memory)
        
        # Create labels and values
        labels = []
        values = []
        colors = []
        
        labels.append('🔹 Streamlit Framework')
        values.append(baseline_memory)
        colors.append('#95a5a6')
        
        if elephant_count > 0:
            # Show if elephants are orphaned or active
            if st.session_state.references_broken:
                labels.append('👻 Orphaned Elephants (in memory!)')
                colors.append('#e74c3c')  # Red for orphaned
            else:
                labels.append('🐘 Elephants')
                colors.append('#3498db')  # Blue for active
            values.append(elephants_memory)
        
        if events_memory > 0:
            labels.append('📅 Events')
            values.append(events_memory)
            colors.append('#2ecc71')
        
        if other_data_memory > 0:
            labels.append('📊 Other Data')
            values.append(other_data_memory)
            colors.append('#f39c12')
        
        if other_memory > 0:
            labels.append('🧩 Other Objects')
            values.append(other_memory)
            colors.append('#9b59b6')
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textfont=dict(size=12),
            hovertemplate='<b>%{label}</b><br>%{value:.2f} MB<br>%{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title={
                'text': f"Total Process Memory: {total_memory:.2f} MB",
                'x': 0.5,
                'xanchor': 'center'
            },
            height=400,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_metrics:
        st.markdown("### 📈 Memory Breakdown")
        st.metric("Total Memory", f"{memory_mb:.2f} MB")
        st.metric("Streamlit Overhead", f"{baseline_memory:.0f} MB")
        
        if elephant_count > 0:
            if st.session_state.references_broken:
                st.metric("👻 Orphaned Elephants", elephant_count, delta="Still in memory!", delta_color="inverse")
            else:
                st.metric("🐘 Active Elephants", elephant_count)
            st.metric("Elephant Memory", f"{elephants_memory:.2f} MB")
        else:
            st.info("🐘 No elephants in memory")
        
        if store_stats['total_events'] > 0:
            st.metric("📅 Events Memory", f"{events_memory:.2f} MB")
    
    st.divider()
    
    # Status and instructions
    if not st.session_state.large_dataset_generated:
        st.info("👉 **Get Started:** Go to the 'Data Generation' tab to create a large dataset with circular references")
    else:
        st.success(f"✅ **Archive Active:** {store_stats['total_elephants']:,} elephants, {store_stats['circular_references']:,} circular references")

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
            children_per_elephant = st.number_input(
                "Max Children per Elephant", 
                min_value=2, 
                max_value=5, 
                value=3
            )
            num_herds = st.number_input("Number of Herds", min_value=5, max_value=50, value=10)
        
        with col_c:
            num_events = st.number_input("Number of Events", min_value=100, max_value=10000, value=1000, step=100)
        
        # Calculate accurate estimate based on actual generation logic
        # random.randint(1, children_per_elephant + 1) gives 1, 2, ..., children_per_elephant+1
        # Average = (1 + children_per_elephant + 1) / 2
        avg_children = (children_per_elephant + 2) / 2
        
        # Geometric series: sum of avg_children^i for i from 0 to generations-1
        if avg_children == 1:
            elephants_per_family = generations  # Special case: 1+1+1+...
        else:
            elephants_per_family = (avg_children ** generations - 1) / (avg_children - 1)
        
        estimated_elephants = int(num_families * elephants_per_family)
        
        # Realistic range: 70% to 140% due to random variation
        range_low = int(estimated_elephants * 0.7)
        range_high = int(estimated_elephants * 1.4)
        
        st.info(f"📊 **Estimated Dataset**: ~{estimated_elephants:,} elephants (range: {range_low:,}-{range_high:,}), {num_events:,} events, {num_herds} herds")
        
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
        
        if stats['total_elephants'] > 0 and st.button("💾 Export to JSON"):
            try:
                st.session_state.store.export_to_json("data/exported_data.json")
                st.success("✅ Exported successfully")
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
                
                if events:
                    type_counts = Counter(e.event_type.value for e in events)
                    event_types = list(type_counts.keys())
                    counts = list(type_counts.values())
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=event_types,
                            y=counts,
                            marker=dict(
                                color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'][:len(event_types)]
                            ),
                            text=counts,
                            textposition='auto',
                        )
                    ])
                    
                    fig.update_layout(
                        title=f"Event Distribution in {year}",
                        xaxis_title="Event Type",
                        yaxis_title="Count",
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show all events
                    with st.expander(f"Show all {len(events)} events"):
                        for event in events:
                            st.markdown(f"**{event.event_type.value}** at {event.location}")
                else:
                    st.warning(f"No events found in {year}")
        
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
# TAB 4: Elephant Genealogy & Relationships
# ============================================================================
with tab4:
    st.header("🌳 Elephant Genealogy & Family Relationships")
    
    if not st.session_state.large_dataset_generated or len(st.session_state.store.elephants) == 0:
        st.info("🐘 Generate a dataset first to explore elephant families and relationships")
    else:
        elephants = st.session_state.store.elephants
        
        # Calculate family statistics
        families = {}
        generations = {}
        orphans = []
        max_depth = 0
        
        for elephant in elephants:
            # Find root ancestor
            root = elephant
            depth = 0
            while root.parent and depth < 100:  # Prevent infinite loops
                root = root.parent
                depth += 1
            
            max_depth = max(max_depth, depth)
            
            if root.name not in families:
                families[root.name] = []
            families[root.name].append(elephant)
            
            # Track generation depth
            generations[elephant.name] = depth
            
            # Find orphans (no parent, but not a root with children)
            if not elephant.parent and len(elephant.children) == 0:
                orphans.append(elephant)
        
        # Overview metrics
        st.subheader("📊 Family Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🌳 Total Families", len(families))
        with col2:
            avg_family_size = len(elephants) / len(families) if families else 0
            st.metric("👥 Avg Family Size", f"{avg_family_size:.1f}")
        with col3:
            st.metric("🔢 Max Generation Depth", max_depth)
        with col4:
            total_circular_refs = sum(1 for e in elephants if e.parent)
            st.metric("♻️ Circular Refs", f"{total_circular_refs:,}")
        with col5:
            st.metric("🍃 Orphans", len(orphans))
        
        st.divider()
        
        # Family Tree Browser
        st.subheader("🌳 Family Tree Explorer")
        
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            # Sort families by size
            sorted_families = sorted(families.items(), key=lambda x: len(x[1]), reverse=True)
            family_options = [f"{root} ({len(members)} elephants)" for root, members in sorted_families]
            
            if family_options:
                selected_family = st.selectbox("Select a Family", family_options)
                selected_root = selected_family.split(" (")[0]
                
                # Get the family
                family_members = families[selected_root]
                root_elephant = next(e for e in family_members if e.name == selected_root)
                
                # Display family tree as hierarchical chart
                st.markdown("### 🌳 Family Tree")
                
                # Build graph structure using dictionaries
                nodes = {}  # {name: {generation, birth_year, num_children}}
                edges = []  # [(parent_name, child_name), ...]
                
                def add_to_graph(elephant, generation=0):
                    """Recursively add elephant and children to graph"""
                    nodes[elephant.name] = {
                        'generation': generation,
                        'birth_year': elephant.birth_year,
                        'num_children': len(elephant.children)
                    }
                    
                    for child in elephant.children:
                        edges.append((elephant.name, child.name))
                        add_to_graph(child, generation + 1)
                
                add_to_graph(root_elephant)
                
                # Use hierarchical layout - position nodes by generation
                pos = {}
                generation_nodes = {}
                
                # Group nodes by generation
                for node_name, node_data in nodes.items():
                    gen = node_data['generation']
                    if gen not in generation_nodes:
                        generation_nodes[gen] = []
                    generation_nodes[gen].append(node_name)
                
                # Position nodes: y by generation, x spread evenly
                for gen, node_list in generation_nodes.items():
                    y = -gen * 100  # Vertical spacing
                    width = len(node_list)
                    for i, node_name in enumerate(node_list):
                        # Center the nodes horizontally
                        x = (i - width/2) * 150  # Horizontal spacing
                        pos[node_name] = (x, y)
                
                # Create edges
                edge_x = []
                edge_y = []
                for parent, child in edges:
                    x0, y0 = pos[parent]
                    x1, y1 = pos[child]
                    edge_x.extend([x0, x1, None])
                    edge_y.extend([y0, y1, None])
                
                edge_trace = go.Scatter(
                    x=edge_x, y=edge_y,
                    line=dict(width=2, color='#95a5a6'),
                    hoverinfo='none',
                    mode='lines'
                )
                
                # Create nodes with generation-based colors
                node_x = []
                node_y = []
                node_text = []
                node_color = []
                node_hover = []
                
                colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
                
                for node_name, node_data in nodes.items():
                    x, y = pos[node_name]
                    node_x.append(x)
                    node_y.append(y)
                    
                    generation = node_data['generation']
                    birth_year = node_data['birth_year']
                    num_children = node_data['num_children']
                    
                    # Short name for display
                    short_name = node_name.split('_')[0] if '_' in node_name else node_name[:8]
                    node_text.append(short_name)
                    
                    # Color by generation
                    node_color.append(colors[generation % len(colors)])
                    
                    # Hover info
                    node_hover.append(f"<b>{node_name}</b><br>Born: {birth_year}<br>Children: {num_children}<br>Generation: {generation}")
                
                node_trace = go.Scatter(
                    x=node_x, y=node_y,
                    mode='markers+text',
                    hoverinfo='text',
                    text=node_text,
                    hovertext=node_hover,
                    textposition="bottom center",
                    textfont=dict(size=10),
                    marker=dict(
                        color=node_color,
                        size=20,
                        line=dict(width=2, color='white')
                    )
                )
                
                # Display family tree
                st.plotly_chart(
                    go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f"Family Tree: {selected_root} ({len(family_members)} elephants)",
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=20,r=20,t=60),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            height=600
                        )
                    ),
                    use_container_width=True
                )
                st.caption("🎨 Colors represent different generations | Hover over nodes for details")
        
        with col_right:
            st.markdown("### 📊 Family Statistics")
            
            # Generation distribution
            gen_counts = Counter(generations.values())
            st.markdown("**Generation Distribution:**")
            for gen in sorted(gen_counts.keys()):
                st.metric(f"Generation {gen}", gen_counts[gen])
        
        st.divider()
        
        # Relationship Analysis
        st.subheader("🔍 Relationship Analysis")
        
        # Combined metrics for both children and age
        avg_children = sum(len(e.children) for e in elephants) / len(elephants)
        current_year = 2026
        valid_elephants = [e for e in elephants if e.birth_year <= current_year]
        
        if valid_elephants:
            ages = [current_year - e.birth_year for e in valid_elephants]
            oldest = max(valid_elephants, key=lambda e: current_year - e.birth_year)
            youngest = min(valid_elephants, key=lambda e: current_year - e.birth_year)
            
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Average Children", f"{avg_children:.2f}")
            with col_m2:
                st.metric("Average Age", f"{sum(ages) / len(ages):.1f} years")
            with col_m3:
                st.success(f"🧓 **{oldest.name}**\n\n{current_year - oldest.birth_year} years")
            with col_m4:
                st.info(f"🍼 **{youngest.name}**\n\n{current_year - youngest.birth_year} years")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("### 👨‍👩‍👧‍👦 Children Distribution")
            
            children_dist = Counter(len(e.children) for e in elephants)
            
            # Get all possible child counts from 0 to max
            max_children_count = max(len(e.children) for e in elephants)
            child_counts = list(range(max_children_count + 1))
            elephant_counts = [children_dist.get(c, 0) for c in child_counts]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=child_counts,
                    y=elephant_counts,
                    marker=dict(
                        color=['#e74c3c' if c == 0 else '#3498db' for c in child_counts]
                    ),
                    text=elephant_counts,
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Number of Children per Elephant",
                xaxis_title="Number of Children",
                yaxis_title="Number of Elephants",
                height=350,
                showlegend=False,
                xaxis=dict(dtick=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            st.markdown("### 📅 Age Distribution")
            
            # Birth year distribution
            birth_years = Counter(e.birth_year for e in elephants)
            years = sorted(birth_years.keys())
            born_counts = [birth_years[y] for y in years]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=years,
                y=born_counts,
                mode='lines+markers',
                name='Elephants Born',
                line=dict(color='#2ecc71', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(46, 204, 113, 0.2)'
            ))
            
            fig.update_layout(
                title="Elephant Births Over Time",
                xaxis_title="Birth Year",
                yaxis_title="Elephants Born",
                height=350,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Orphan detection
        if orphans:
            st.divider()
            st.subheader("🍃 Orphaned Elephants")
            st.warning(f"Found {len(orphans)} orphaned elephants (no parents, no children)")
            
            with st.expander("View Orphans"):
                for orphan in orphans[:20]:
                    st.caption(f"🐘 {orphan.name} (Born: {orphan.birth_year})")

# Footer
st.divider()
st.caption("🐘 Elephant Memory Cloud - Demonstrating Python's Cyclic Garbage Collection at Scale")

