"""
Water source model with historical data tracking.
"""

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.elephant import Elephant


class WaterSource:
    """
    Represents a water source with historical availability data.
    """
    
    _all_sources: List['WaterSource'] = []
    
    def __init__(
        self,
        name: str,
        latitude: float,
        longitude: float,
        capacity: str  # "small", "medium", "large"
    ):
        """
        Args:
            name: Name of water source
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            capacity: Size/capacity category
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.capacity = capacity
        
        # Historical data: year -> availability (True/False)
        self.availability_history: Dict[int, bool] = {}
        
        # Visits: year -> list of elephants that visited
        self.visit_history: Dict[int, List['Elephant']] = {}
        
        WaterSource._all_sources.append(self)
    
    def record_availability(self, year: int, available: bool):
        """Record whether water was available in a given year."""
        self.availability_history[year] = available
    
    def record_visit(self, year: int, elephant: 'Elephant'):
        """Record an elephant visit."""
        if year not in self.visit_history:
            self.visit_history[year] = []
        if elephant not in self.visit_history[year]:
            self.visit_history[year].append(elephant)
    
    def was_available(self, year: int) -> bool:
        """Check if water was available in a given year."""
        return self.availability_history.get(year, True)
    
    def get_drought_years(self) -> List[int]:
        """Get years when this source was dry."""
        return [year for year, avail in self.availability_history.items() if not avail]
    
    def distance_to(self, lat: float, lon: float) -> float:
        """
        Calculate approximate distance to coordinates.
        Simple Euclidean distance (not accurate for real Earth, but sufficient for demo).
        """
        return ((self.latitude - lat) ** 2 + (self.longitude - lon) ** 2) ** 0.5
    
    @classmethod
    def find_nearest(cls, lat: float, lon: float, year: int = None) -> 'WaterSource':
        """
        Find nearest water source to coordinates.
        Optionally filter by availability in a specific year.
        """
        sources = cls._all_sources
        
        if year is not None:
            sources = [s for s in sources if s.was_available(year)]
        
        if not sources:
            return None
        
        return min(sources, key=lambda s: s.distance_to(lat, lon))
    
    @classmethod
    def get_all_sources(cls) -> List['WaterSource']:
        """Get all water sources."""
        return cls._all_sources.copy()
    
    @classmethod
    def clear_all(cls):
        """Clear all sources (for testing)."""
        cls._all_sources.clear()
    
    def __repr__(self) -> str:
        return (f"WaterSource(name='{self.name}', "
                f"coords=({self.latitude}, {self.longitude}), "
                f"capacity='{self.capacity}')")
