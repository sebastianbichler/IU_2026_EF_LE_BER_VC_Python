"""
Generate large-scale dummy data for memory/search testing.
Demonstrates circular references in complex relationship graphs.
"""

import random
from datetime import datetime
from typing import List, Tuple
from models.elephant import Elephant
from models.herd import Herd
from models.event import Event, EventType
from models.water_source import WaterSource


class DataGenerator:
    """Generate large datasets for testing memory management and search."""
    
    ELEPHANT_NAMES = [
        "Ella", "Emma", "Eric", "Elsa", "Emily", "Ethan", "Eva", 
        "Eddie", "Elena", "Eli", "Ember", "Enzo", "Eden", "Ezra",
        "Eleanor", "Emmett", "Evelyn", "Elliot", "Esther", "Everett"
    ]
    
    WATER_SOURCES_DATA = [
        ("Okavango River", -19.0, 22.5, "large"),
        ("Chobe Waterhole", -18.5, 24.0, "medium"),
        ("Savuti Marsh", -18.5, 24.1, "medium"),
        ("Linyanti Springs", -18.3, 23.8, "small"),
        ("Moremi Delta", -19.3, 23.0, "large"),
        ("Khwai Pools", -19.1, 23.8, "medium"),
        ("Makgadikgadi Pans", -20.5, 25.0, "small"),
        ("Nxai Pan", -20.1, 24.7, "small"),
        ("Boteti River", -20.3, 24.5, "large"),
        ("Zambezi Waters", -17.8, 25.3, "large")
    ]
    
    TERRITORIES = [
        "Northern Savanna", "Central Plains", "Southern Grasslands",
        "Eastern Woodlands", "Western Wetlands", "Delta Region",
        "Mountain Foothills", "Coastal Lowlands"
    ]
    
    @staticmethod
    def generate_herds(count: int = 10) -> List[Herd]:
        """
        Generate multiple herds.
        
        Args:
            count: Number of herds to generate
            
        Returns:
            List of Herd objects
        """
        herds = []
        for i in range(count):
            herd = Herd(
                name=f"Herd_{chr(65+i)}_{i+1}",  # Herd_A_1, Herd_B_2, etc.
                territory=random.choice(DataGenerator.TERRITORIES)
            )
            herds.append(herd)
        return herds
    
    @staticmethod
    def generate_family_tree(
        root_name: str = "Matriarch_Ella",
        generations: int = 5,
        children_per_elephant: int = 3,
        start_year: int = 1950
    ) -> Tuple[Elephant, List[Elephant]]:
        """
        Generate a large family tree with circular references.
        This creates the circular parent-child relationships that demonstrate
        Python's cyclic garbage collection.
        
        Args:
            root_name: Name of the matriarch
            generations: Number of generations to create
            children_per_elephant: Average children per elephant
            start_year: Birth year of matriarch
            
        Returns:
            Tuple of (root elephant, list of all elephants)
        """
        all_elephants = []
        
        def create_generation(parent: Elephant, current_gen: int, max_gen: int):
            """Recursively create generations with circular references."""
            if current_gen >= max_gen:
                return
            
            num_children = random.randint(1, children_per_elephant + 1)
            birth_year = start_year + (current_gen * 15)
            
            for i in range(num_children):
                name = f"{random.choice(DataGenerator.ELEPHANT_NAMES)}_G{current_gen}_{random.randint(100,999)}"
                gender = random.choice(['M', 'F'])
                
                child = Elephant(name, birth_year, gender)
                parent.add_child(child)  # Creates circular reference: parent → child, child → parent
                all_elephants.append(child)
                
                # Recursively create next generation
                create_generation(child, current_gen + 1, max_gen)
        
        # Create matriarch
        matriarch = Elephant(root_name, start_year, "F")
        all_elephants.append(matriarch)
        
        # Generate family tree
        create_generation(matriarch, 1, generations)
        
        return matriarch, all_elephants
    
    @staticmethod
    def generate_multiple_families(
        num_families: int = 5,
        generations: int = 4,
        children_per_elephant: int = 3
    ) -> List[Elephant]:
        """
        Generate multiple independent family trees.
        
        Args:
            num_families: Number of independent families
            generations: Generations per family
            children_per_elephant: Average children
            
        Returns:
            List of all elephants from all families
        """
        all_elephants = []
        
        for i in range(num_families):
            start_year = random.randint(1940, 1980)
            root_name = f"Matriarch_{random.choice(DataGenerator.ELEPHANT_NAMES)}_{i+1}"
            
            _, family_elephants = DataGenerator.generate_family_tree(
                root_name=root_name,
                generations=generations,
                children_per_elephant=children_per_elephant,
                start_year=start_year
            )
            
            all_elephants.extend(family_elephants)
        
        return all_elephants
    
    @staticmethod
    def generate_water_sources() -> List[WaterSource]:
        """
        Generate water sources with historical availability data.
        
        Returns:
            List of WaterSource objects
        """
        sources = []
        
        for name, lat, lon, capacity in DataGenerator.WATER_SOURCES_DATA:
            source = WaterSource(name, lat, lon, capacity)
            
            # Add historical availability (simulate droughts)
            for year in range(2000, 2026):
                # 20% chance of drought, higher in certain years
                drought_probability = 0.2
                if year in [2005, 2012, 2019]:  # Historical drought years
                    drought_probability = 0.6
                
                available = random.random() > drought_probability
                source.record_availability(year, available)
            
            sources.append(source)
        
        return sources
    
    @staticmethod
    def generate_events(
        elephants: List[Elephant],
        herds: List[Herd],
        count: int = 500
    ) -> List[Event]:
        """
        Generate historical events linking elephants and herds.
        
        Args:
            elephants: List of available elephants
            herds: List of available herds
            count: Number of events to generate
            
        Returns:
            List of Event objects
        """
        events = []
        
        if not elephants or not herds:
            return events
        
        for i in range(count):
            event_type = random.choice(list(EventType))
            year = random.randint(2000, 2025)
            
            # Generate random location in southern Africa
            lat = round(random.uniform(-20.5, -17.5), 2)
            lon = round(random.uniform(22.0, 25.5), 2)
            location = f"{lat}, {lon}"
            
            # Randomly select involved elephants and herds
            num_elephants = min(random.randint(1, 8), len(elephants))
            num_herds = min(random.randint(1, 3), len(herds))
            
            involved = random.sample(elephants, num_elephants)
            involved_herds = random.sample(herds, num_herds)
            
            description = f"{event_type.value} at {location} in {year}"
            
            event = Event(
                event_type=event_type,
                year=year,
                location=location,
                description=description,
                involved_elephants=involved,
                involved_herds=involved_herds
            )
            
            events.append(event)
        
        return events
    
    @staticmethod
    def assign_elephants_to_herds(elephants: List[Elephant], herds: List[Herd]):
        """
        Distribute elephants across herds, creating more circular references.
        
        Args:
            elephants: List of elephants
            herds: List of herds
        """
        if not elephants or not herds:
            return
        
        for elephant in elephants:
            # Assign to random herd
            herd = random.choice(herds)
            herd.add_member(elephant)
