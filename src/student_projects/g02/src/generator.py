import random
from datetime import datetime, timedelta
from .model import NutStash

def generate_dummy_data(count: int = 10) -> list[NutStash]:
    
    stashes = []
    # 1. Liste der Nüsse
    nut_types = ["Haselnuss", "Walnuss", "Eichel", "Erdnuss"]
    
    # 2. Liste der 4 Baumarten
    tree_types = ["Eiche", "Kiefer", "Buche", "Trauerweide"]
    
    # Startdatum für Haltbarkeit (heute)
    today = datetime.now()

    for i in range(count):
        # Zufälliges Datum in der Zukunft (10 bis 365 Tage)
        days_future = random.randint(10, 365)
        exp_date = (today + timedelta(days=days_future)).strftime("%Y-%m-%d")

        stashes.append(NutStash(
            id=i + 1,
            x=random.uniform(0.0, 100.0),
            y=random.uniform(0.0, 100.0),
            nut_type=random.choice(nut_types),
            tree_type=random.choice(tree_types),
            amount=random.randint(5, 300),
            depth=random.uniform(5.0, 60.0),  
            expiration_date=exp_date
        ))
    return stashes