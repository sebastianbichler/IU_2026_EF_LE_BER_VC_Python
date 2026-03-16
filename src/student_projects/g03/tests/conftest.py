"""Pytest configuration: add src/ to sys.path so bare imports work."""

import os
import sys

_g03_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_src_dir = os.path.join(_g03_root, "src")
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)
