### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Project Abschlussbericht: [Name der App / Projektname]

## 1. Einleitung und Vision

### 1.1 Projektvision und Ziele

Das Projekt Football League ist eine Webanwendung zur Verwaltung und Darstellung von Informationen über eine Fußballliga.
Die Anwendung ermöglicht es, zentrale Elemente einer Liga strukturiert zu speichern und darzustellen, darunter Teams, Spieler, Wettbewerbe, Spiele und Nachrichten.

Ziel der Anwendung ist es, eine übersichtliche Plattform bereitzustellen, auf der Benutzer Informationen über Mannschaften und Spieler abrufen sowie aktuelle Spiele und Ligaereignisse verfolgen können.

Das System löst das Problem der zentralisierten Verwaltung von Ligadaten. In vielen Fällen sind Informationen über Spieler, Teams oder Spiele auf verschiedenen Plattformen verteilt. Die Anwendung bündelt diese Daten in einer einzigen Anwendung und stellt sie strukturiert dar.

Typische Nutzer der Anwendung sind:

1) Fußballfans, die Informationen über Spieler und Teams suchen

2) Organisatoren oder Administratoren, die Ligadaten verwalten

3) Nutzer, die aktuelle Spiele und Wettbewerbe verfolgen möchten

Durch die klare Struktur der Datenmodelle und die Nutzung einer Datenbank können neue Informationen einfach hinzugefügt und aktualisiert werden.

### 1.2 Wissenschaftliche Herausforderung / Python-Spezifischer Aspekt

Der technische Fokus des Projekts liegt auf der modularen Architektur einer Python-Anwendung mit klar definierten Datenmodellen und Typisierung.

Ein wichtiger Aspekt ist die Verwendung von Python Type Hints (typing), um die Struktur der Daten klar zu definieren und Fehler bereits während der Entwicklung zu vermeiden. Durch die Nutzung von Typisierung wird der Code besser lesbar, wartbarer und weniger fehleranfällig.

Die Anwendung verwendet eine NoSQL-Datenbank (MongoDB), wodurch flexible Datenstrukturen möglich sind. Die Daten werden in Form von Dokumenten gespeichert und über Python-Modelle verarbeitet.

Die Architektur folgt einer klaren Trennung von Komponenten:

1) Models - definieren die Datenstruktur (z. B. Spieler, Teams)

2) Services 

3) Datenbank-Layer - Verbindung zur MongoDB

Ein Beispiel ist der Zugriff auf Spielerdaten:

    def get_player(player_id: str) -> Player | None:

Durch die Verwendung von Typisierung wird klar definiert, welcher Datentyp zurückgegeben wird.

Als Analogie kann man sich die Anwendung wie eine digitale Fußballliga-Verwaltung vorstellen:

1) Teams sind die Organisationseinheiten der Liga

2) Spieler gehören zu Teams

3) Spiele verbinden zwei Teams miteinander

4) Wettbewerbe organisieren mehrere Spiele

5) Nachrichten informieren über Ereignisse in der Liga

Diese Struktur bildet die reale Organisation einer Fußballliga im Softwaremodell ab.

### 1.3 Arbeitshypothese

Im wissenschaftlichen Teil des Projekts wird untersucht, wie sich Typisierung und strukturierte Datenmodelle auf die Qualität und Wartbarkeit einer Python-Anwendung auswirken.

Die Arbeitshypothese lautet:

"Die Verwendung von MyPy und klar definierten Datenmodellen verbessert die Wartbarkeit und Fehlersicherheit einer Anwendung zur Verwaltung von Fußballligadaten."

Zur Untersuchung dieser Hypothese werden verschiedene Aspekte analysiert, beispielsweise:

- Struktur und Validierung der Datenmodelle (Spieler, Teams, Spiele)
- Konsistenz der Datentypen bei Datenbankoperationen
- Vergleich von Code mit und ohne Typisierung

Die Datenentities der Anwendung umfassen unter anderem:

- Player
- Team
- Game
- Competition
- News

Diese Modelle bilden die Grundlage für die Analyse und Demonstration im wissenschaftlichen Teil.

---

## 2. Requirements Engineering

### 2.1 Kontextdiagramm

Die Anwendung Football League ist eine Webanwendung zur Darstellung von Informationen über eine Fußballliga.
Das System ermöglicht es Benutzern, Daten über Teams, Spieler, Spiele, Wettbewerbe und Nachrichten zu betrachten.

