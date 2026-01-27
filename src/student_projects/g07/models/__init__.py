"""
Core data models for Elephant Memory Cloud.
These models deliberately use circular references to demonstrate
Python's garbage collection mechanisms.
"""

from .elephant import Elephant
from .herd import Herd
from .event import Event
from .water_source import WaterSource

__all__ = ['Elephant', 'Herd', 'Event', 'WaterSource']
