from ..db import db

def get_all_players():
    players_cursor = db.players.find()
    players = list(players_cursor)

    default_comp = db.competitions.find_one()  # я тут беру рандомное соревнование, ибо нет связи
    default_comp_id = str(default_comp["_id"]) if default_comp else None

    for player in players:
        player["competition_id"] = default_comp_id

    return players