Die Anwendung interagiert mit folgenden externen Komponenten:

Externe Akteure:

1) Benutzer (User)
Der Benutzer greift über einen Webbrowser auf die Anwendung zu und kann Informationen über Teams, Spieler, Spiele und Wettbewerbe abrufen.

2) MongoDB Datenbank
Alle Ligadaten (Spieler, Teams, Spiele, Wettbewerbe und Nachrichten) werden in einer MongoDB-Datenbank gespeichert.

Systemübersicht:

    +-------------------+
    |       User        |
    +---------+---------+
              |
              v
    +-------------------+
    |   Football App    |
    |     (Python)      |
    +---------+---------+
              |
              v
    +-------------------+
    |      MongoDB      |
    |     Database      |
    +-------------------+

Der Benutzer sendet Anfragen an die Anwendung, welche die benötigten Daten aus der Datenbank abruft und im Interface darstellt.

### 2.2 Funktionale Anforderungen

| ID  | Beschreibung                                                                                    | Priorität |
| :-: | ----------------------------------------------------------------------------------------------- | :-------: |
| FK1 | Turnierverwaltung: Auflistung aller verfügbaren Turniere.                                       | Muss      |
| FK2 | Teamverwaltung: Erfassen von Namen, Positionen und Trikotnummern.                               | Muss      |
| FK3 | Ergebnis-Erfassung: Protokollierung von Toren, Karten und Torschützen während eines Spiels.     | Muss      |
| FK4 | Tabellenberechnung: Automatische Berechnung der Punkte und Ranglisten pro Turnier.              | Muss      |
| FK5 | Spielplan-Logik: Automatische Erstellung von Hin- und Rückrunden sowie Terminen.                | Könnte    |
| FK6 | Finanzen: Tracking von Einnahmen (Tickets) und Ausgaben (Miete, Schiedsrichter).                | Könnte    |
| FK7 | Spieler-Statistiken: Visualisierung der besten Spieler und Fairplay-Wertungen.                  | Könnte    | 

### 2.3 Nicht-funktionale Anforderungen

Neben den funktionalen Anforderungen muss das System bestimmte Qualitätsanforderungen erfüllen.

Das System soll Datenbankabfragen effizient durchführen.
Spieler-, Team- und Spielinformationen sollen schnell aus der MongoDB-Datenbank geladen werden.

Wartbarkeit (Maintainability)

Der Code folgt einer modularen Struktur:

- Models definieren Datenstrukturen
- Services enthalten Geschäftslogik
- Database Layer verwaltet Datenbankzugriffe

Durch diese Struktur kann die Anwendung leichter erweitert werden.

Das System muss sicherstellen, dass fehlerhafte Datenbankabfragen korrekt behandelt werden.
Falls ein Objekt nicht existiert, soll das System None zurückgeben, anstatt einen Fehler zu verursachen.

Durch die Nutzung einer NoSQL-Datenbank (MongoDB) kann das System leicht erweitert werden, wenn neue Spiele, Teams oder Wettbewerbe hinzugefügt werden.

### 2.4 Use-Case Modellierung

### UC1. Teams anzeigen

| Feld | Beschreibung |
|-----|-------------|
| **Name** | Teams anzeigen |
| **Akteur** | Benutzer |
| **Beschreibung** | Der Benutzer möchte eine Liste aller Teams der Liga sehen. |
| **Vorbedingung** | Die Anwendung ist gestartet und die Datenbank enthält Teamdaten. |
| **Hauptablauf** | 1. Benutzer öffnet die Teamseite.<br>2. Das System sendet eine Anfrage an die Datenbank.<br>3. Die Teams werden aus MongoDB geladen.<br>4. Die Teamliste wird angezeigt. |
| **Ergebnis** | Alle Teams der Liga werden im Interface angezeigt. |

### UC2. Spieler eines Teams anzeigen

| Feld | Beschreibung |
|-----|-------------|
| **Name** | Spieler eines Teams anzeigen |
| **Akteur** | Benutzer |
| **Beschreibung** | Der Benutzer möchte alle Spieler eines bestimmten Teams sehen. |
| **Vorbedingung** | Das Team existiert in der Datenbank. |
| **Hauptablauf** | 1. Benutzer wählt ein Team aus.<br>2. Das System ruft alle Spieler mit entsprechender `team_id` ab.<br>3. Die Spieler werden geladen.<br>4. Die Spieler werden im Interface angezeigt. |
| **Ergebnis** | Die Liste der Spieler des ausgewählten Teams wird angezeigt. |

