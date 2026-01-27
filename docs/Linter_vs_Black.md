Ein Linter und Black lösen unterschiedliche Aufgaben:

**Linter**

- Zweck: Findet Probleme im Code (= Analyse), z.B. Fehler, schlechte Patterns, ungenutzte Imports, mögliche Bugs, Stil-Regeln.
- Output: Meldungen/Warnungen/Fehler mit Zeilenangaben.
- Beispiele: ruff, flake8, pylint.
- Optional: Manche Linter können auch Auto-Fixes machen (\z.B. ruff --fix).

**Black**

- Zweck: Formatiert Code automatisch nach einem festen Style (= Formatter).
- Output: Ändert Quelltext so, dass Einrückungen, Zeilenumbrüche, Anführungszeichen-Stil usw. konsistent sind.
- Merkmal: Kaum konfigurierbar (\„opinionated“). Ziel ist, Diskussionen über Formatierung zu vermeiden.

**Kurz gesagt:**

- Linter: „Ist der Code korrekt/sauber?“
- Black: „Wie soll der Code aussehen?“

Wir benutzen aber nur ruff, da dieser sowohl Linting- als auch Formatierungs-Funktionalität bietet.
Black würde man für Legacy-Projekte nutzen, die strikt Black-Style wollen.
