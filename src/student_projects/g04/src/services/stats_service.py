from ..db import db
from ..models.card_record_model import CardRecord
from ..models.goal_record_model import GoalRecord
from ..stats.game_stats import GameStats
from ..stats.player_stats import PlayerStats
from ..stats.team_stats import TeamStats
from bson import ObjectId



def get_game_stats(game_id):
    game_oid = ObjectId(game_id)

    cards_cursor = db.cards.find({"game_id": game_oid})
    goals_cursor = db.goals.find({"game_id": game_oid})

    cards = [CardRecord.from_dict(c) for c in cards_cursor]
    goals = [GoalRecord.from_dict(g) for g in goals_cursor]

    player_ids = set()
    team_ids = set()

    for goal in goals:
        player_ids.add(ObjectId(goal.player_id))
        team_ids.add(ObjectId(goal.team_id))

    for card in cards:
        player_ids.add(ObjectId(card.player_id))

    players = {
        str(p["_id"]): p
        for p in db.players.find({"_id": {"$in": list(player_ids)}})
    }

    teams = {
        str(t["_id"]): t
        for t in db.teams.find({"_id": {"$in": list(team_ids)}})
    }

    for goal in goals:
        goal.player_name = players.get(goal.player_id, {}).get("name", "Unknown")
        goal.team_name = teams.get(goal.team_id, {}).get("name", "Unknown")

    for card in cards:
        card.player_name = players.get(card.player_id, {}).get("name", "Unknown")

    return GameStats(
        game_id=game_id,
        cards=cards,
        goals=goals
    )



def get_player_stats(player_id, competition_id=None):
    player_oid = ObjectId(player_id)

    cards_cursor = db.cards.find({"player_id": player_oid})
    goals_cursor = db.goals.find({"player_id": player_oid})

    cards = [CardRecord.from_dict(c) for c in cards_cursor]
    goals = [GoalRecord.from_dict(g) for g in goals_cursor]

    return PlayerStats(
        player_id=player_id,
        competition_id=competition_id,
        cards=cards,
        goals=goals
    )



def get_team_stats(team_id, competition_id):
    team_oid = ObjectId(team_id)
    comp_oid = ObjectId(competition_id)

    games_cursor = db.games.find({
        "$or": [{"team_1_id": team_oid}, {"team_2_id": team_oid}],
        "competition_id": comp_oid
    })

    
    wins = draws = losses = goals_for = goals_against = 0

    for game in games_cursor:
        team_score = 0
        opponent_score = 0

        goals_cursor = db.goals.find({"game_id": game["_id"]})
        for g in goals_cursor:
            if g["team_id"] == team_id:
                team_score += 1
            else:
                opponent_score += 1

        goals_for += team_score
        goals_against += opponent_score

        if team_score > opponent_score:
            wins += 1
        elif team_score == opponent_score:
            draws += 1
        else:
            losses += 1

    goal_difference = goals_for - goals_against
    points = wins * 3 + draws

    return TeamStats(
        team_id=team_id,
        competition_id=competition_id,
        wins=wins,
        draws=draws,
        losses=losses,
        goals_for=goals_for,
        goals_against=goals_against,
        goal_difference=goal_difference,
        points=points
    )

def get_competition_stats(competition_id):
    comp_oid = ObjectId(competition_id)

    games_cursor = db.games.find({"competition_id": comp_oid})
    games = list(games_cursor)

    total_goals = 0
    total_cards = 0
    game_stats_list = []

    for game in games:
        cards_cursor = db.cards.find({"game_id": game["_id"]})
        cards = [CardRecord.from_dict(c) for c in cards_cursor]
        total_cards += len(cards)

        goals_cursor = db.goals.find({"game_id": game["_id"]})
        goals = [GoalRecord.from_dict(g) for g in goals_cursor]
        total_goals += len(goals)

        game_stats_list.append({
            "game_id": str(game["_id"]),
            "cards": [c.to_dict() for c in cards],
            "goals": [g.to_dict() for g in goals],
        })

    return {
        "competition_id": competition_id,
        "games_count": len(games),
        "total_goals": total_goals,
        "total_cards": total_cards,
        "games": game_stats_list
    }
