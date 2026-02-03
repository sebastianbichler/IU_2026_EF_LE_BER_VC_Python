Anforderungen – Bear Honeyworks (mypy)

Das Projekt Bear Honeyworks modelliert die Abläufe einer fiktiven Honigfabrik eines Bären.
Ziel ist es, mithilfe von mypy die Vorteile statischer Typprüfung in Python praxisnah zu demonstrieren.
Die Priorisierung der Anforderungen erfolgt nach dem MoSCoW-Prinzip.

## 1. Funktionale Anforderungen

### F-01 – Typgesicherte Domänenmodelle (Must)

Das System muss zentrale Fachobjekte der Honigfabrik (z. B. Bär, Honigglas, Lager, Bestellung) mithilfe von Python-Typannotationen abbilden.

Abnahme:
	•	Alle Klassen und Funktionen besitzen explizite Typannotationen.
	•	mypy meldet bei korrektem Code keine Fehler.
	•	Falsche Typverwendungen (z. B. str statt float) werden von mypy erkannt.

### F-02 – Statische Typprüfung mit mypy (Must)

Das Projekt muss vollständig mit mypy überprüfbar sein.

Abnahme:
	•	mypy lässt sich über CLI ausführen.
	•	Typfehler werden vor der Programmausführung erkannt.
	•	Die Anwendung läuft ohne Laufzeitfehler bei korrekten Typen.

### F-03 – Produktionslogik für Honig (Must)

Der Bär muss Honig produzieren und als Honiggläser zurückgeben können.

Abnahme:
	•	Die Produktionsfunktion liefert ein korrekt typisiertes Objekt zurück.
	•	Die Rückgabewerte entsprechen den definierten Typen.
	•	Falsche Rückgabetypen werden durch mypy verhindert.

### F-04 – Lagerverwaltung (Should)

Das System soll einen Lagerbestand für Honiggläser verwalten.

Abnahme:
	•	Honiggläser können dem Lager hinzugefügt werden.
	•	Das Lager akzeptiert nur gültige Honigglas-Objekte.
	•	mypy verhindert das Einlagern falscher Datentypen.

### F-05 – Bestellverarbeitung (Should)

Bestellungen sollen eine definierte Menge Honig anfordern können.

Abnahme:
	•	Bestellungen besitzen klar definierte Datentypen (Menge, Gewicht, Preis).
	•	Ungültige Typen führen zu mypy-Fehlern.
	•	Die Bestelllogik ist vollständig typgesichert.

### F-06 – Fehlerhafte Typverwendung demonstrieren (Could)

Das Projekt soll bewusst fehlerhafte Typverwendungen enthalten, um mypy-Fehlermeldungen zu demonstrieren.

Abnahme:
	•	Beispielcode erzeugt reproduzierbare mypy-Fehler.
	•	Die Fehlermeldungen sind nachvollziehbar und erklärbar.
	•	Nach Korrektur verschwinden die Fehler vollständig.

### F-07 – Erweiterbarkeit des Modells (Could)

Das System soll einfach um neue Komponenten (z. B. Lieferant, Verkauf, Qualitätsprüfung) erweiterbar sein.

Abnahme:
	•	Neue Klassen lassen sich typisiert integrieren.
	•	mypy prüft neue Komponenten ohne Anpassung der bestehenden Logik.
	•	Bestehende Typverträge bleiben stabil.

## 2. Nicht-funktionale Anforderungen (Qualität)

### NFA-01 – Codequalität & Wartbarkeit

Der Code muss durch Typannotationen klar strukturiert und gut wartbar sein.

Abnahme:
	•	Typannotationen erleichtern das Verständnis des Codes.
	•	IDE-Unterstützung (Autocomplete, Warnungen) funktioniert zuverlässig.

### NFA-02 – Frühe Fehlererkennung

Typfehler sollen bereits vor der Programmausführung erkannt werden.

Abnahme:
	•	Fehler werden von mypy gemeldet, bevor das Programm gestartet wird.
	•	Laufzeitfehler durch falsche Typen treten nicht auf.

### NFA-04 – Reproduzierbarkeit

Gleicher Code und gleiche Eingaben führen zu identischen mypy-Ergebnissen.

Abnahme:
	•	Mehrere mypy-Durchläufe liefern konsistente Ergebnisse.
	•	Keine zufallsabhängigen Typprüfungen.