from datetime import datetime
from bson import ObjectId

from .entity_model import Entity

class GoalRecord(Entity):
    def __init__(self, game_id: str, player_id: str, team_id: str, time: datetime, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.game_id = game_id
        self.player_id = player_id
        self.team_id = team_id
        self.time = time

    @classmethod
    def from_dict(cls, data):
        time = data.get("time")
        if isinstance(time, str):
            time = datetime.fromisoformat(time.replace("Z", "+00:00"))
        return cls(
            game_id=str(data.get("game_id")),
            player_id=data.get("player_id"),
            team_id=str(data.get("team_id")),
            time=time,
            id=str(data.get("_id")),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def to_dict(self, for_db=False):
        data = {
            "time": self.time.isoformat() if self.time else None,
            "id": self.id
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