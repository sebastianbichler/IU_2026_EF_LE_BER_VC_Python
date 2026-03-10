### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Project Abschlussbericht: [PenguEats]

## 1. Einleitung und Vision

### 1.1 Projektvision und Ziele

PenguEats ist eine Python-basierte Anwendung zur Unterstützung des Betriebs eines Fischrestaurants, das von Pinguinen betrieben wird und sich auf Fischgerichte spezialisiert hat.
Das zentrale Problem, das die Anwendung adressiert, ist die Unsicherheit in der Fischlieferkette. In der realen Welt können Lieferungen aufgrund von Wetterbedingungen, Fangquoten oder Transportproblemen ausfallen oder verspätet eintreffen. Diese Unsicherheiten erschweren eine zuverlässige Planung von Lagerbestand und Speisekarte.

PenguEats unterstützt den Restaurantbetreiber dabei, den Überblick über:
- Fischbestände
- Kundenbestellungen
- Einnahmen und Ausgaben
- zukünftige Fischlieferungen
zu behalten.

Das langfristige Ziel der Anwendung ist es, mithilfe datenbasierter Prognosen bessere Entscheidungen im Einkauf und der Lagerhaltung zu ermöglichen und dadurch Lieferengpässe sowie Lebensmittelverschwendung zu reduzieren.

### 1.2 Wissenschaftliche Herausforderung / Python-Spezifischer Aspekt

Der wissenschaftliche Schwerpunkt des Projekts liegt auf der probabilistischen Programmierung in Python.
Viele reale Prozesse sind nicht deterministisch, sondern unterliegen Unsicherheiten. Besonders in Lieferketten kann nicht exakt vorhergesagt werden, wann bestimmte Waren verfügbar sein werden. Daher werden diese Prozesse mit Wahrscheinlichkeitsmodellen beschrieben.

Die Anwendung nutzt hierfür bayesianische Modellierung, die es erlaubt:
- Unsicherheiten explizit zu modellieren
- Wahrscheinlichkeiten für zukünftige Ereignisse zu berechnen
- Vorhersagen mit Vertrauensintervallen zu treffen

Als Grundlage dient der wissenschaftliche Artikel "Probabilistic programming in Python using PyMC3" von Salvatier et al. (2016).

Innerhalb der Anwendung wird diese theoretische Grundlage in einer spielerischen Story-Domain umgesetzt:
In der Welt von PenguEats betreiben Pinguine ein Fischrestaurant. Die Pinguine sind auf Fischlieferanten angewiesen, die jedoch nicht immer zuverlässig liefern. Das System modelliert diese Unsicherheit und berechnet die Wahrscheinlichkeit, dass bestimmte Fischarten zu einem zukünftigen Zeitpunkt verfügbar sind.
Diese Analogie ermöglicht es, komplexe statistische Modelle anschaulich darzustellen.

### 1.3 Arbeitshypothese

Die zentrale Hypothese des wissenschaftlichen Teils lautet:
„Durch den Einsatz eines bayesianischen Modells zur Analyse historischer Lieferdaten kann die Wahrscheinlichkeit zukünftiger Fischlieferungen realistisch prognostiziert werden und daraus resultierend die Verkaufspreise für das Fischrestaurant angepasst werden.

In den Berechnungen/Analysen wird untersucht:
- wie historische Lieferdaten
- Ausfallquoten von Lieferanten
- saisonale Schwankungen
die Prognose der Fischverfügbarkeit beeinflussen.

Das Modell berechnet für jede Fischart eine Wahrscheinlichkeitsverteilung der Lieferbarkeit zu einem zukünftigen Zeitpunkt.

---

## 2. Requirements Engineering

### 2.1 Kontextdiagramm

<img width="691" height="421" alt="Use-Case-Diagramm2 drawio" src="https://github.com/user-attachments/assets/4f83ebf9-a972-4713-893c-effbfe25c4d9" />

### 2.2 Funktionale Anforderungen als Katalog

[x] Checkboxen können hier verwendet werden, um den Status der Anforderung zu dokumentieren (z. B. [x] für erfüllt, [ ]
für offen) oder per Tabelle mit einem genauen Status (z. B. 80 % erfüllt, 20 % offen) und Notizen.

| ID | Anforderung                  | Status  | Notizen                                         |
|----|------------------------------|---------|-------------------------------------------------|
| REQ-01 | Verwalten des Fischinventars | erfüllt | Speicherung von Fischart, Menge und Haltbarkeit |
| REQ-02 | Reduktion des Bestands bei Bestellung         |  | automatische Aktualisierung |
| REQ-03 | Erstellung und Verwaltung von Bestellungen         | erfüllt | Bestellung enthält Gericht und Menge |
| REQ-04 | Prüfung der Lagerverfügbarkeit vor Bestellung         |  | verhindert negative Bestände |
| REQ-05 | Verwaltung von Einnahmen und Ausgaben         | erfüllt | Verkäufe und Betriebskosten |
| REQ-06 | Berechnung der Lieferwahrscheinlichkeit von Fischarten         |  | probabilistisches Modell |
| REQ-07 | Warnung bei niedrigem Bestand         |  | Inventarüberwachung |


