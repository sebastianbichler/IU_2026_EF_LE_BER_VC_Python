from typing import Dict
from bson import ObjectId
from pymongo.collection import Collection

from ..db.db import db
from ..models.player_model import Player, PlayerPosition

def get_all_players() -> list[Player]:
    players_cursor = db.players.find()
    
    return [Player.from_dict(player) for player in players_cursor]

def get_players(team_id: str) -> list[Player]:
    raw_players = db.players.find({'team_id': ObjectId(team_id)})

    return [Player.from_dict(player) for player in raw_players]


def get_player(player_id: str) -> Player | None:
    raw_player = db.players.find_one({'_id': ObjectId(player_id)})
    if raw_player:
        return Player.from_dict(raw_player)

    return None


def create_player(first_name: str, last_name: str, picture_url: str, position: PlayerPosition, shirt_number: int, team_id: str) -> Dict:
    player = Player(first_name=first_name, last_name=last_name, picture_url=picture_url, position=position, shirt_number=shirt_number, team_id=team_id)

    result = db.players.insert_one(player.to_doc())
    player.id = str(result.inserted_id)

    return player.to_dict()
