from datetime import datetime
from flask import Blueprint, jsonify, redirect, render_template, request, url_for


from ..services import player_service
from ..services import team_service
from ..services import game_service
from ..services import stats_service

# Web routes

teams_web_bp = Blueprint('teams_web', __name__)


@teams_web_bp.route('/', methods=['GET'])
def get_teams():
    teams = team_service.get_teams()

    return render_template('team/index.html', teams=teams)


@teams_web_bp.route('/<team_id>', methods=['GET'])
def team_details(team_id):
    team = team_service.get_team(team_id)
    if not team:
        return render_template('not-found.html'), 404
    
    players = player_service.get_players(team_id)
    players = [player.to_dict() for player in players]

    return render_template('team/details.html', team=team, players=players)

@teams_web_bp.route('/<team_id>/players/<player_id>', methods=['GET'])
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

    return render_template('team/player_details.html', player=player_dict)


# API endpoints

teams_api_bp = Blueprint('teams_api', __name__)


@teams_api_bp.route('/add', methods=['POST'])
def add_team():
    data = request.get_json()

    name = data.get('name')
    logo_url = data.get('logo_url')

    team = team_service.create_team(name, logo_url)
    return jsonify(team), 200
