from typing import cast
from flask import g, current_app
from werkzeug.local import LocalProxy
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from ..models.player_model import PlayerDoc

class MyDatabase(Database):
    players: Collection[PlayerDoc]
    teams: Collection
    competitions: Collection
    games: Collection
    news: Collection
    goals: Collection
    cards: Collection

def get_db() -> MyDatabase:
    db = getattr(g, '_database', None)

    if db is None:
        uri = current_app.config.get('MONGO_URI')

        if not uri:
            raise RuntimeError('MONGO_URI is not set in app.config')

        client: MongoClient = MongoClient(uri)
        db = g._database = client.get_default_database()

    return cast(MyDatabase, db)


db: MyDatabase = LocalProxy(get_db) # type: ignore[assignment]
