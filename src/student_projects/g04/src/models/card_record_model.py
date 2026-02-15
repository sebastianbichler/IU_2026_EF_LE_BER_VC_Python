from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar
from bson import ObjectId

from .entity_model import Entity
from src.enums import CardColor


T = TypeVar("T", bound="CardRecord")


class CardRecord(Entity):
    def __init__(
        self,
        game_id: str,
        player_id: str,
        color: CardColor,
        time: datetime,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.game_id: str = game_id
        self.player_id: str = player_id
        self.color: CardColor = color
        self.time: datetime = time

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(
            game_id=str(data.get("game_id")),
            player_id=str(data.get("player_id")),
            color=CardColor(data.get("color")),
            time=data.get("time"),
            id=str(data.get("_id")) if data.get("_id") else None,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def to_dict(self, for_db: bool = False) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "color": self.color.value,
            "time": self.time.isoformat() if self.time else None,
        }

        if for_db:
            data["game_id"] = ObjectId(self.game_id) if self.game_id else None
            data["player_id"] = ObjectId(self.player_id) if self.player_id else None
        else:
            data["game_id"] = self.game_id if self.game_id else None
            data["player_id"] = self.player_id if self.player_id else None

        data.update(super().to_dict(for_db=for_db))
        return data
