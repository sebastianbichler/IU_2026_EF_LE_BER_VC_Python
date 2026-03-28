from pathlib import Path

def ensure_parent(path: str):
    p = Path(path)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)