### UC3. Spielerprofil anzeigen

| Feld | Beschreibung |
|-----|-------------|
| **Name** | Spielerprofil anzeigen |
| **Akteur** | Benutzer |
| **Beschreibung** | Der Benutzer möchte detaillierte Informationen über einen Spieler sehen. |
| **Vorbedingung** | Der Spieler existiert in der Datenbank. |
| **Hauptablauf** | 1. Benutzer klickt auf einen Spieler.<br>2. Das System ruft die Spielerdaten aus der Datenbank ab.<br>3. Die Daten werden verarbeitet.<br>4. Das Spielerprofil wird angezeigt. |
| **Ergebnis** | Der Benutzer sieht Informationen über den Spieler (Name, Position, Nummer, Team). |

### UC4. Spiele eines Wettbewerbs anzeigen

| Feld | Beschreibung |
|-----|-------------|
| **Name** | Spiele anzeigen |
| **Akteur** | Benutzer |
| **Beschreibung** | Der Benutzer möchte alle Spiele eines Wettbewerbs sehen. |
| **Vorbedingung** | Der Wettbewerb existiert in der Datenbank. |
| **Hauptablauf** | 1. Benutzer öffnet einen Wettbewerb.<br>2. Das System lädt alle Spiele mit entsprechender `competition_id`.<br>3. Die Spiele werden angezeigt. |
| **Ergebnis** | Der Benutzer sieht eine Liste der Spiele des Wettbewerbs. |

### UC5. Spielstatistiken anzeigen

| Feld | Beschreibung |
|-----|-------------|
| **Name** | Spielstatistiken anzeigen |
| **Akteur** | Benutzer |
| **Beschreibung** | Der Benutzer möchte Statistiken eines Spiels sehen. |
| **Vorbedingung** | Das Spiel existiert in der Datenbank. |
| **Hauptablauf** | 1. Benutzer öffnet ein Spiel.<br>2. Das System lädt die Spieldaten.<br>3. Tore und Karten werden aus der Datenbank geladen.<br>4. Die Statistiken werden angezeigt. |
| **Ergebnis** | Der Benutzer sieht Tore, Karten und weitere Statistiken des Spiels. |

---

## 3. Architektur und Tech-Stack

### 3.1 Auswahl der Plattform

Flask wurde als Web-Framework ausgewählt, da es eine äußerst flexible und schlanke Struktur bietet. Im Gegensatz zu geschlossenen Systemen ermöglicht Flask eine klare Trennung von Logik und Darstellung. Die Entscheidung fiel auf Flask, um eine echte Webanwendung mit einer klaren Struktur zu entwickeln, die deutlich skalierbarer ist als einfache Skripte oder interaktive Notebooks.


### 3.2 Modularer Kern und Open-Closed Principle

Die Anwendung wurde so strukturiert, dass der Kern des Systems modular bleibt und einfach erweitert werden kann, ohne bestehenden Code ändern zu müssen. Durch die Trennung in verschiedene Ordner können neue Funktionen hinzugefügt werden, indem man einfach neue Klassen und Routen ergänzt. Es wurde entschieden das Projekt in folgende Bereiche aufzuteilen, um eine klare Struktur und Wartbarkeit zu garantieren:

- **/models:** Dieser Ordner enthält die Datenstrukturen, die dank **MyPy** genau festlegen, welche Eigenschaften ein *Player* oder ein *Team* hat.
- **/services:** Dieser Ordner enthält Services mit der Logik (CRUD) - also das Erstellen, Lesen, Bearbeiten und Löschen von Daten.
- **/routes:** Dieser Ordner enthält Routen, die festlegen, welche Route welcher Action-Methode entspricht.
- **/templates:** Dieser Ordner enthält die HTML-Dateien, in denen durch Flask direkt Python-Code für die Anzeige der Daten genutzt wird.

### 3.3 Technologie-Stack

Für die technische Umsetzung der Anwendung wurde eine Kombination aus modernen und flexiblen Werkzeugen gewählt. Es wurde entschieden, den Fokus auf eine starke Typisierung und eine einfache Skalierbarkeit zu legen.

