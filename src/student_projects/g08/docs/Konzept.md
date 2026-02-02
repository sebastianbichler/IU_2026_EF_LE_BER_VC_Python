# Konzept – Bear Honeyworks 

## Leitfrage 

„Welchen Mehrwert bietet statische Typprüfung mit mypy in dynamisch typisierten Python-Anwendungen
am Beispiel eines domänenspezifischen Produktionssystems?“


## Erläuterung 

Ziel des Projekts „Bear Honeyworks“ ist die Entwicklung einer vereinfachten Software zur Modellierung einer fiktiven Honigfabrik eines Bären.

Das System bildet typische fachliche Prozesse ab, darunter:
	•	Honigproduktion
	•	Lagerverwaltung
	•	Bestellverarbeitung

Im Fokus steht dabei nicht die Laufzeitoptimierung, sondern die Absicherung der fachlichen Logik durch statische Typprüfung.

Mithilfe von mypy soll untersucht werden, inwiefern:
	•	Typfehler frühzeitig erkannt
	•	Laufzeitfehler reduziert
	•	Codeverständlichkeit und Wartbarkeit verbessert

werden können – trotz der dynamischen Natur von Python.


## Zielsetzung 

Das Projekt verfolgt folgende Ziele:
	•	Demonstration statischer Typprüfung in Python
	•	Praxisnahe Modellierung einer Domäne (Honigfabrik)
	•	Aufzeigen typischer Fehlerquellen ohne Typprüfung
	•	Vergleich von Code mit und ohne mypy-Absicherung

Der Fokus liegt auf Softwarequalität, nicht auf Performance.


## Systemaufbau 

Konzeptionell besteht „Bear Honeyworks“ aus mehreren logisch getrennten Komponenten:
	•	einem Domänenmodul für zentrale Fachobjekte (z. B. Bär, Honigglas, Bestellung)
	•	einem Produktionsmodul zur Erzeugung von Honig
	•	einem Lagermodul zur Verwaltung des Bestands
	•	einer Validierungs- und Prüfkomponente durch mypy

Die Module sind bewusst stark typisiert, um klare Schnittstellen zwischen den Komponenten zu definieren.


## Methodik 

Die Methodik des Projekts basiert auf einem vergleichenden Analyseansatz:
	•	Implementierung fachlicher Logik mit vollständigen Typannotationen
	•	Prüfung des Codes mit mypy
	•	gezielte Einbringung fehlerhafter Typverwendungen
	•	Analyse der von mypy erzeugten Fehlermeldungen

Zusätzlich wird untersucht, wie sich Typannotationen auf:
	•	Lesbarkeit
	•	Entwicklungsunterstützung (IDE)
	•	Fehlersuche

auswirken.

Der Ansatz ist qualitativ-analytisch und nicht benchmark-orientiert.


## Typisierungskonzept 

Zur Typabsicherung werden unter anderem eingesetzt:
	•	primitive Typen (int, float, str)
	•	zusammengesetzte Typen (List, Optional)
	•	Rückgabetypen von Funktionen
	•	Klassenattribute mit expliziten Typen

Alle fachlichen Objekte besitzen klar definierte Typverträge, die von mypy überprüft werden.


## Technologien & Entscheidungen 

Zur Umsetzung des Projekts wurden folgende Technologien gewählt:

Programmiersprache
	•	Python
	•	Begründung: Python ist dynamisch typisiert und eignet sich daher besonders gut, um den Nutzen statischer Typprüfung sichtbar zu machen.

Statische Typprüfung
	•	mypy
	•	Begründung: Etablierter De-facto-Standard für statische Typprüfung in Python, mit guter Tool- und IDE-Integration.

Typannotationssystem
	•	typing (Standardbibliothek)
	•	Begründung: Ermöglicht präzise Typdefinitionen ohne zusätzliche Abhängigkeiten.

Entwicklungsumgebung
	•	IDE mit mypy-Integration
	•	Begründung: Sofortige Rückmeldung über Typfehler erhöht Entwicklungsqualität und Produktivität.


## Abgrenzung 

Nicht Bestandteil des Projekts sind:
	•	Performance-Optimierungen
	•	Datenbankanbindungen
	•	Benutzeroberflächen
	•	Nebenläufigkeit oder Parallelisierung

Der Fokus liegt ausschließlich auf Typensicherheit und Softwarequalität.


## Projektstruktur & Architektur 

Um die Typprüfung mit mypy sinnvoll und wartbar einzusetzen, wird Bear Honeyworks modular aufgebaut.
Die fachliche Logik wird in klar getrennte Komponenten aufgeteilt, sodass jede Schicht eindeutige Typverträge besitzt.

Ordnerstruktur (geplant)
	•	src/
	•	domain/ – Domänenmodell (reine Daten- und Fachobjekte)
	•	bear.py (Bär / Produzent)
	•	honey.py (Honigglas, Honigtypen, ggf. Qualitätsstufen)
	•	order.py (Bestellung, Positionen)
	•	services/ – Geschäftslogik / Use-Cases
	•	production_service.py (Produktion erzeugt Gläser)
	•	inventory_service.py (Einlagern, Entnehmen, Bestand)
	•	order_service.py (Bestellungen prüfen & ausführen)
	•	repositories/ – Datenzugriff / Speicherung (optional, auch in-memory)
	•	inventory_repository.py
	•	order_repository.py
	•	cli/ oder app.py – Einstiegspunkt zum Testen der Abläufe (Demo für Prüfung)
	•	tests/ – Unit-Tests (optional)
	•	pyproject.toml oder mypy.ini – mypy-Konfiguration

Warum so?
	•	domain/ bleibt möglichst „clean“ (keine IO, keine Nebenwirkungen)
	•	services/ kapseln Logik und validieren Typen/Schnittstellen
	•	repositories/ machen späteres Erweitern leicht (Datei/DB), ohne Logik umzubauen



Klassendesign & Typverträge 

Das Modell wird objektorientiert mit klaren Verantwortlichkeiten umgesetzt:
	•	Bear: produziert Honig (liefert typisierte HoneyJar zurück)
	•	HoneyJar: enthält feste Attribute wie Gewicht, Sorte, Qualitätsstufe
	•	Inventory / InventoryRepository: verwaltet Bestand als typisierte Sammlung
	•	Order: beschreibt Bestellanforderungen (Menge, Sorte, max. Preis etc.)
	•	Services übernehmen die Abläufe (Produktion → Lager → Bestellung)

mypy-Ziel dabei:
Jede Service-Methode hat eindeutige Parameter- und Rückgabetypen, sodass Fehler wie „falsche Einheit“, „falsches Objekt“, „None statt Objekt“ früh erkannt werden.



Konfigurationsansatz für mypy 

Die Typprüfung wird so konfiguriert, dass sie für die Prüfung klar nachweisbar ist:
	•	striktere Einstellungen (z. B. disallow_untyped_defs)
	•	klare Trennung: Domain strikt typisiert, Demo-Code ebenfalls
	•	demonstrierbare Fehlerfälle (absichtlich falscher Typ) als Prüfbeispiel