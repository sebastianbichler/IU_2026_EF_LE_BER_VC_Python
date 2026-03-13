from dataclasses import dataclass
from src.student_projects.g05.src.models.recipe import Recipe


@dataclass
class MenuItem:
    name: str
    recipe: Recipe
    price: float
