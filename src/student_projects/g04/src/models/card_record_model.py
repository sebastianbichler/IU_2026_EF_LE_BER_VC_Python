from datetime import datetime
from .entity_model import Entity
from src.enums import CardColor

class CardRecord(Entity):
     def __init__(
        self,
        game_id: str,
        player_id: str,
        color: CardColor,
        time: datetime,
        id=None,
        created_at=None,
        updated_at=None
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.game_id = game_id
        self.player_id = player_id
        self.color = color
        self.time = time
     
        @classmethod
        def from_dict(cls, data):
            return cls(
                game_id=data.get("game_id"),
                player_id=data.get("player_id"),
                color=CardColor(data.get("color")),
                time=data.get("time"),
                id=str(data.get("_id")),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at")
            )
        
        
        def to_dict(self, for_db=False):
            data = {
                "game_id": str(self.game_id),
                "player_id": self.player_id,
                "color": self.color,
                "time": self.time.isoformat() if self.time else None,
            }
            data.update(super().to_dict(for_db=for_db))
            return data

