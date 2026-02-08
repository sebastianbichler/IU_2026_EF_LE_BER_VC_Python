from flask import Blueprint, render_template, request, jsonify

from ..models.player_model import PlayerPosition
from ..services import player_service
from ..services import stats_service

players_web_bp = Blueprint("players_web", __name__, url_prefix="/players")


@players_web_bp.route("/", methods=["GET"])
def players_stats_index():
    players = player_service.get_all_players()

    return render_template(
        "players/index.html",
        players=players
    )


@players_web_bp.route("/<player_id>/competition/<competition_id>/stats")
def player_stats(player_id, competition_id):
    stats = stats_service.get_player_stats_by_competition(player_id, competition_id)
    if not stats:
        return render_template("not-found.html"), 404
    return render_template(
        "stats/player_stats.html",
        stats=stats  
    )

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