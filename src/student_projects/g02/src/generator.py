import random
from .model import NutStash  # <-- Der Punkt ist wichtig!

def generate_dummy_data(count: int = 10) -> list[NutStash]:
    """Requirement F02: Generator"""
    stashes = []
    nut_types = ["Haselnuss", "Walnuss", "Eichel"]
    
    for i in range(count):
        stashes.append(NutStash(
            id=i + 1,
            x=random.uniform(0.0, 100.0),
            y=random.uniform(0.0, 100.0),
            nut_type=random.choice(nut_types),
            amount=random.randint(5, 50)
        ))
    return stashes