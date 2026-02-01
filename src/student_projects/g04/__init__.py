import os

from dotenv import load_dotenv
from flask import Flask

from .routes.user_routes import user_bp
from .routes.main_routes import main_bp
from .routes.news_routes import news_bp


def create_app():
    app = Flask(__name__)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    load_dotenv()
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(main_bp) 
    app.register_blueprint(news_bp)

    return app
