from __future__ import annotations

import random
from typing import Dict, List, Tuple


class AnimalLocation:
    def __init__(self, node_id: int, name: str, animal_type: str, description: str) -> None:
        self.node_id = node_id
        self.name = name
        self.animal_type = animal_type
        self.description = description

    def __repr__(self) -> str:
        return f"{self.name} ({self.animal_type})"


POSTAMT_NODE_ID = 0


FIXED_LOCATIONS: Dict[int, AnimalLocation] = {
    0: AnimalLocation(0, "Fuchs Postamt", "Fuchs", "Das Hauptpostamt des Fuchses - Startpunkt aller Lieferungen"),
    1: AnimalLocation(1, "Biberdamm", "Biber", "Die Wohnstatt am großen Fluss"),
    2: AnimalLocation(2, "Dachshöhle", "Dachs", "Die gemütliche Höhle unter der Eiche"),
    3: AnimalLocation(3, "Igelhecke", "Igel", "Dickicht hinter dem Garten"),
    4: AnimalLocation(4, "Froschteich", "Frosch", "Der sonnige Teich mit Seerosen"),
    5: AnimalLocation(5, "Kaninchenbau", "Kaninchen", "Die unterirdische WG"),
    6: AnimalLocation(6, "Vogelnest", "Vogel", "Hoher Baum am Waldrand"),
    7: AnimalLocation(7, "Mäuseloch", "Maus", "Kleines Loch unterm Zaun"),
    8: AnimalLocation(8, "Fischerranch", "Fisch", "Am Ufer des großen Sees"),
    9: AnimalLocation(9, "Schildkrötenstrand", "Schildkröte", "Warme Sandbank"),
    10: AnimalLocation(10, "Eichhörnchenkobel", "Eichhörnchen", "Baumkrone mit Nüssen"),
    11: AnimalLocation(11, "Wespennest", "Wespe", "Unter dem Dach"),
    12: AnimalLocation(12, "Bienenstock", "Biene", "Blumenwiese"),
    13: AnimalLocation(13, "Rehgatter", "Reh", "Lichtung im Wald"),
    14: AnimalLocation(14, "Fuchsbau", "Fuchs", "Der alternative Fuchs-Bau"),
    15: AnimalLocation(15, "Hasenfeld", "Hase", "Wiese hinter dem Hügel"),
    16: AnimalLocation(16, "Schweinestall", "Schwein", "Der gemütliche Stall"),
    17: AnimalLocation(17, "Kuhwiese", "Kuh", "Grüne Weide"),
    18: AnimalLocation(18, "Schafspferch", "Schaf", "Hügelige Wiese"),
    19: AnimalLocation(19, "Ziegenfelsen", "Ziege", "Steiniger Hang"),
}


ANIMAL_TYPES = [
    "Fuchs", "Biber", "Dachs", "Igel", "Frosch", "Kaninchen", "Vogel", "Maus", "Fisch",
    "Schildkröte", "Eichhörnchen", "Wespe", "Biene", "Reh", "Hase", "Schwein", "Kuh",
    "Schaf", "Ziege", "Elch", "Hirsch", "Wildschwein", "Fischotter", "Marder", "Wiesel",
    "Hermelin", "Hamster", "Ratte", "Eidechse", "Schlange", "Molch", "Salamander",
    "Krähe", "Rabe", "Falke", "Habicht", "Uhu", "Eule", "Fledermaus", "Dachs",
]

LOCATION_SUFFIXES = [
    "Wald", "Wiese", "Berg", "Tal", "Hain", "Höhle", "Bau", "Nest", "Teich", "See",
    "Fluss", "Bach", "Lichtung", "Dickicht", "Hecke", "Feld", "Garten", "Schlucht",
    "Klamm", "Kuppe", "Grat", "Hang", "Stein", "Felsen", "Morast", "Sumpf",
]


def _generate_location_name(node_id: int, seed: int) -> str:
    rng = random.Random(seed + node_id)
    animal = rng.choice(ANIMAL_TYPES)
    suffix = rng.choice(LOCATION_SUFFIXES)
    return f"{animal}-{suffix}"


def get_location_name(node_id: int, seed: int = 42) -> str:
    if node_id in FIXED_LOCATIONS:
        return FIXED_LOCATIONS[node_id].name
    return _generate_location_name(node_id, seed)


def get_location(node_id: int, seed: int = 42) -> AnimalLocation:
    if node_id in FIXED_LOCATIONS:
        return FIXED_LOCATIONS[node_id]
    name = _generate_location_name(node_id, seed)
    rng = random.Random(seed + node_id)
    animal = rng.choice(ANIMAL_TYPES)
    return AnimalLocation(node_id, name, animal, f"Generierter Ort #{node_id}")


def get_location_options(max_nodes: int = 250) -> List[Tuple[int, str]]:
    options = []
    for node_id in range(1, max_nodes):
        loc = get_location(node_id)
        options.append((node_id, f"{loc.name} ({loc.animal_type})"))
    return options


def get_all_locations(max_nodes: int = 250, seed: int = 42) -> List[AnimalLocation]:
    locations = []
    for node_id in range(max_nodes):
        locations.append(get_location(node_id, seed))
    return locations
