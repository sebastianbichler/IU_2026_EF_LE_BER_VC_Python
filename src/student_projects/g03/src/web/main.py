#!/usr/bin/env python3
"""
Einstiegspunkt für die RabbitFarm-Webapp.
Starten von Projektroot (g03):  python -m src.web.main
"""
import os
import sys

_g03 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _g03)
sys.path.insert(0, os.path.join(_g03, "src"))

from src.web.app import app


def main():
    app.run(debug=True, port=8081)


if __name__ == "__main__":
    main()