### 2.3 Nicht-funktionale Anforderungen (Qualitätsanforderungen)

Basierend auf der ISO 25010 werden folgende Qualitätsanforderungen definiert:

#### Performance
Die Berechnung von Prognosen soll innerhalb weniger Sekunden erfolgen, damit Entscheidungen schnell getroffen werden können.

#### Usability
Die Anwendung soll über eine einfache Benutzeroberfläche (z. B. Konsoleninterface) bedienbar sein.

#### Wartbarkeit
Der Code soll modular aufgebaut sein, sodass einzelne Komponenten wie das Prognosemodell leicht erweitert werden können.

#### Zuverlässigkeit
Das System soll sicherstellen, dass Bestellungen nur möglich sind, wenn ausreichend Inventar vorhanden ist.

### 2.4 Use-Case Modellierung

Wichtige Use-Cases des Systems sind:

#### UC-01 Fischinventar verwalten
Der Restaurantbetreiber kann Fischarten hinzufügen, aktualisieren oder entfernen.

#### UC-02 Bestellung aufnehmen
Ein Kunde bestellt ein Fischgericht. Das System prüft den Bestand und bestätigt die Bestellung.

#### UC-03 Finanzdaten verwalten
Das System erfasst Einnahmen aus Verkäufen sowie Ausgaben für Lieferungen und Betriebskosten.

#### UC-04 Lieferwahrscheinlichkeit berechnen
Das System analysiert historische Lieferdaten und berechnet Wahrscheinlichkeiten zukünftiger Lieferungen.

#### UC-05 Warnung bei niedrigem Bestand
Das System informiert den Betreiber, wenn eine Fischart knapp wird.

---

## 3. Architektur und Tech-Stack

### 3.1 Auswahl der Plattform (Begründung)

Die Anwendung wurde als Python-basierte Anwendung mit Konsoleninterface entwickelt. 

Der Grund für diese Entscheidung ist:
- einfache Integration wissenschaftlicher Modelle
- gute Unterstützung für Datenanalyse
- einfache Demonstration der probabilistischen Modelle

Es wurde die flask library verwendet.

### 3.2 Modularer Kern und Open-Closed Principle

Die Architektur der Anwendung ist modular aufgebaut.
Der Kern der Anwendung besteht aus der Geschäftslogik, die unabhängig von der Benutzeroberfläche funktioniert.

Beispiele für Module:
- Inventory Management
- Order Management
- Financial Tracking
- Prediction Model

Durch diese Struktur kann die Benutzeroberfläche später leicht ausgetauscht werden, ohne den Kern der Anwendung zu verändern.

### 3.3 Technologie-Stack

Listen Sie alle verwendeten Pakete und Tools auf (z. B. PyMC, PyTensor, Pandas) und erläutern Sie deren Rolle.

- Python:  	        Hauptprogrammiersprache
- PyMC3:            probabilistische Modellierung
- NumPy:   	        numerische Berechnungen
- arviZ:	          Datenanalyse
- flask:	          Visualisierung der Ergebnisse


### 3.4 Logging und Fehlerbehandlung

Demonstieren Sie, wie wichtige Aspekte wie Logging, Fehlerbehandlung, Performance-Optimierung und Debugging-Strategien in
der App umgesetzt wurden.

#### Logging

Das System protokolliert wichtige Ereignisse wie:
- neue Bestellungen
- Inventaränderungen
- Prognoseberechnungen

#### Fehlerbehandlung

Fehler werden mit Exception Handling abgefangen, z. B.:
- Bestellung mit unzureichendem Bestand
- ungültige Eingaben
- fehlende Daten

#### Debugging

Zur Analyse von Problemen werden Logs verwendet.


---

## 4. Design und Modellierung (Die "Story")

### 4.1 Domänenmodell und UML-Klassendiagramm

Wichtige Klassen der Anwendung sind:

- Restaurant
- Bill
- Supplier
- Order
- Delivery
- OrderItem
- MenuItem
- InventoryItem
- Fish

Beziehungen:

- Ein Restaurant besitzt ein Inventar
- Das Inventar enthält mehrere Fischarten
- Kundenbestellungen reduzieren den Bestand
- Lieferanten liefern Fisch
- Das Prognosemodell berechnet die Wahrscheinlichkeit zukünftiger Lieferungen

