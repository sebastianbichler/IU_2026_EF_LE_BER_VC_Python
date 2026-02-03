from flask import Blueprint, jsonify
from src.services.stats_service import get_game_stats

stats_api_bp = Blueprint("stats_api", __name__, url_prefix="/api/stats")

@stats_api_bp.route("/game/<game_id>")
def api_game_stats(game_id):
    stats = get_game_stats(game_id)
    return jsonify(stats.to_dict())
