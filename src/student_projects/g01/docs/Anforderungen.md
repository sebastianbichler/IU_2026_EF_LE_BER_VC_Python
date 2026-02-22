# Anforderungen – FoxExpress

Die folgenden Tabellen definieren die funktionalen und nicht-funktionalen Anforderungen an das System. Die Priorisierung erfolgt nach dem **MoSCoW-Prinzip** (Must, Should, Could, Won't).

### 1. Funktionale Anforderungen (Functional Requirements)

| ID | Priorität | Anforderung (Titel & Beschreibung) | Abnahmekriterien (Akzeptanztest) |
| :--- | :--- | :--- | :--- |
| **F-01** | 🟥 Must | **Kürzesten Weg berechnen (Dijkstra)**<br>Das System muss den kürzesten Pfad und die Gesamtkosten zwischen zwei gewählten Knoten berechnen. | 1. Eingabe von Start- und Zielknoten ist möglich.<br>2. Algorithmus gibt die korrekte Sequenz der Knoten und die Gesamtdistanz zurück.<br>3. Ergebnis stimmt mit Referenzwert überein. |
| **F-02** | 🟥 Must | **Benchmark-Funktion (Multi-Environment)**<br>Das System führt identische Routenberechnungen unter CPython, PyPy und Numba aus. | 1. Der Prozess startet und läuft auf allen drei Umgebungen fehlerfrei durch.<br>2. PyPy wird (da extern) erfolgreich über einen Subprozess angesprochen.<br>3. Numba nutzt den @jit(nopython=True) Modus. |
| **F-03** | 🟥 Must | **Zeitmessung & Vergleich**<br>Die Ausführungszeiten müssen gemessen, gespeichert und vergleichend dargestellt werden. | 1. Messung erfolgt präzise (z. B. mittels timeit).<br>2. Ein Balkendiagramm zeigt alle drei Werte (CPython, Numba, PyPy) nebeneinander.<br>3. Die schnellste Variante ist optisch erkennbar. |
| **F-04** | 🟧 Should | **Lieferungen verwalten**<br>Benutzer können Lieferaufträge mit Start- und Zielknoten anlegen und bearbeiten. | 1. Über ein Formular kann eine neue Lieferung erstellt werden.<br>2. Die Lieferung erscheint in einer Listenansicht/Tabelle in der GUI. |
| **F-05** | 🟧 Should | **Auswahl der Ausführungsumgebung**<br>Benutzer sollen auswählen können, ob ein Benchmark unter CPython, PyPy oder Numba ausgeführt wird. | 1. Checkboxen oder Dropdown ermöglichen die Auswahl (z. B. „Nur CPython vs. Numba“).<br>2. Der Benchmark führt nur die ausgewählten Umgebungen aus. |
| **F-06** | 🟨 Could | **Paketstatus-Tracking**<br>Verwaltung von Status wie Eingegangen, Unterwegs, Zugestellt. | 1. Der Status einer Lieferung kann in der GUI geändert werden.<br>2. Der aktuelle Status wird visuell angezeigt (z. B. durch Farben). |
| **F-07** | 🟨 Could | **Express-Zuschläge berechnen**<br>Berechnung zusätzlicher Kosten abhängig von der Gefährlichkeit der Route. | 1. Kanten im Graphen besitzen ein Attribut (z. B. danger_level).<br>2. Der Endpreis ist bei gefährlichen Routen höher als bei sicheren (Formel-Check). |
| **F-08** | 🟨 Could | **Empfänger-Präferenzen speichern**<br>Speicherung, ob Pakete versteckt oder persönlich übergeben werden sollen. | 1. Ein Datenfeld „Zustellart“ wird pro Lieferung gespeichert.<br>2. Die Information wird in der Lieferübersicht angezeigt. |
| **F-09** | 🟨 Could | **Interaktive Graph-Eingabe**<br>Benutzer können eigene Graphen definieren. | 1. Benutzer kann Knoten/Kanten hinzufügen (z. B. per Text-Input oder Klick).<br>2. Der Dijkstra-Algorithmus funktioniert auf dem neu erstellten Graphen korrekt. |
| **F-10** | 🟨 Could | **Export der Ergebnisse**<br>Export der Benchmark-Ergebnisse als Datei (z. B. CSV). | 1. Ein Button „Download CSV“ ist verfügbar.<br>2. Die Datei enthält die korrekten Messwerte und Spaltenüberschriften. |

### 2. Nicht-Funktionale Anforderungen (Quality Requirements)

Diese Anforderungen definieren die Qualitätsmerkmale des Systems.

| ID | Kategorie | Anforderung | Abnahmekriterien |
| :--- | :--- | :--- | :--- |
| **NFA-01** | Performance | **Reaktivität der GUI** | Die Streamlit-Oberfläche friert während der Benchmark-Berechnung nicht dauerhaft ein (Nutzer erhält visuelles Feedback, z. B. Ladebalken). |
| **NFA-02** | Interoperabilität | **PyPy Integration** | Die Hauptanwendung (CPython) kann erfolgreich einen externen Subprozess für PyPy starten und dessen Rückgabewert lesen. |
| **NFA-03** | Usability | **Verständlichkeit** | Die Ergebnisse (Diagramme) sind klar beschriftet (Achsen, Einheiten in ms/s), sodass sie ohne Erklärung verständlich sind. |
| **NFA-04** | Reproduzierbarkeit | **Reproduzierbarkeit** | Gleiche Eingaben sollen zu vergleichbaren Messergebnissen führen. |
