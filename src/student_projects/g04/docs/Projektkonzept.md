# Foorball League

## 1. Aufgabenstellung

Die Anwendung "Football League" wird als zentrales Informationsportal für Fußballfans dienen. Der Zweck besteht darin, den Nutzern einen schnellen Zugriff auf eine übersichtliche Darstellung des Spielplans und der Spielergebnisse zu ermöglichen.

## 2. Anforderungen

### 2.1 Funktionale Anforderungen

| ID  | Beschreibung | Priorität |
| :-: | ------------ | :-------: |
| FK1 | Turnierverwaltung: Auflistung aller verfügbaren Turniere. | Muss |
| FK2 | Teamverwaltung: Erfassen von Namen, Positionen und Trikotnummern. | Muss |
| FK3 | Ergebnis-Erfassung: Protokollierung von Toren, Karten und Torschützen während eines Spiels. | Muss |
| FK4 | Tabellenberechnung: Automatische Berechnung der Punkte und Ranglisten pro Turnier. | Muss |
| FK5 | Spielplan-Logik: Automatische Erstellung von Hin- und Rückrunden sowie Terminen. | Könnte |
| FK6 | Finanzen: Tracking von Einnahmen (Tickets) und Ausgaben (Miete, Schiedsrichter). | Könnte |
| FK7 | Spieler-Statistiken: Visualisierung der besten Spieler und Fairplay-Wertungen. | Könnte |

### 2.2 Nicht-funktionale Anforderungen

* **Typ-Sicherheit:** Alle mathematischen Operationen müssen durch **MyPy** strikt typisiert sein, um Rechenfehler zu verhindern.
* **Performance:** Schnelle Ladezeiten der Spieldaten durch effiziente MongoDB-Abfragen.
* **Skalierbarkeit:** Das Schema in MongoDB sollte flexibel genug sein, um später zusätzliche Statistiken hinzufügen zu können.
* **Wartbarkeit:** Der Code muss modular aufgebaut sein, damit neue Funktionen ohne große Umstrukturierung des Kernsystems hinzugefügt werden können. 

## 3. Use-Cases

| ID  | Name | Beschreibung |
| :-: | ---- | ------------ |
| UC1 | Turnier auswählen | User navigiert durch die Liste der verfügbaren Turniere. |
| UC2 | Spieldetails einsehen | User klickt auf einen Turnier und sieht die Tabelle der anstehenden/beendeten Spiele. |
| UC3 | Spielergebnisse prüfen | User vergleicht Scores und Spieldaten in der Detailansicht. |
| UC4 | Teamdetails einsehen | User klickt auf eine Team und sieht alle Spieler mit Positionen und Trikotnummern. |

## 4. Tech-Stack

* **Backend:** Flask
* **Frontend:** Bootstrap 5.3
* **Datenbank:** MongoDB
* **DB-Anbindung:** PyMongo
* **Type-Checker:** MyPy

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