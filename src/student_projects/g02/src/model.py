from dataclasses import dataclass

@dataclass
class NutStash:
    id: int
    x: float
    y: float
    nut_type: str
    tree_type: str        
    amount: int
    depth: float
    expiration_date: str

    def __repr__(self):
        return (f"🌰 #{self.id}: {self.amount}x {self.nut_type} (Baum: {self.tree_type}) "
                f"bei ({self.x:.1f}/{self.y:.1f}) | "
                f"{self.depth:.1f}cm tief | Haltbar: {self.expiration_date}")