- **Python, Flask:** Diese bilden das Grundgerüst des Backends, da Flask sehr schnell für Web-Projekte einsatzbereit ist.
- **MongoDB, PyMongo:** Als Datenbank wurde eine NoSQL-Datenbank MongoDB gewählt, da sie eine flexible Datenspeicherung ermöglicht. Dadurch können zusätzliche Informationen, beispielsweise neue Statistiken, leicht hinzugefügt werden, ohne bereits vorhandene Daten zu beeinträchtigen.
- **MyPy:** Dieses Tool überprüft statische Typen in Python, wodurch potenzielle Fehler und Bugs erkannt werden können, noch bevor das Programm startet.
- **Bootstrap:** Diese Style-Bibliothek wird verwendet, um das Frontend modern zu gestalten, ohne alle Styles manuell erstellen zu müssen.

## 4. Design und Modellierung (Die "Story")

### 4.1 Domänenmodell und UML-Klassendiagramm

Die Anwendung modelliert die Struktur einer Fußballliga. Die wichtigsten Objekte der Domäne sind Teams, Spieler, Spiele, Wettbewerbe und verschiedene Spielstatistiken.

Das zentrale Konzept der Anwendung ist die abstrakte Basisklasse `Entity`. Alle anderen Domänenmodelle erben von dieser Klasse und besitzen gemeinsame Eigenschaften wie:

- `id`
- `created_at`
- `updated_at`

Dadurch wird eine einheitliche Struktur für alle Datenmodelle sichergestellt.

Wichtige Domänenobjekte sind:

- **Team** - repräsentiert eine Fußballmannschaft
- **Player** - repräsentiert einen Spieler, der zu einem Team gehört
- **Game** - repräsentiert ein Spiel zwischen zwei Teams
- **Competition** - beschreibt einen Wettbewerb oder eine Liga
- **CardRecord** - speichert gelbe oder rote Karten eines Spiels
- **GoalRecord** - speichert Tore eines Spiels

Die Beziehungen zwischen den Objekten werden über **IDs (MongoDB ObjectId)** modelliert.

Beispiele für Beziehungen:

- Ein **Team** enthält mehrere **Player**
- Ein **Game** verbindet zwei Teams (`team_1_id`, `team_2_id`)
- Ein **Game** gehört zu einem **Competition**
- Ein **CardRecord** gehört zu einem **Game** und einem **Player**
- Ein **GoalRecord** gehört zu einem **Game**, einem **Player** und einem **Team**

Diese Referenzen ermöglichen eine flexible Datenstruktur innerhalb der MongoDB-Datenbank.

Die Beziehungen zwischen allen Domänenobjekten und Services sind im UML-Diagramm unter [./docs/UML-Diagramm.md](./docs/UML-Diagramm.md) zu finden.

### 4.2 Verhaltensdiagramme: Activity- & State-Diagram

Das Verhalten des Systems wird durch typische Abläufe innerhalb der Anwendung beschrieben.

Ein Beispiel ist der Ablauf beim Anzeigen von Spielern eines Teams.

**Activity Ablauf:**

1. Der Benutzer öffnet eine Teamseite.
2. Das System empfängt die Anfrage über eine Route.
3. Der entsprechende Service ruft die Daten aus der MongoDB-Datenbank ab.
4. Die Daten werden in Modellobjekte (z. B. Player) konvertiert.
5. Die Spieler werden im Interface angezeigt.

### 4.3 Interaktionsdiagramm: Sequence-Diagram

Die Kommunikation innerhalb der Anwendung folgt einer klaren Struktur.

Die Architektur besteht aus mehreren Schichten:

- **Routes** - empfangen Benutzeranfragen
- **Services** - enthalten Geschäftslogik
- **Models** - repräsentieren Datenobjekte
- **Database Layer** - kommuniziert mit MongoDB

Ein typischer Ablauf beim Abrufen von Spielern ist:

1. Der Benutzer sendet eine Anfrage an eine Route.
2. Die Route ruft den entsprechenden Service auf.
3. Der Service führt eine Datenbankabfrage aus.
4. Die Daten werden in Modellobjekte konvertiert.
5. Die Ergebnisse werden an den Benutzer zurückgegeben.

Dieser Ablauf trennt klar die Verantwortlichkeiten der einzelnen Komponenten.

