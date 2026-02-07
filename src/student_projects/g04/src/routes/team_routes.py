from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from ..services import player_service
from ..services import team_service

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


# API endpoints

teams_api_bp = Blueprint('teams_api', __name__)


@teams_api_bp.route('/add', methods=['POST'])
def add_team():
    data = request.get_json()

    name = data.get('name')
    logo_url = data.get('logo_url')

    team = team_service.create_team(name, logo_url)
    return jsonify(team), 200
