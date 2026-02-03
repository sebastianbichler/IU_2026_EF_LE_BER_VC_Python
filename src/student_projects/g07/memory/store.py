"""
In-memory object store for elephant archive.
Manages all elephants, herds, events, and water sources in RAM.
"""

from typing import List, Optional, Dict, Any
import json
from pathlib import Path
from models.elephant import Elephant
from models.herd import Herd
from models.event import Event, EventType
from models.water_source import WaterSource


class MemoryStore:
    """
    Centralized in-memory storage for all elephant archive data.
    All objects live in Python memory with circular references intact.
    """
    
    def __init__(self):
        self.elephants: List[Elephant] = []
        self.herds: List[Herd] = []
        self.events: List[Event] = []
        self.water_sources: List[WaterSource] = []
        self._elephant_by_name: Dict[str, Elephant] = {}
    
    def clear(self):
        """Clear all data from memory."""
        self.elephants.clear()
        self.herds.clear()
        self.events.clear()
        self.water_sources.clear()
        self._elephant_by_name.clear()
        
        # Also clear class-level storage in WaterSource
        WaterSource._all_sources.clear()
    
    def add_elephant(self, elephant: Elephant):
        """Add elephant to store."""
        self.elephants.append(elephant)
        self._elephant_by_name[elephant.name] = elephant
    
    def add_elephants(self, elephants: List[Elephant]):
        """Add multiple elephants."""
        for elephant in elephants:
            self.add_elephant(elephant)
    
    def add_herd(self, herd: Herd):
        """Add herd to store."""
        self.herds.append(herd)
    
    def add_herds(self, herds: List[Herd]):
        """Add multiple herds."""
        self.herds.extend(herds)
    
    def add_event(self, event: Event):
        """Add event to store."""
        self.events.append(event)
    
    def add_events(self, events: List[Event]):
        """Add multiple events."""
        self.events.extend(events)
    
    def add_water_source(self, source: WaterSource):
        """Add water source to store."""
        self.water_sources.append(source)
    
    def add_water_sources(self, sources: List[WaterSource]):
        """Add multiple water sources."""
        self.water_sources.extend(sources)
    
    def get_elephant_by_name(self, name: str) -> Optional[Elephant]:
        """Find elephant by name."""
        return self._elephant_by_name.get(name)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data."""
        total_relationships = sum(
            len(e.children) + (1 if e.parent else 0) 
            for e in self.elephants
        )
        
        return {
            "total_elephants": len(self.elephants),
            "total_herds": len(self.herds),
            "total_events": len(self.events),
            "total_water_sources": len(self.water_sources),
            "circular_references": total_relationships,
            "avg_children": sum(len(e.children) for e in self.elephants) / max(len(self.elephants), 1)
        }
    
    def export_to_json(self, filepath: str):
        """
        Export current state to JSON (simplified).
        Only exports basic data, not full circular references.
        """
        data = {
            "elephants": [
                {
                    "name": e.name,
                    "birth_year": e.birth_year,
                    "gender": e.gender,
                    "children": [c.name for c in e.children]
                }
                for e in self.elephants
            ],
            "herds": [
                {
                    "name": h.name,
                    "territory": h.territory,
                    "members": [m.name for m in h.members]
                }
                for h in self.herds
            ],
            "events": [
                {
                    "type": e.event_type.value,
                    "year": e.year,
                    "location": e.location,
                    "description": e.description
                }
                for e in self.events
            ]
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_circular_reference_count(self) -> int:
        """
        Count total circular references in memory.
        Each parent-child relationship creates a cycle.
        """
        count = 0
        for elephant in self.elephants:
            # Each child relationship is a potential circular reference
            count += len(elephant.children)
            # Each herd membership is also a reference
            for herd in self.herds:
                if elephant in herd.members:
                    count += 1
        return count


# Global singleton instance
_store = MemoryStore()


def get_store() -> MemoryStore:
    """Get the global memory store instance."""
    return _store
