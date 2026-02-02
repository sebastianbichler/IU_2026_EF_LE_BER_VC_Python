"""
Herd model - represents a group of elephants.
Also creates circular references: Herd ↔ Elephants
"""

from typing import List, Set, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from models.elephant import Elephant


class Herd:
    """
    Represents a herd of elephants.
    
    CIRCULAR REFERENCE WARNING:
    - Herd contains elephants
    - Each elephant has a reference back to herd
    """
    
    _instance_count = 0
    
    def __init__(self, name: str, territory: str):
        """
        Args:
            name: Herd name
            territory: Geographic territory
        """
        self.name = name
        self.territory = territory
        self.members: List['Elephant'] = []
        self.established_year: int = date.today().year
        
        Herd._instance_count += 1
        self._id = Herd._instance_count
    
    def add_member(self, elephant: 'Elephant'):
        """
        Add an elephant to the herd.
        Creates circular reference: herd.members → elephant.herd → herd
        """
        if elephant not in self.members:
            self.members.append(elephant)
            elephant.herd = self  # CIRCULAR REFERENCE
    
    def remove_member(self, elephant: 'Elephant'):
        """Remove an elephant from the herd."""
        if elephant in self.members:
            self.members.remove(elephant)
            elephant.herd = None
    
    def get_matriarch(self) -> 'Elephant':
        """
        Get the oldest female elephant (matriarch).
        In real elephant herds, the oldest female leads.
        """
        females = [e for e in self.members if e.gender == 'F']
        if not females:
            return None
        return min(females, key=lambda e: e.birth_year)
    
    def get_family_count(self) -> int:
        """Count distinct family groups in the herd."""
        families = set()
        for elephant in self.members:
            # Trace back to root ancestor
            root = elephant
            while root.parent is not None:
                root = root.parent
            families.add(id(root))
        return len(families)
    
    def __repr__(self) -> str:
        return (f"Herd(name='{self.name}', territory='{self.territory}', "
                f"members={len(self.members)})")
    
    @classmethod
    def get_instance_count(cls) -> int:
        """Get number of herd instances created."""
        return cls._instance_count
