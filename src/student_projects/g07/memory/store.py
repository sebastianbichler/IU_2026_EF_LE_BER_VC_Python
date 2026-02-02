"""
In-memory object store for elephant archive.
Manages all elephants, herds, events, and water sources in RAM.
"""

from typing import List, Optional, Dict, Any
import json
from pathlib import Path
from models.elephant import Elephant
from models.herd import Herd
from models.event import Event
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
        """Clear all data from memory (for demo - keeps circular references intact)."""
        # Just remove from store, keep circular references for demo
        self.elephants.clear()
        self.herds.clear()
        self.events.clear()
        self.water_sources.clear()
        self._elephant_by_name.clear()
        
        # Also clear class-level storage in WaterSource and Event
        WaterSource._all_sources.clear()
        Event._all_events.clear()
    
    def clear_and_cleanup(self):
        """Clear all data and break circular references for full cleanup."""
        # Break circular references before clearing
        for elephant in self.elephants:
            elephant._parent = None
            elephant.children.clear()
            elephant.herd = None
        
        for herd in self.herds:
            herd.members.clear() if hasattr(herd, 'members') else None
        
        self.elephants.clear()
        self.herds.clear()
        self.events.clear()
        self.water_sources.clear()
        self._elephant_by_name.clear()
        
        # Also clear class-level storage in WaterSource and Event
        WaterSource._all_sources.clear()
        Event._all_events.clear()
        
        # Reset elephant tracking to clear stale IDs
        Elephant.reset_tracking()
    
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
        
        Args:
            filepath: Path where JSON file will be saved
            
        Raises:
            ValueError: If filepath is invalid
            IOError: If file cannot be written
        """
        if not filepath:
            raise ValueError("Filepath cannot be empty")
        
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
        
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except (IOError, OSError) as e:
            raise IOError(f"Failed to write to {filepath}: {str(e)}")
    
    def get_circular_reference_count(self) -> int:
        """
        Count total circular references in memory.
        Each parent-child relationship creates a cycle (bidirectional).
        Each herd membership creates an elephant↔herd reference.
        """
        count = 0
        for elephant in self.elephants:
            # Each child relationship is bidirectional: parent→child and child→parent
            # We count each unique relationship once (already counted via children list)
            count += len(elephant.children)
            # Each elephant with a herd creates one elephant→herd reference
            # (herd→elephant is already counted in herd.members)
            if elephant.herd is not None:
                count += 1
        return count


# Global singleton instance
_store = MemoryStore()


def get_store() -> MemoryStore:
    """Get the global memory store instance."""
    return _store
