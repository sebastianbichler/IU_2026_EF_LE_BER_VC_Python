from dataclasses import dataclass
from src.student_projects.g05.src.models.fish import Fish


@dataclass
class Recipe:
    name: str
    fish: Fish
    fish_required_kg: float

    def required_fish_kg(self, quantity: int) -> float:
        return self.fish_required_kg * quantity
