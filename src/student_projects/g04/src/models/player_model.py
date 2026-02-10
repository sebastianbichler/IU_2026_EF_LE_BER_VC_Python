from datetime import datetime
from enum import Enum
from typing import Any, Dict, cast
from bson import ObjectId

from ..db.general_document import GeneralDoc
from .entity_model import Entity


class PlayerPosition(Enum):
    GOALKEEPER = 'Goalkeeper'
    DEFENDER = 'Defender'
    MIDFIELDER = 'Midfielder'
    FORWARD = 'Forward'


class PlayerDoc(GeneralDoc):
    first_name: str
    last_name: str
    picture_url: str
    position: str
    shirt_number: int
    team_id: ObjectId

class Player(Entity):
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 picture_url: str,
                 position: PlayerPosition,
                 shirt_number: int,
                 team_id: str,
                 id: str | None = None,
                 created_at: datetime | None = None,
                 updated_at: datetime | None = None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.first_name = first_name
        self.last_name = last_name
        self.picture_url = picture_url
        self.position = position
        self.shirt_number = shirt_number
        self.team_id = team_id

    @classmethod
    def from_dict(cls, data: PlayerDoc) -> Player:
        # Converts MongoDB dictionary to Player object
        return cls(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            picture_url=data.get('picture_url', ''),
            position=PlayerPosition(data.get('position', PlayerPosition.FORWARD.value)),
            shirt_number=data.get('shirt_number', 0),
            team_id=str(data.get('team_id', '')),
            id=str(data.get('_id')),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self, for_db: bool = False) -> Dict[str, Any]:
        # Converts Player object to dictionary (for MongoDB if for_db=True)
        data: Dict[str, Any] = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'picture_url': self.picture_url,
            'position': self.position.value,
            'shirt_number': self.shirt_number,
            'team_id': self.team_id,
        }

        if for_db:
            data['team_id'] = ObjectId(self.team_id) if self.team_id else None
        else:
            data['team_id'] = self.team_id if self.team_id else None

        super_data = super().to_dict(for_db=for_db)
        data.update(super_data)

        return data
        
    def to_doc(self) -> PlayerDoc:
        return cast(PlayerDoc, self.to_dict(for_db=True))
