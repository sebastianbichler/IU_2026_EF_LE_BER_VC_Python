from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from ..services import competition_service
from ..services import game_service
from ..models.game_model import GameStatus

# Web routes

games_web_bp = Blueprint('games_web', __name__)


@games_web_bp.route('/', methods=['GET'])
def index_action(competition_id):
    competition = competition_service.get_competition(competition_id)
    if not competition:
        return render_template('not-found.html'), 404

    games = game_service.get_games(competition_id)

    return render_template('game/index.html', games=games)


# API endpoints

games_api_bp = Blueprint('games_api', __name__)


@games_api_bp.route('/add', methods=['POST'])
def add_action(competition_id):
    data = request.get_json()

    team_1_id = data.get('team_1_id')
    team_2_id = data.get('team_2_id')
    score_1 = data.get('score_1')
    score_2 = data.get('score_2')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    status = data.get('status')
    game_status = GameStatus(
        status) if status in GameStatus._value2member_map_ else GameStatus.SCHEDULED

    competition = competition_service.get_competition(competition_id)
    if not competition:
        return jsonify({"message": "Competition not found"}), 404

    game = game_service.create_game(
        team_1_id, team_2_id, competition_id, score_1, score_2, start_date, end_date, status=game_status)

    return jsonify(game), 200
