from ..db import db
from ..models.competition_model import Competition

from bson.objectid import ObjectId


def get_competitions():
    raw_competitions = db.competitions.find()

    return [Competition.from_dict(competition).to_dict() for competition in raw_competitions]


def get_competition(competition_id):
    raw_competition = db.competitions.find_one(
        {'_id': ObjectId(competition_id)})
    if raw_competition:
        return Competition.from_dict(raw_competition).to_dict()

    return None


def get_scoreboard(competition_id):
    pipeline = [
        {'$match': {'competition_id': ObjectId(competition_id)}},

        {'$project': {
            'teams': [
                {
                    'team_id': '$team_1_id',
                    'goals_for': '$score_1',
                    'goals_against': '$score_2',
                    'is_win': {'$cond': [{'$gt': ['$score_1', '$score_2']}, 1, 0]},
                    'is_draw': {'$cond': [{'$eq': ['$score_1', '$score_2']}, 1, 0]},
                    'is_loss': {'$cond': [{'$lt': ['$score_1', '$score_2']}, 1, 0]}
                },
                {
                    'team_id': '$team_2_id',
                    'goals_for': '$score_2',
                    'goals_against': '$score_1',
                    'is_win': {'$cond': [{'$gt': ['$score_2', '$score_1']}, 1, 0]},
                    'is_draw': {'$cond': [{'$eq': ['$score_2', '$score_1']}, 1, 0]},
                    'is_loss': {'$cond': [{'$lt': ['$score_2', '$score_1']}, 1, 0]}
                }
            ]
        }},

        {'$unwind': '$teams'},

        {'$group': {
            '_id': '$teams.team_id',
            'P': {'$sum': 1},
            'W': {'$sum': '$teams.is_win'},
            'D': {'$sum': '$teams.is_draw'},
            'L': {'$sum': '$teams.is_loss'},
            'GF': {'$sum': '$teams.goals_for'},
            'GA': {'$sum': '$teams.goals_against'},
            'PTS': {'$sum': {
                '$add': [
                    {'$multiply': ['$teams.is_win', 3]},
                    {'$multiply': ['$teams.is_draw', 1]}
                ]
            }}
        }},

        {'$addFields': {
            'GD': {'$subtract': ['$GF', '$GA']}
        }},

        {'$sort': {'PTS': -1, 'GD': -1}}
    ]

    scoreboard_raw =  list(db.games.aggregate(pipeline))

    scoreboard = []
    for entry in scoreboard_raw:
        scoreboard.append(
            {
                'team_id': str(entry['_id']),
                'played': entry['P'],
                'won': entry['W'],
                'drawn': entry['D'],
                'lost': entry['L'],
                'goals_for': entry['GF'],
                'goals_against': entry['GA'],
                'goal_difference': entry['GD'],
                'points': entry['PTS']
            }
        )
        
    return scoreboard


def create_competition(name, description, logo, start_date, end_date):
    competition = Competition(name=name, description=description,
                              logo=logo, start_date=start_date, end_date=end_date)

    result = db.competitions.insert_one(competition.to_dict(for_db=True))
    competition.id = str(result.inserted_id)

    return competition.to_dict()
