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
