from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar
from bson import ObjectId

from .entity_model import Entity


T = TypeVar("T", bound="GoalRecord")


class GoalRecord(Entity):
    def __init__(
        self,
        game_id: str,
        player_id: str,
        team_id: str,
        time: datetime,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.game_id: str = game_id
        self.player_id: str = player_id
        self.team_id: str = team_id
        self.time: datetime = time

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        raw_time = data.get("time")

        parsed_time: Optional[datetime]
        if isinstance(raw_time, str):
            parsed_time = datetime.fromisoformat(
                raw_time.replace("Z", "+00:00")
            )
        else:
            parsed_time = raw_time

        return cls(
            game_id=str(data.get("game_id")),
            player_id=str(data.get("player_id")),
            team_id=str(data.get("team_id")),
            time=parsed_time if parsed_time else datetime.now(),  
            id=str(data.get("_id")) if data.get("_id") else None,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def to_dict(self, for_db: bool = False) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "time": self.time.isoformat() if self.time else None,
            "id": self.id,
        }

        if for_db:
            data["game_id"] = ObjectId(self.game_id) if self.game_id else None
            data["player_id"] = ObjectId(self.player_id) if self.player_id else None
            data["team_id"] = ObjectId(self.team_id) if self.team_id else None
        else:
            data["game_id"] = self.game_id if self.game_id else None
            data["player_id"] = self.player_id if self.player_id else None
            data["team_id"] = self.team_id if self.team_id else None

        data.update(super().to_dict(for_db=for_db))
        return data
