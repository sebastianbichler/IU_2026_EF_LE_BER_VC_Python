from __future__ import annotations

import sys
from pathlib import Path


# Ensure g07 modules can be imported when running pytest from repo root.
G07_ROOT = Path(__file__).resolve().parents[2] / "src" / "student_projects" / "g07"
sys.path.insert(0, str(G07_ROOT))


from models.elephant import Elephant
from models.event import Event, EventType
from models.herd import Herd
from search.engine import ElephantSearchEngine
from memory.store import MemoryStore


def setup_function():
    """Reset global/class-level registries between tests."""
    Elephant.reset_tracking()
    Event.clear_all()


def test_search_engine_indexes_and_queries():
    e1 = Elephant("Ella", 2000, "F")
    e2 = Elephant("Eric", 2001, "M")

    herd = Herd("Herd_A", "Central Plains")
    herd.add_member(e1)
    herd.add_member(e2)

    event = Event(
        event_type=EventType.MIGRATION,
        year=2020,
        location="-19.0, 23.0",
        description="migration test event",
        involved_elephants=[e1, e2],
        involved_herds=[herd],
    )

    engine = ElephantSearchEngine()
    engine.index_all([e1, e2], [event], [herd])

    assert engine.search_by_year(2020) == [event]
    assert engine.search_by_elephant("Ella") == [event]
    assert engine.search_by_elephant("Eric") == [event]

    # Location grid lookup should find the event at its own cell
    nearby = engine.search_by_location(-19.0, 23.0, radius=0)
    assert nearby == [event]

    stats = engine.get_search_statistics()
    assert stats["indexed"] is True
    assert stats["total_events"] == 1
    assert stats["elephants_indexed"] == 2


def test_memory_store_clear_and_cleanup_breaks_relationships():
    store = MemoryStore()

    parent = Elephant("Matriarch", 1980, "F")
    child = Elephant("Child", 2000, "M")
    parent.add_child(child)

    herd = Herd("Herd_B", "Delta Region")
    herd.add_member(parent)
    herd.add_member(child)

    store.add_elephants([parent, child])
    store.add_herds([herd])

    assert child.parent is parent
    assert child in parent.children
    assert parent.herd is herd

    store.clear_and_cleanup()

    # Store emptied
    assert store.elephants == []
    assert store.herds == []

    # Relationships broken (important for predictable cleanup)
    assert child.parent is None
    assert child.children == []
    assert child.herd is None
    assert parent.parent is None
    assert parent.children == []
    assert parent.herd is None
    assert herd.members == []

    # Tracking reset is part of the cleanup semantics
    assert Elephant.get_instance_count() == 0
