import os
from flask import g, current_app
from werkzeug.local import LocalProxy
from pymongo import MongoClient


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        uri = current_app.config.get('MONGO_URI')

        print(uri)

        if not uri:
            raise RuntimeError('MONGO_URI is not set in app.config')

        client = MongoClient(uri)
        db = g._database = client.get_default_database()

    return db


db = LocalProxy(get_db)