![UML-Diagramm](https://github.com/user-attachments/assets/fe9e9be8-6372-4898-a184-e4667c8a5b3f)

### 4.2 Verhaltensdiagramme: Activity- & State-Diagram

Zeigen Sie komplexe Abläufe (Aktivität) und die Lebenszyklen wichtiger Objekte (Zustand).

Typischer Ablauf einer Bestellung:

1. Kunde bestellt Fischgericht
2. System prüft Inventar
3. Bestellung wird bestätigt oder abgelehnt
4. Bestand wird reduziert
5. Einnahmen werden aktualisiert


### 4.3 Interaktionsdiagramm: Sequence-Diagram

Wer ruft welche Methode bei wem auf? Dokumentieren Sie hier die Kommunikation zwischen den Objekten.

### 4.4 Design Patterns und Prinzipien

Welche Muster (z. B. Factory, Strategy, MVC) wurden implementiert? Begründen Sie den Einsatz von SOLID, DRY und
KISS, ... Verwenden Sie UML-Diagramme, um die Umsetzung zu verdeutlichen.

---

## 5. Wissenschaftliche Problemstellung

### 5.1 Methodik der Untersuchung

Beschreiben Sie den Aufbau Ihres Versuchs im Notebook.(Forschungsfrage beantworten, Datenmodell)

In PyCharm wird ein bayesianisches Modell entwickelt, das die Lieferwahrscheinlichkeit von Fischarten prognostiziert.

Dazu werden folgende Daten verwendet:
- historische Lieferungen
- Lieferausfälle
- saisonale Effekte

Das Modell verwendet Markov-Chain-Monte-Carlo-Verfahren zur Schätzung der Wahrscheinlichkeitsverteilungen.

### 5.2 Analyse und Demonstration

Dokumentieren Sie die Ausführung des Codes und die Visualisierung der Ergebnisse zur Bestätigung/Widerlegung der
Hypothese. Hinterlegen Sie im Notebook aussagekräftige Plots.

---

## 6. Implementierung und Qualitätssicherung

### 6.1 Code-Struktur und Dokumentation

Hinweise zur englischsprachigen Programmierung, Docstrings und der modularen Aufteilung.

### 6.2 Test-Konzept: Unit-Tests

Listen Sie beispielhafte Unit-Tests auf, die die Kernfunktionalität absichern.

### 6.3 Integration-Tests und Traceability

Dokumentieren Sie mindestens 3 Integration-Tests. Ordnen Sie diese explizit den Software-Requirements (aus Kap. 2.2) zu.

### 6.4 CI-Pipeline

Beschreiben Sie die (mögliche) Automatisierung (GitHub Actions, Befehlsreihenfolge, Prüfung der `requirements.txt`,
project.toml).

---

## 7. Software-Qualität nach [ISO 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)

Beurteilung der Produktqualität: Skalieren und bewerten Sie Ihre Software in Kategorien wie Wartbarkeit, Zuverlässigkeit
und Benutzbarkeit.
Wählen Sie 3-5 Kategorien aus und begründen Sie die Bewertung. Welche Maßnahmen wurden ergriffen, um die Qualität zu
verbessern?

Bewertete Kategorien:

#### Wartbarkeit

Der modulare Aufbau ermöglicht eine einfache Erweiterung der Software.

#### Zuverlässigkeit

Durch Prüfungen des Inventars werden ungültige Bestellungen verhindert.

#### Benutzbarkeit

Die Anwendung bietet eine einfache Interaktion über die Konsole.

#### Performance

Die Berechnungen erfolgen effizient mit Hilfe von NumPy und PyMC.

---

## 8. Projektabschluss und Reflexion

### 8.1 Methodik und Anpassungen

Wie sind Sie vorgegangen? Welche Anpassungen mussten während der Entwicklung vorgenommen werden und warum?

### 8.2 Selbstreflexion

#### Arbeitsprozess

Analysieren Sie den Arbeitsprozess. Wo hat das Requirements Engineering geholfen, wo gab es bspw. durch "
Drauflos-Programmieren" Probleme?

#### Einsatz von KI

Bitte denkt daran, dass ihr eine schriftliche Reflektion zu eurer KI-Nutzung im Projekt mit abgeben müsst. Da alle
höchstwahrscheinlich KI-Tools verwenden werden, ist die Dokumentation des Lernfortschritts erforderlich (siehe IU
Richtlinie zur Nutzung von KI im Studium (S. 13) https://mycampus-classic.iu.org/mod/resource/view.php?id=357067)

### 8.3 Nutzungsanweisung (How-to-use)

Kurze Anleitung für den Nutzer oder den Korrektor: Wie wird die App gestartet und welche Features sind wie zu nutzen?

### 8.4 Pitch-Video

Erstellen Sie ein kurzes Video (max. 3-5 Minuten), in dem Sie die App vorstellen, die wichtigsten Funktionen
demonstrieren
und die wissenschaftliche Fragestellung sowie die Ergebnisse präsentieren.

Erstellt dazu bspw. einen Screencast mit einem Tool wie OBS Studio, Camtasia oder der System-eigenen Bildschirmaufnahme.

Examples:

- https://dl.acm.org/doi/10.1145/3411764.3445651
- https://dl.acm.org/doi/10.1145/2992154.2992174
- https://dl.acm.org/conference/chi

---

## Anhang

- **README.md (Inhalt):** Setup-Anleitung, Python-Umgebung, Paketliste.

- **Glossar:** Definition der fachlichen Begriffe der "Story".

---
