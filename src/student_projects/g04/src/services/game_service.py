from ..db.db import db
from ..models.game_model import Game, GameStatus

from bson.objectid import ObjectId


def get_games_by_competition_id(competition_id):
    raw_games = db.games.find({'competition_id': ObjectId(competition_id)})

    return [Game.from_dict(game) for game in raw_games]


def create_game(team_1_id, team_2_id, competition_id, score_1, score_2, start_date, end_date, status=GameStatus.SCHEDULED):
    game = Game(team_1_id=team_1_id, team_2_id=team_2_id, competition_id=competition_id,
                score_1=score_1, score_2=score_2, start_date=start_date, end_date=end_date, status=status)

    result = db.games.insert_one(game.to_dict(for_db=True))
    game.id = str(result.inserted_id)

    return game.to_dict()

def get_all_games():
    games = list(db.games.find())

    for g in games:
        team1 = db.teams.find_one({"_id": ObjectId(g["team_1_id"])})
        team2 = db.teams.find_one({"_id": ObjectId(g["team_2_id"])})

        g["team_1_name"] = team1["name"] if team1 else "Unknown"
        g["team_2_name"] = team2["name"] if team2 else "Unknown"

        g["id"] = str(g["_id"])

    return games

def get_games_by_ids(game_ids):
    object_ids = [ObjectId(game_id) for game_id in game_ids]
    raw_games = db.games.find({'_id': {'$in': object_ids}})

    return [Game.from_dict(game) for game in raw_games]
