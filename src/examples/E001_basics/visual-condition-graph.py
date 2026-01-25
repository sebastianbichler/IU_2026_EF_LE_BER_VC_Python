# you need to install graphviz package: pip install graphviz and be sure to have graphiz installed on your system
from graphviz import Digraph

# dot = Digraph()
dot = Digraph("Fallunterscheidung", format="png")
dot.attr(rankdir="LR", size="8")

# Knoten
dot.node("Start", "Start")
dot.node("Cond", "Bedingung ?", shape="diamond")
dot.node("A1", "Anweisung 1", shape="box")
dot.node("A2", "Anweisung 2", shape="box")
dot.node("Weiter", "Weiterer Programmablauf")

# Kanten
dot.edge("Start", "Cond")
dot.edge("Cond", "A1", label="Ja")
dot.edge("Cond", "A2", label="Nein")
dot.edge("A1", "Weiter")
dot.edge("A2", "Weiter")

# Ausgabe (optional)
# dot.render('fallunterscheidung', view=True)
dot.render("fallunterscheidung", cleanup=True)
print("Diagram created: fallunterscheidung.png")
