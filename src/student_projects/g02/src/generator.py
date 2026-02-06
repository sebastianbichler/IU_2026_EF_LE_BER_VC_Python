"""
Modul zur Generierung synthetischer Testdaten

Wissenschaftlicher Kontext:
Um die Skalierbarkeit von Algorithmen zu testen, werden große Mengen an Daten
benötigt, die manuell nicht erfasst werden können.
Dieses Modul simuliert den Prozess der Datenerfassung durch Zufallsgeneratoren.

Verantwortlichkeiten:
- Erzeugung valider `NutStash`-Objekte mit zufälligen Eigenschaften
- Simulation realistischer Wertebereiche
"""
import random
from datetime import datetime, timedelta
from .model import NutStash

def generate_dummy_data(count: int = 10) -> list[NutStash]:
    """
    Erzeugt eine Liste von zufälligen Verstecken (Stashes)

    Dient als Datenquelle für:
    1. Funktionale Tests (kleine Mengen, z.B. count=5)
    2. Performance-Benchmarks (große Mengen, z.B. count=10.000)

    Args:
        count (int): Die Anzahl der zu generierenden Datensätze. Standard ist 10

    Returns:
        list[NutStash]: Eine Liste mit instanziierten Datenobjekten
    """
    stashes = []
    # 1. Liste der Nüsse
    nut_types = ["Haselnuss", "Walnuss", "Eichel", "Erdnuss"]
    
    # 2. Liste der Baumarten
    tree_types = ["Eiche", "Kiefer", "Buche", "Trauerweide"]
    
    # Startdatum für Haltbarkeit
    today = datetime.now()

    for i in range(count):
        # Zufälliges Datum in der Zukunft (10 bis 365 Tage)
        days_future = random.randint(10, 365)
        exp_date = (today + timedelta(days=days_future)).strftime("%Y-%m-%d")

        stashes.append(NutStash(
            # ID wird später vom Manager überschrieben/verwaltet
            id=i + 1,

            # Geografische Verteilung (0-100m Feld)
            x=random.uniform(0.0, 100.0),
            y=random.uniform(0.0, 100.0),

            # Kategorien
            nut_type=random.choice(nut_types),
            tree_type=random.choice(tree_types),

            # Menge: Angepasst auf 50-300, um Überleben im Simulator realistisch zu machen
            amount=random.randint(5, 300),

            # Tiefe: 5.0cm bis 60.0cm 
            # Werte < 10.0cm gelten als "unsicher" 
            depth=random.uniform(5.0, 60.0),  

            expiration_date=exp_date
        ))
    return stashes