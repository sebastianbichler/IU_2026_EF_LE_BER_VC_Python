from .entity_model import Entity
from enum import Enum
from bson import ObjectId

class GameStatus(Enum):
    SCHEDULED = 'Scheduled'
    ONGOING = 'Ongoing'
    FINISHED = 'Finished'

class Game(Entity):
    def __init__(self, team_1_id, team_2_id, competition_id, score_1, score_2, start_date, end_date, status, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self.team_1_id = team_1_id
        self.team_2_id = team_2_id
        self.competition_id = competition_id
        self.score_1 = score_1
        self.score_2 = score_2
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    @classmethod
    def from_dict(cls, data):
        # Converts MongoDB dictionary to Game object
        return cls(
            team_1_id=str(data.get('team_1_id')),
            team_2_id=str(data.get('team_2_id')),
            competition_id=str(data.get('competition_id')),
            score_1=data.get('score_1'),
            score_2=data.get('score_2'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            status=GameStatus(data.get('status')),
            id=str(data.get('_id')),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self, for_db=False):
        # Converts Game object to dictionary (for MongoDB if for_db=True)
        data = {
            'score_1': self.score_1,
            'score_2': self.score_2,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status.value,
        }

        if for_db:
            if self.team_1_id:
                data['team_1_id'] = ObjectId(self.team_1_id)
            if self.team_2_id:
                data['team_2_id'] = ObjectId(self.team_2_id)
            if self.competition_id:
                data['competition_id'] = ObjectId(self.competition_id)
        else:
            data['team_1_id'] = self.team_1_id if self.team_1_id else None
            data['team_2_id'] = self.team_2_id if self.team_2_id else None
            data['competition_id'] = self.competition_id if self.competition_id else None

        super_data = super().to_dict(for_db=for_db)
        data.update(super_data)

        return data
