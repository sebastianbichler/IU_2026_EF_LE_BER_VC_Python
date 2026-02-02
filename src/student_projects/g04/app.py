import os

from dotenv import load_dotenv
from flask import Flask

from src.routes.main_routes import main_bp
from src.routes.news_routes import news_bp
from src.routes.team_routes import teams_web_bp, teams_api_bp
from src.routes.competition_routes import competitions_web_bp, competitions_api_bp
from src.routes.game_routes import games_web_bp, games_api_bp


def create_app():
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    load_dotenv()
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    app.register_blueprint(main_bp) 
    app.register_blueprint(news_bp)
    
    app.register_blueprint(teams_web_bp, url_prefix='/teams')
    app.register_blueprint(teams_api_bp, url_prefix='/api/teams')

    app.register_blueprint(competitions_web_bp, url_prefix='/competitions')
    app.register_blueprint(competitions_api_bp, url_prefix='/api/competitions')

    app.register_blueprint(games_web_bp, url_prefix='/competitions/<competition_id>/games')
    app.register_blueprint(games_api_bp, url_prefix='/api/competitions/<competition_id>/games')

    return app
