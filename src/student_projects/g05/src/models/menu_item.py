from dataclasses import dataclass
from src.student_projects.g05.src.models.fish import Fish


@dataclass
class MenuItem:
    name: str
    fish: Fish
    price: float
    fish_required_kg: float
