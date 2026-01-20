"""
Search engine for elephant archive with efficient indexing.
Operates on in-memory objects with dictionary-based indexes.
"""

from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from models.elephant import Elephant
from models.event import Event, EventType
from models.water_source import WaterSource
from models.herd import Herd


class ElephantSearchEngine:
    """
    Efficient search across elephant archive using in-memory indexes.
    Builds dictionary-based indexes for O(1) lookups.
    """
    
    def __init__(self):
        # Event indexes
        self._year_index: Dict[int, List[Event]] = defaultdict(list)
        self._location_index: Dict[str, List[Event]] = defaultdict(list)
        self._elephant_index: Dict[str, List[Event]] = defaultdict(list)
        self._event_type_index: Dict[EventType, List[Event]] = defaultdict(list)
        
        # Elephant indexes
        self._elephant_by_name: Dict[str, Elephant] = {}
        self._elephants_by_year: Dict[int, List[Elephant]] = defaultdict(list)
        
        # Herd indexes
        self._herd_by_name: Dict[str, Herd] = {}
        
        self._indexed = False
    
    def index_all(
        self, 
        elephants: List[Elephant],
        events: List[Event],
        herds: List[Herd]
    ):
        """
        Build all search indexes from in-memory objects.
        
        Args:
            elephants: List of all elephants
            events: List of all events
            herds: List of all herds
        """
        self._indexed = False
        
        # Clear existing indexes
        self._year_index.clear()
        self._location_index.clear()
        self._elephant_index.clear()
        self._event_type_index.clear()
        self._elephant_by_name.clear()
        self._elephants_by_year.clear()
        self._herd_by_name.clear()
        
        # Index elephants
        for elephant in elephants:
            self._elephant_by_name[elephant.name] = elephant
            self._elephants_by_year[elephant.birth_year].append(elephant)
        
        # Index herds
        for herd in herds:
            self._herd_by_name[herd.name] = herd
        
        # Index events
        for event in events:
            # Year index
            self._year_index[event.year].append(event)
            
            # Location index (group by region)
            location_key = self._get_location_key(event.location)
            self._location_index[location_key].append(event)
            
            # Event type index
            self._event_type_index[event.event_type].append(event)
            
            # Elephant index (each elephant mentioned in event)
            for elephant in event.involved_elephants:
                self._elephant_index[elephant.name].append(event)
        
        self._indexed = True
    
    @staticmethod
    def _get_location_key(location: str) -> str:
        """Convert location string to region key for indexing."""
        try:
            # Location format: "lat, lon"
            lat, lon = map(float, location.split(','))
            # Group into 1-degree grid cells
            return f"{int(lat)},{int(lon)}"
        except:
            return "unknown"
    
    def find_nearest_water(
        self, 
        lat: float, 
        lon: float, 
        year: Optional[int] = None
    ) -> Optional[WaterSource]:
        """
        Find nearest available water source to given coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            year: Optional year to check availability
            
        Returns:
            Nearest WaterSource or None
        """
        return WaterSource.find_nearest(lat, lon, year)
    
    def search_droughts(self, start_year: int, end_year: int) -> Dict[str, List[int]]:
        """
        Find drought years (when water sources were unavailable).
        
        Args:
            start_year: Start year of search range
            end_year: End year of search range
            
        Returns:
            Dict mapping water source names to list of drought years
        """
        results = {}
        
        for source in WaterSource.get_all_sources():
            drought_years = [
                year for year in range(start_year, end_year + 1)
                if not source.was_available(year)
            ]
            if drought_years:
                results[source.name] = drought_years
        
        return results
    
    def search_by_year(self, year: int) -> List[Event]:
        """
        Search events by year (O(1) lookup using index).
        
        Args:
            year: Year to search for
            
        Returns:
            List of events in that year
        """
        return self._year_index.get(year, [])
    
    def search_by_year_range(self, start_year: int, end_year: int) -> List[Event]:
        """Search events in year range."""
        events = []
        for year in range(start_year, end_year + 1):
            events.extend(self._year_index.get(year, []))
        return events
    
    def search_by_elephant(self, name: str) -> List[Event]:
        """
        Search events involving specific elephant (O(1) lookup).
        
        Args:
            name: Elephant name
            
        Returns:
            List of events involving this elephant
        """
        return self._elephant_index.get(name, [])
    
    def search_by_event_type(self, event_type: EventType) -> List[Event]:
        """Search events by type."""
        return self._event_type_index.get(event_type, [])
    
    def search_by_location(self, lat: float, lon: float, radius: int = 1) -> List[Event]:
        """
        Search events near location.
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Search radius in degree grid cells
            
        Returns:
            List of nearby events
        """
        events = []
        center_lat, center_lon = int(lat), int(lon)
        
        for dlat in range(-radius, radius + 1):
            for dlon in range(-radius, radius + 1):
                key = f"{center_lat + dlat},{center_lon + dlon}"
                events.extend(self._location_index.get(key, []))
        
        return events
    
    def get_elephant_timeline(self, name: str) -> Dict[str, any]:
        """
        Get complete timeline for an elephant.
        
        Args:
            name: Elephant name
            
        Returns:
            Dict with elephant info and event timeline
        """
        elephant = self._elephant_by_name.get(name)
        if not elephant:
            return {}
        
        events = self.search_by_elephant(name)
        events_sorted = sorted(events, key=lambda e: e.year)
        
        return {
            "elephant": elephant,
            "birth_year": elephant.birth_year,
            "num_children": len(elephant.children),
            "parent": elephant.parent.name if elephant.parent else None,
            "events": events_sorted,
            "event_count": len(events_sorted)
        }
    
    def get_migration_alerts(self, current_year: int = 2026) -> List[Tuple[str, int]]:
        """
        Get migration anniversary alerts.
        
        Args:
            current_year: Current year for calculating anniversaries
            
        Returns:
            List of (description, years_ago) tuples
        """
        alerts = []
        migration_events = self._event_type_index.get(EventType.MIGRATION, [])
        
        for event in migration_events:
            years_ago = current_year - event.year
            if years_ago in [5, 10, 15, 20, 25]:  # Milestone anniversaries
                alerts.append((
                    f"{years_ago}-year anniversary of {event.description}",
                    years_ago
                ))
        
        return sorted(alerts, key=lambda x: x[1])
    
    def get_search_statistics(self) -> Dict[str, int]:
        """Get statistics about indexed data."""
        return {
            "indexed": self._indexed,
            "total_events": sum(len(events) for events in self._year_index.values()),
            "years_covered": len(self._year_index),
            "elephants_indexed": len(self._elephant_by_name),
            "herds_indexed": len(self._herd_by_name),
            "event_types": len(self._event_type_index)
        }
