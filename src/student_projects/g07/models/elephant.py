"""
Elephant model with circular references for family relationships.
This demonstrates Python's cyclic garbage collection.
"""

from typing import Optional, List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from models.herd import Herd


class Elephant:
    """
    Represents an elephant with family relationships.
    
    CIRCULAR REFERENCE WARNING:
    - parent/children create bidirectional references
    - Python's cyclic GC handles cleanup automatically
    """
    
    _instances: Set[int] = set()
    _instance_count = 0
    
    def __init__(self, name: str, birth_year: int, gender: str):
        """
        Args:
            name: Elephant's name
            birth_year: Year of birth
            gender: 'M' or 'F'
        """
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self._parent: Optional['Elephant'] = None
        self.children: List['Elephant'] = []
        self.herd: Optional['Herd'] = None
        
        Elephant._instance_count += 1
        Elephant._instances.add(id(self))
        self._id = Elephant._instance_count
    
    @property
    def parent(self) -> Optional['Elephant']:
        """Get parent elephant."""
        return self._parent
    
    @parent.setter
    def parent(self, value: Optional['Elephant']):
        """Set parent, creating circular reference."""
        self._parent = value
        if value is not None and self not in value.children:
            value.children.append(self)
    
    def add_child(self, child: 'Elephant'):
        """Add a child, creating bidirectional relationship."""
        if child not in self.children:
            self.children.append(child)
            child.parent = self
    
    def get_siblings(self) -> List['Elephant']:
        """Get all siblings (same parent)."""
        if self.parent is None:
            return []
        return [child for child in self.parent.children if child != self]
    
    def get_descendants(self, max_depth: int = 10) -> List['Elephant']:
        """Recursively get all descendants."""
        descendants = []
        visited = set()
        
        def _traverse(elephant: 'Elephant', depth: int):
            if depth > max_depth or id(elephant) in visited:
                return
            visited.add(id(elephant))
            for child in elephant.children:
                descendants.append(child)
                _traverse(child, depth + 1)
        
        _traverse(self, 0)
        return descendants
    
    def age_in_year(self, year: int) -> int:
        """Calculate age in a given year."""
        return year - self.birth_year
    
    def __repr__(self) -> str:
        parent_name = self.parent.name if self.parent else "None"
        return (f"Elephant(name='{self.name}', birth={self.birth_year}, "
                f"parent={parent_name}, children={len(self.children)})")
    
    def __del__(self):
        """Track when instances are garbage collected."""
        Elephant._instances.discard(id(self))
    
    @classmethod
    def get_instance_count(cls) -> int:
        """Get number of living instances."""
        return len(cls._instances)
    
    @classmethod
    def reset_tracking(cls):
        """Reset tracking."""
        cls._instances.clear()
        cls._instance_count = 0
