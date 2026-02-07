from ..db import db
from ..models.player_model import Player

from bson import ObjectId


def get_players(team_id):
    raw_players = db.players.find({'team_id': ObjectId(team_id)})

    return [Player.from_dict(player) for player in raw_players]


def get_player(player_id):
    raw_player = db.players.find_one({'_id': ObjectId(player_id)})
    if raw_player:
        return Player.from_dict(raw_player)

    return None


def create_player(first_name, last_name, picture_url, position, shirt_number, team_id):
    player = Player(first_name=first_name, last_name=last_name, picture_url=picture_url, position=position, shirt_number=shirt_number, team_id=team_id)

    result = db.players.insert_one(player.to_dict(for_db=True))
    player.id = str(result.inserted_id)

    return player.to_dict()
