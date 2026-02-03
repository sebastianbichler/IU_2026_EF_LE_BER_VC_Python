from flask import Blueprint, jsonify
from src.services.stats_service import get_game_stats
from flask import Blueprint, render_template
from src.services import game_service
stats_web_bp = Blueprint( "stats_web",__name__,url_prefix="/games")

@stats_web_bp.route("/", methods=["GET"])
def games_stats_index():
    games = game_service.get_all_games()

    return render_template(
        "game/index.html",
        games=games
    )

@stats_web_bp.route("/<game_id>/stats", methods=["GET"])
def index_action(game_id):
    stats = get_game_stats(game_id)

    if not stats:
        return render_template("not-found.html"), 404

    return render_template(
        "stats/game_stats.html",
        stats=stats
    )


stats_api_bp = Blueprint("stats_api", __name__, url_prefix="/api/stats")

@stats_api_bp.route("/game/<game_id>")
def api_game_stats(game_id):
    stats = get_game_stats(game_id)
    return jsonify(stats.to_dict())
