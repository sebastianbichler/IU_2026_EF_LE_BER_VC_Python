from flask import Blueprint
from src.services.stats_service import get_player_stats
from flask import Blueprint, render_template
from ..services import player_service

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
    stats = get_player_stats(player_id, competition_id)
    if not stats:
        return render_template("not-found.html"), 404
    return render_template(
        "stats/player_stats.html",
        stats=stats  
    )