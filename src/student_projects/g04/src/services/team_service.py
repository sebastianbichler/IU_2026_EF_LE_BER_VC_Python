from ..db import db
from ..models.team_model import Team

from bson import ObjectId


def get_teams():
    raw_teams = db.teams.find()

    return [Team.from_dict(team) for team in raw_teams]

def get_teams_by_ids(team_ids):
    object_ids = [ObjectId(team_id) for team_id in team_ids]
    raw_teams = db.teams.find({'_id': {'$in': object_ids}})

    return [Team.from_dict(team) for team in raw_teams]


def get_team(team_id):
    raw_team = db.teams.find_one({'_id': ObjectId(team_id)})
    if raw_team:
        return Team.from_dict(raw_team).to_dict()

    return None


def create_team(name, logo_url):
    team = Team(name=name, logo_url=logo_url)

    result = db.teams.insert_one(team.to_dict(for_db=True))
    team.id = str(result.inserted_id)

    return team.to_dict()
