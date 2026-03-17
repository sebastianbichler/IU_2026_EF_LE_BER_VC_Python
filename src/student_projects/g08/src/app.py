# Hauptanwendung für Bear Honeyworks, die die Streamlit-Oberfläche startet und die Umgebungsvariable für den Python-Pfad setzt, damit die Module korrekt gefunden werden können.
# Die main-Funktion führt die Streamlit-App aus und fängt KeyboardInterrupt ab, um eine saubere Beendigung zu ermöglichen.
# Wenn die App mit Strg+C beendet wird, wird eine Nachricht ausgegeben und die Anwendung mit einem Rückgabewert von 0 (erfolgreiche Beendigung) geschlossen.
# Die Anwendung wird gestartet, wenn dieses Skript direkt ausgeführt wird, indem die main-Funktion aufgerufen und ihr Rückgabewert als Systemexit-Code verwendet wird.
# Import der benötigten Module für die Ausführung der Streamlit-App und die Handhabung von Systembefehlen
# Die Anwendung setzt die Umgebungsvariable PYTHONPATH auf "src", damit die Module aus dem src-Ordner korrekt importiert werden können.
# Die Streamlit-App wird mit dem Befehl "honeyworks" gestartet, wobei das aktuelle Python-Interpreter verwendet wird.
import os
import subprocess
import sys


def main() -> int:
    os.environ["PYTHONPATH"] = "src"

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "src/bear_honeyworks/ui/app.py",
            ],
            check=False,
        )
        return result.returncode
    except KeyboardInterrupt:
        print("\nBear Honeyworks wurde beendet.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())