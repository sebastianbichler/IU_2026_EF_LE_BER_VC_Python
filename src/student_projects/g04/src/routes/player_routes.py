from flask import Blueprint, jsonify, render_template, request
from collections import defaultdict
from datetime import datetime

from ..models.player_model import PlayerPosition
from ..services import player_service
from ..services import stats_service
from ..services import game_service
from ..services import team_service

# Web routes

players_web_bp = Blueprint('players_web', __name__)


@players_web_bp.route('/<player_id>', methods=['GET'])
def player_details(team_id, player_id):
    player = player_service.get_player(player_id)
    if not player:
        return render_template('not-found.html'), 404
    
    player_dict = player.to_dict()

    player_stats = stats_service.get_player_stats(player_id)

    # Getting all games player played
    game_ids = set()

    for card in player_stats.cards:
        game_ids.add(card.game_id)

    for goal in player_stats.goals:
        game_ids.add(goal.game_id)

    games = game_service.get_games_by_ids(list(game_ids))

    # Getting all teams of played games
    teams_ids = set()

    for game in games:
        teams_ids.add(game.team_1_id)
        teams_ids.add(game.team_2_id)

    teams = team_service.get_teams_by_ids(list(teams_ids))

    # Getting player's team info
    player_team = next((team for team in teams if team.id == player.team_id), None)

    player_dict['team_name'] = player_team.name if player_team else "Unknown Team"
    player_dict['team_logo_url'] = player_team.logo_url if player_team else None

    # Building games info with player's stats in each game
    player_games = []

    for game in games:
        game_dict = game.to_dict()

        team_against_id = game.team_2_id if game.team_1_id == player.team_id else game.team_1_id
        team_against = next((team for team in teams if team.id == team_against_id), None)

        game_dict['team_against_name'] = team_against.name if team_against else "Unknown Team"
        game_dict['team_against_logo_url'] = team_against.logo_url if team_against else None

        cards_in_game = [card.to_dict() for card in player_stats.cards if card.game_id == game.id]
        goals_in_game = [goal.to_dict() for goal in player_stats.goals if goal.game_id == game.id]

        for card in cards_in_game:
            card['in_game_time'] = round((datetime.strptime(card['time'], '%Y-%m-%dT%H:%M:%S') - game.start_date).total_seconds() // 60)

        for goal in goals_in_game:
            goal['in_game_time'] = round((datetime.strptime(goal['time'], '%Y-%m-%dT%H:%M:%S') - game.start_date).total_seconds() // 60)

        game_dict['cards'] = cards_in_game
        game_dict['goals'] = goals_in_game

        player_games.append(game_dict)

    player_dict['games'] = player_games

    return render_template('player/details.html', player=player_dict)

# API endpoints

players_api_bp = Blueprint('players_api', __name__)

@players_api_bp.route('/add', methods=['POST'])
def add_player(team_id):
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    picture_url = data.get('picture_url')
    shirt_number = data.get('shirt_number')

    position = data.get('position')
    player_position = PlayerPosition(position) if position in PlayerPosition._value2member_map_ else PlayerPosition.DEFENDER

    player = player_service.create_player(first_name, last_name, picture_url, player_position, shirt_number, team_id)
    return jsonify(player), 200