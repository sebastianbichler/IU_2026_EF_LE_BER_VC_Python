#!/usr/bin/env python3
"""
Einstieg der Web-Anwendung.
Startet den Server aus dem Projektverzeichnis.
"""
import os
import sys

_g03 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _g03)
sys.path.insert(0, os.path.join(_g03, "src"))

from src.web.app import app


def main():
    """Startet den Server."""
    app.run(debug=True, port=8081)


if __name__ == "__main__":
    main()
