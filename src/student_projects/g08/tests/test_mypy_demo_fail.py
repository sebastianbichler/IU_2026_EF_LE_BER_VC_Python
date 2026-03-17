# Test, der absichtlich einen Fehler enthält, um die Funktionsweise von Mypy zu demonstrieren. In diesem Fall wird versucht, einen String als HoneyJar zurückzugeben, was zu einem Typfehler führt.
from bear_honeyworks.domain.honey import HoneyJar

def build_honeyjar() -> HoneyJar:
    return "Das ist kein HoneyJar"