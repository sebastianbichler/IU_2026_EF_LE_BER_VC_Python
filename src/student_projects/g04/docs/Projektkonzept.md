# Foorball League

## 1. Aufgabenstellung

Die Anwendung "Football League" wird als zentrales Informationsportal für Fußballfans dienen. Der Zweck besteht darin, den Nutzern einen schnellen Zugriff auf eine übersichtliche Darstellung des Spielplans und der Spielergebnisse zu ermöglichen.

## 2. Anforderungen

### 2.1 Funktionale Anforderungen

| ID  | Beschreibung                                                                                    | Priorität |
| :-: | ----------------------------------------------------------------------------------------------- | :-------: |
| FK1 | Turnierverwaltung: Auflistung aller verfügbaren Turniere.                                       | Muss      |
| FK2 | Teamverwaltung: Erfassen von Namen, Positionen und Trikotnummern.                               | Muss      |
| FK3 | Ergebnis-Erfassung: Protokollierung von Toren, Karten und Torschützen während eines Spiels.     | Muss      |
| FK4 | Tabellenberechnung: Automatische Berechnung der Punkte und Ranglisten pro Turnier.              | Muss      |
| FK5 | Spielplan-Logik: Automatische Erstellung von Hin- und Rückrunden sowie Terminen.                | Könnte    |
| FK6 | Finanzen: Tracking von Einnahmen (Tickets) und Ausgaben (Miete, Schiedsrichter).                | Könnte    |
| FK7 | Spieler-Statistiken: Visualisierung der besten Spieler und Fairplay-Wertungen.                  | Könnte    | 

### 2.2 Nicht-funktionale Anforderungen

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

## 3. Use-Cases

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

## 4. Tech-Stack

- **Python, Flask:** Diese bilden das Grundgerüst des Backends, da Flask sehr schnell für Web-Projekte einsatzbereit ist.
- **MongoDB, PyMongo:** Als Datenbank wurde eine NoSQL-Datenbank MongoDB gewählt, da sie eine flexible Datenspeicherung ermöglicht. Dadurch können zusätzliche Informationen, beispielsweise neue Statistiken, leicht hinzugefügt werden, ohne bereits vorhandene Daten zu beeinträchtigen.
- **MyPy:** Dieses Tool überprüft statische Typen in Python, wodurch potenzielle Fehler und Bugs erkannt werden können, noch bevor das Programm startet.
- **Bootstrap:** Diese Style-Bibliothek wird verwendet, um das Frontend modern zu gestalten, ohne alle Styles manuell erstellen zu müssen.

## 5. Statische Typisierung

In diesem Abschnitt wird erklärt, wie Statische Typisierung dabei hilft, die Fehleranfälligkeit bei komplexen Berechnungen in der Anwendung zu minimieren.

### MyPy

MyPy ist ein statischer Typ-Prüfer für Python. Es erlaubt das Hinzufügen von Typ-Annotationen und prüft den Code vor der Ausführung, um sicherzustellen, dass keine falschen Datentypen (z. B. ein Text statt einer Zahl) in Berechnungen einfließen.

#### Vorteile

* **Frühe Fehlererkennung:** Logikfehler werden vor dem Starten der App gefunden.
* **Bessere Dokumentation:** Andere Entwickler sehen sofort, welche Daten die Methoden erwarten.
* **Sicheres Refactoring:** Wenn man die Struktur einer Klasse ändert, zeigt MyPy sofort alle Stellen im Code, die nun angepasst werden müssen.

#### Nachteile

* **Zusätzlicher Zeitaufwand:** Man muss mehr Code schreiben.
* **Lernkurve:** Bei komplexen Typen muss man sich tiefer mit der MyPy-Syntax auskennen.
* **Geringere Flexibilität:** Das Ändern von Variablentypen erfordert zusätzlichen Aufwand und kann bestimmte Programmieraufgaben erschweren.
* **Falsches Sicherheitsgefühl:** MyPy prüft nur den statischen Code, keine Fehler, die erst zur Laufzeit durch falsche User-Eingaben entstehen.

### Verwendung von MyPy in der Anwendung

Die Anwendung enthält Daten mit komplexen Beziehungen und Daten, die komplexe Berechnungen erfordern. `GoalRecord` ist mit einem `Player`, einer `Team` und einem `Competition` verknüpft. `StatsService` muss die Statistiken daraus in mehreren Schritten berechnen.

Beispiel für die Komplexität: Die Methode `get_team_stats(team_id, competition_id)` greift auf viele `GameStats` zu, die wiederum aus einzelnen `GoalRecord` und `CardRecord`-Objekten bestehen. Die Methode `get_competition_stats(competition_id)` berechnet wiederum die Statistiken für jedes `Team`, das an einem gemeinsamen `Competition` teilnimmt.

Wenn bei der Berechnung der Tordifferenz oder der Rangliste versehentlich `player_id` (string) anstelle `goals_for` (int) hinzugefügt wird, meldet **MyPy** diesen Fehler sofort, bevor das Programm überhaupt abstürzt. Ohne **MyPy** wäre dieser Fehler in der NoSQL-Datenbank **MongoDB** unbemerkt geblieben.