### 4.4 Design Patterns und Prinzipien

### Software-Design-Prinzipien

**Layered Architecture**

Die Anwendung ist in mehrere Schichten unterteilt:

- **Routes Layer** - verarbeitet HTTP-Anfragen
- **Service Layer** - enthält Geschäftslogik
- **Model Layer** - definiert Datenstrukturen
- **Database Layer** - verwaltet Datenbankzugriffe

Diese Struktur verbessert Wartbarkeit und Erweiterbarkeit des Systems.

### SOLID Prinzipien

**Single Responsibility Principle**

Jede Klasse hat eine klar definierte Aufgabe.

Beispiele:

- Models repräsentieren Datenstrukturen
- Services enthalten Geschäftslogik
- Routes verarbeiten Benutzeranfragen

**Open-Closed Principle**

Die Verwendung einer abstrakten Basisklasse `Entity` ermöglicht es, neue Modelle zu erstellen, ohne bestehende Klassen zu verändern.

---

## 5. Wissenschaftliche Problemstellung (Jupyter Notebook)

### 5.1 Methodik der Untersuchung

In diesem Abschnitt wird die zentrale Forschungsfrage untersucht: *Ist der Einsatz der statischen Typisierung mit MyPy in komplexen Python-Webanwendungen sinnvoll, wenn man den zusätzlichen Zeitaufwand für die Definition aller Typen gegen die Vorteile abwägt?*

Um dies zu untersuchen, wurde ein spezifischer Versuchsaufbau gewählt. Es wurde entschieden, das Projekt in zwei Teilen zu implementieren:
Für bestimmte Entitäten, wie beispielsweise den *Player* (im Modell, Service und in der Route), wurde MyPy konsequent angewendet und jeder Datentyp präzise definiert.
Im Gegensatz dazu wurden andere Entitäten, wie beispielsweise das *Team*, ohne Typspezifikationen definiert.

Dies ermöglicht einen direkten Vergleich der Fehleranfälligkeit der verschiedenen Bereiche.

### 5.2 Analyse und Demonstration

Die Durchführung der Untersuchung hat gezeigt, dass der Aufwand für das Definieren der Typen in den Klassen und Methoden minimal war. Es wurde festgestellt, dass man nur wenig zusätzliche Zeit benötigt, um die Felder korrekt zu typisieren, sobald man sich an die Syntax gewöhnt hat.

Der konkrete Nutzen lässt sich durch das Ausführen des **MyPy**-Befehls in der Konsole belegen. Die Ausführungen und Ergebnisse werden im Jupyter Notebook angezeigt ([mypy.ipynb](./mypy.ipynb)).

---

## 6. Implementierung und Qualitätssicherung

### 6.1 Code-Struktur und Dokumentation

Es wurde entschieden, auf klassische Docstrings oder ausführliche Kommentare innerhalb der Methoden zu verzichten, da der Code durch zwei Faktoren selbsterklärend ist:

1. **Einsatz von MyPy:** Da durch MyPy alle Methoden-Argumente und Rückgabewerte direkt im Code mit Typen versehen sind, ist sofort ersichtlich, welche Daten eine Funktion erwartet und was sie zurückgibt.
2. **Klare Namensgebung:** Aufgrund des Open-Closed-Prinzips und einer sehr sauberen Benennung (z. B. get_all_players oder create_game) ist die Funktion jeder Methode auch ohne Dokumentation eindeutig.

Die modulare Aufteilung folgt dabei einem klaren Datenfluss, der die Wartung erleichtert:
Die Daten wandern von den **Models** über die **Services** zu den **Routes** und werden schließlich in den **Templates** ausgegeben. Diese strikte Trennung sorgt dafür, dass jeder Code-Abschnitt nur eine einzige, klar definierte Aufgabe hat.

### 6.2 Test-Konzept: Unit-Tests

Für einfache Service-Methoden, die Daten lediglich aus der Datenbank abfragen und an die Routes weitergeben, ist der Einsatz von Unit-Tests nur wenig sinnvoll, da hier kaum eigene Programmlogik existiert.

Potenziell hilfreich wären Tests jedoch für komplexere Berechnungen, wie zum Beispiel die Methode `get_team_stats` in [stats_service.py](./src/services/stats_service.py). Da hier aus einzelnen Spielergebnissen und Toren wichtige Kennzahlen wie Siege, Niederlagen und die Tordifferenz ermittelt werden, könnte ein Unit-Test sicherstellen, dass die mathematische Logik auch bei unterschiedlichen Spielausgängen immer korrekt funktioniert.

