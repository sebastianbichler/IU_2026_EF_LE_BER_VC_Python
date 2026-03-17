# Import der benötigten Domänenklasse
from dataclasses import dataclass

# Die Klasse HoneyJar repräsentiert ein Honigglas mit spezifischen Eigenschaften.
@dataclass
class HoneyJar:
    weight: float  # in kg
    sort: str
    quality: int  # 1-5
    bear_name: str