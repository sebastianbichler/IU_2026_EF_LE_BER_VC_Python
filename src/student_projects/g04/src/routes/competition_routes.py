from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from ..services import game_service, team_service
from ..services import competition_service

# Web routes

competitions_web_bp = Blueprint('competitions_web', __name__)


@competitions_web_bp.route('/', methods=['GET'])
def index_action():
    competitions = competition_service.get_competitions()

    return render_template('competition/index.html', competitions=competitions)


@competitions_web_bp.route('/<competition_id>', methods=['GET'])
def details_action(competition_id):
    competition = competition_service.get_competition(competition_id)
    if not competition:
        return render_template('not-found.html'), 404

    games = game_service.get_games(competition_id)
    games = [game.to_dict() for game in games]

    scoreboard = competition_service.get_scoreboard(competition_id)

    teams = team_service.get_teams()
    teams = [team.to_dict() for team in teams]

    return render_template('competition/details.html', competition=competition, games=games, scoreboard=scoreboard, teams=teams)


# API endpoints

competitions_api_bp = Blueprint('competitions_api', __name__)


@competitions_api_bp.route('/add', methods=['GET', 'POST'])
def add_action():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    logo_url = data.get('logo_url')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    competition = competition_service.create_competition(
        name, description, logo_url, start_date, end_date)

    return jsonify(competition), 200