---

## 7. Software-Qualität nach [ISO 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)

Die Qualität der entwickelten Anwendung wird anhand ausgewählter Kriterien des ISO 25010 Software Quality Models bewertet.  
Für dieses Projekt wurden die Kategorien Wartbarkeit, Zuverlässigkeit, Benutzbarkeit und Performance betrachtet.

### Wartbarkeit (Maintainability)

Die Wartbarkeit der Anwendung wird als **hoch** bewertet.

Die Anwendung ist modular aufgebaut und folgt einer klaren Architekturstruktur.

Zusätzlich wird eine abstrakte Basisklasse `Entity` verwendet, welche gemeinsame Eigenschaften wie `id`, `created_at` und `updated_at` definiert.  
Dadurch wird Code-Duplikation reduziert und neue Modelle können leichter erweitert werden.

### Zuverlässigkeit (Reliability)

Die Zuverlässigkeit der Anwendung wird als **hoch** bewertet.

- Die Anwendung stellt sicher, dass Daten aus der Datenbank korrekt verarbeitet werden.
- Die Anwendung prüft vor der Verarbeitung, ob Objekte vorhanden sind. Dies trägt dazu bei, Laufzeitfehler zu reduzieren.
- Die Anwendung führt mit MyPy Typüberprüfungen durch, wodurch Typfehler bereits zur Kompilierungszeit verhindert werden.
- Die Verwendung klar definierter Datenmodelle trägt ebenfalls zur Stabilität des Systems bei.

---

## 8. Projektabschluss und Reflexion

### 8.1 Methodik und Anpassungen

Bei der Entwicklung wurde schrittweise vorgegangen, wobei zuerst die Datenbankstruktur in *MongoDB* und danach die Logik in den Services aufgebaut wurde. Während der Programmierung mussten Anpassungen bei der Typisierung vorgenommen werden, da einige Datenformate aus der Datenbank erst exakt definiert werden mussten, damit *MyPy* keine Fehlermeldungen mehr ausgibt.

### 8.2 Selbstreflexion
    
#### Arbeitsprozess

Da die Projektentwicklung in drei klar voneinander abgegrenzte Phasen unterteilt war, wurde der gesamte Prozess erheblich vereinfacht. Da die Struktur, der Code und die Datenbankmodelle im Voraus geplant wurden, war es nicht notwendig, während der Programmierphase irgendetwas grundlegend umzuschreiben oder zu überarbeiten.

#### Einsatz von KI

Künstliche Intelligenz wurde im Projekt gezielt für Erklärungen und zur Klärung von Fachfragen genutzt, zum Beispiel um die genauen Vorteile von MyPy und statischer Typisierung besser zu verstehen. Außerdem wurde KI für die Gestaltung des Frontends mit Bootstrap verwendet, da das Design nicht der Hauptschwerpunkt des Kurses war und so mehr Zeit für die Implementierung blieb.

### 8.3 Nutzungsanweisung (How-to-use)

1. Virtuelle Umgebung aktivieren

    ```
    .\.venv\Scripts\activate
    ```

2. Installation

    ```
    pip install -r requirements.txt
    ```

3. Typ-Prüfung

    ```
    mypy .
    ```

4. Start

    ```
    flask run
    ```

Nach dem Start der App kann der Nutzer verschiedene Bereiche aufrufen:

1. **Teams:** In diesem Bereich werden alle Mannschaften angezeigt. Durch Anklicken einer Mannschaft werden Details wie eine Beschreibung und eine Liste aller Spieler dieser Mannschaft angezeigt.
2. **Competitions**: In diesem Bereich werden alle Wettbewerbe angezeigt. Durch Anklicken eines Wettbewerbs werden Details wie eine Beschreibung, ein Spielplan und eine "Scoreboard" angezeigt, die automatisch Statistiken berechnet.
3. **Statistics**: Diese Seite ist in "Game statistics" und "Player statistics" unterteilt und bietet eine Übersicht über die verschiedenen Leistungsdaten des Portals.

## Anhang

- [**README.md:**](./README.md) Setup-Anleitung, Python-Umgebung, Paketliste.

---
