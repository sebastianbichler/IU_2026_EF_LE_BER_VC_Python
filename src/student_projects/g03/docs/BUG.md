# Bugs

- Nach dem Erstellen eines Kunden wird keine Abo-Kiste erstellt (Fix erforderlich)
- Zeiten werden falsch angezeigt (Formatfehler) — Fix erforderlich
- Gemüse wird in der Lagerverwaltung direkt als „abgelaufen“ markiert, obwohl noch ca. 10 Tage Haltbarkeit vorhanden sind
- Bei Bestellungen können aktuell nicht mehrere Sorten ausgewählt werden (Orders)
- jup. diagramm zeigt ein fehler

# DATETIME
in main.py strftime von %Y-%m-%d auf %d.%m.%Y geändert Zeilen: 215,216, 245-249 und 444 Bug ist somit gefixt
in models.py Zeile 57 auch strftime vorhanden

# ABOKISTEN
der Turnus ist hier entscheidend - es ist aus dem Programm heraus zu erkennen wann der Kunde eine Abokiste erhält main.py Line 465 angepasst damit klarer ist, was man eingeben soll.

Neuer BUG: keine Auswahl des Gemüses möglich
