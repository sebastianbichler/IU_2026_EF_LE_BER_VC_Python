from dataclasses import dataclass

@dataclass
class NutStash:
    """Requirement F01: Datenmodell"""
    id: int
    x: float
    y: float
    nut_type: str
    amount: int

    def __repr__(self):
        return f"Versteck #{self.id}: {self.amount}x {self.nut_type} bei ({self.x:.1f}/{self.y:.1f})"