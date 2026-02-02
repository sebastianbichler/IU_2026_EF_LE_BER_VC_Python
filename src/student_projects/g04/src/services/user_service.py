from ..db import db
from ..models.user_model import User


def get_all_users():
    raw_users = db.users.find()

    users = []
    for user in raw_users:
        user_obj = User.from_dict(user)

        # because user['_id'] is ObjectId, not string
        user_data = user_obj.to_dict()
        user_data['id'] = str(user['_id'])

        users.append(user_data)

    return users
