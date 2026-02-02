from ..db import db
from ..models.game_model import Game, GameStatus

from bson.objectid import ObjectId


def get_games(competition_id):
    raw_games = db.games.find({'competition_id': ObjectId(competition_id)})

    return [Game.from_dict(game) for game in raw_games]


def create_game(team_1_id, team_2_id, competition_id, score_1, score_2, start_date, end_date, status=GameStatus.SCHEDULED):
    game = Game(team_1_id=team_1_id, team_2_id=team_2_id, competition_id=competition_id,
                score_1=score_1, score_2=score_2, start_date=start_date, end_date=end_date, status=status)

    result = db.games.insert_one(game.to_dict(for_db=True))
    game.id = str(result.inserted_id)

    return game.to_dict()
