# Test, der absichtlich keinen Fehler enthält, um die Funktionsweise von Mypy zu demonstrieren. In diesem Fall wird eine Funktion definiert, die ein HoneyJar-Objekt zurückgibt, was mit den Typannotationen übereinstimmt und somit keinen Fehler verursacht.
from bear_honeyworks.domain.honey import HoneyJar


def build_honeyjar() -> HoneyJar:
    return HoneyJar(
        weight=0.5,
        sort="Waldhonig",
        quality=5,
        bear_name="Balou",
    )