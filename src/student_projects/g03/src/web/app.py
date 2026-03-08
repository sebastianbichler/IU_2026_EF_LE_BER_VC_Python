"""
RabbitFarm Web-App: Flask-Anwendung.
Nur App-Logik; Jupyter-Notebooks bleiben an ihrem ursprünglichen Ort.
"""
import os
import sys

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR = os.path.dirname(_THIS_DIR)
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from flask import Flask
from src.web.routes import bp

app = Flask(
    __name__,
    template_folder=os.path.join(_THIS_DIR, "templates"),
    static_folder=os.path.join(_THIS_DIR, "static"),
)
app.jinja_env.globals.update(enumerate=enumerate)
app.register_blueprint(bp)

import data_manager  # noqa: E402
data_manager.load_data()
