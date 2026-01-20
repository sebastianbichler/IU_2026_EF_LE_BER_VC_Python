"""
Event model for tracking significant occurrences.
"""

from typing import List, Optional
from datetime import date
from enum import Enum


class EventType(Enum):
    """Types of events in elephant history."""
    BIRTH = "birth"
    MIGRATION = "migration"
    WATER_DISCOVERY = "water_discovery"
    DROUGHT = "drought"
    GATHERING = "gathering"
    DANGER = "danger"


class Event:
    """
    Represents a historical event in the savanna.
    
    Links elephants, herds, and locations together.
    Potential for complex circular references.
    """
    
    _all_events: List['Event'] = []
    
    def __init__(
        self,
        event_type: EventType,
        year: int,
        location: str,
        description: str,
        involved_elephants: Optional[List['Elephant']] = None,
        involved_herds: Optional[List['Herd']] = None
    ):
        """
        Args:
            event_type: Type of event
            year: Year of occurrence
            location: Location name/coordinates
            description: Event description
            involved_elephants: Elephants involved
            involved_herds: Herds involved
        """
        self.event_type = event_type
        self.year = year
        self.location = location
        self.description = description
        self.involved_elephants = involved_elephants or []
        self.involved_herds = involved_herds or []
        self.timestamp = date.today()
        
        # Index this event
        Event._all_events.append(self)
    
    @classmethod
    def search_by_year(cls, year: int) -> List['Event']:
        """Find all events in a specific year."""
        return [e for e in cls._all_events if e.year == year]
    
    @classmethod
    def search_by_location(cls, location: str) -> List['Event']:
        """Find all events at a location."""
        return [e for e in cls._all_events if location.lower() in e.location.lower()]
    
    @classmethod
    def search_by_elephant(cls, elephant: 'Elephant') -> List['Event']:
        """Find all events involving a specific elephant."""
        return [e for e in cls._all_events if elephant in e.involved_elephants]
    
    @classmethod
    def search_by_type(cls, event_type: EventType) -> List['Event']:
        """Find all events of a specific type."""
        return [e for e in cls._all_events if e.event_type == event_type]
    
    @classmethod
    def get_all_events(cls) -> List['Event']:
        """Get all recorded events."""
        return cls._all_events.copy()
    
    @classmethod
    def clear_all(cls):
        """Clear all events (for testing)."""
        cls._all_events.clear()
    
    def __repr__(self) -> str:
        return (f"Event({self.event_type.value}, {self.year}, "
                f"'{self.location}', elephants={len(self.involved_elephants)})")
