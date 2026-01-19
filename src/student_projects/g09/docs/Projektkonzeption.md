# Projektkonzeption: Sloth’s Slow-Motion Hotel

## 1. Einleitung und Zweck der Anwendung
Das Projektziel ist die Entwicklung einer spezialisierten Hotel-Management-Software für **"Sid Sloth"**, einen Hotelmanager, der ein Luxus-Resort für Faultiere betreibt.

Anders als bei herkömmlicher Hotelsoftware, bei der Effizienz und Schnelligkeit im Vordergrund stehen, ist der **Zweck dieser Anwendung die Maximierung der Langsamkeit**. Die Software soll Sid dabei unterstützen, die philosophischen Grundsätze des Resorts technisch durchzusetzen: Entschleunigung, Ruhe und minimale Bewegung.

Die Applikation dient als Verwaltungszentrale für:
- Langzeit-Buchungen (Hängematten).
- Die Berechnung von Rabatten basierend auf Inaktivität (Bewegungs-Tracker).
- Die kulinarische Versorgung mit exakt gereiften Blättern.
- Einen Weckservice, der die Ruhe der Gäste respektiert (durch absichtliche Verzögerung).

## 2. Wissenschaftlicher Fokus (Python vs. Science)
Im Rahmen des Moduls *DLBDSIPWP01* wird in diesem Projekt ein spezifischer wissenschaftlicher Schwerpunkt auf **Software-Architektur** gelegt.

* **Topic:** Structural Design Patterns (Fokus auf Flexibilität).
* **Konkrete Umsetzung:** Implementierung des **State Patterns** (Verhaltensmuster).
* **Ziel:** Die verschiedenen Phasen der "Langsamkeit" eines Gastes (z.B. *Schlafen, Ruhen, Langsames Essen*) sollen sauber modelliert werden. Das System muss erkennen, dass ein Gast im Zustand "Schlafen" beispielsweise nicht essen kann.
* **Duck Typing:** Es wird Python-typisches "Duck Typing" verwendet, um flexible Schnittstellen für verschiedene Arten von "faulen Objekten" zu ermöglichen, ohne strikte Vererbungshierarchien zu erzwingen.

---

## 3. Funktionale Anforderungen (Functional Requirements)
Da der Code in Englisch verfasst wird, werden die Requirements hier bereits mit englischen IDs definiert, um die Zuordnung im Code (als Kommentare/Docstrings) zu erleichtern.

### 3.1 Hängematten-Management (Booking)
Das System muss Buchungen verwalten, die der extremen Faulheit der Gäste entsprechen.
- **REQ-FUN-001 (Min Duration):** Eine Buchung muss für mindestens 7 Tage erfolgen. Kürzere Aufenthalte sind zu stressig und werden vom System abgelehnt.
- **REQ-FUN-002 (Availability):** Das System muss prüfen, ob eine Hängematte im gewünschten Zeitraum frei ist.

### 3.2 Bewegungs-Tracker (Incentives)
Das System belohnt Faulheit monetär.
- **REQ-FUN-003 (Step Input):** Der User (Sid) kann die täglichen Schritte eines Gastes eingeben.
- **REQ-FUN-004 (Inverse Discount):** Je weniger Schritte, desto höher der Rabatt.
    - *Zielwert:* Nahe 0 Schritte = Maximaler Rabatt.
    - *Logik:* Hohe Schrittzahl = Geringer/Kein Rabatt (Strafe für Hektik).

### 3.3 Menüplan (Leaf Gourmet)
Verwaltung der Nahrungsmittel basierend auf Zeit.
- **REQ-FUN-005 (Maturity Calc):** Berechnung der Reifezeit von Blättern. Das System darf Blätter nur freigeben, wenn sie den Status "perfekt gereift" erreicht haben.

### 3.4 Weckruf-Service (Wake-Up)
Ein Wecker, der nicht stresst.
- **REQ-FUN-006 (Delayed Alarm):** Wenn ein Gast um Zeit $t$ geweckt werden möchte, darf der Alarm frühestens um $t + 3$ Stunden ausgelöst werden. Das System muss diese Verzögerung automatisch addieren.

### 3.5 Zustands-Management (State Pattern)
- **REQ-FUN-007 (Guest States):** Ein Gast muss immer einen definierten Zustand haben.
    - *States:* `Sleeping`, `Resting`, `Eating`.
- **REQ-FUN-008 (State Transition):** Der Gast kann den Zustand wechseln (z.B. von *Sleeping* zu *Resting*), aber unlogische Wechsel (z.B. *Sleeping* zu *Eating*) müssen behandelt oder blockiert werden.

---

## 4. Nicht-Funktionale Anforderungen (NFR)
Diese Anforderungen definieren die Qualität und technische Umgebung des Projekts.

- **REQ-NFR-001 (Language):** Der gesamte Quellcode (Variablennamen, Funktionen, Klassen) sowie Kommentare müssen in **Englisch** verfasst sein.
- **REQ-NFR-002 (Documentation):** Der Code muss mittels Docstrings und einer README.md dokumentiert sein.
- **REQ-NFR-003 (Testing):** Es müssen Unit-Tests und mindestens 3 Integrationstests implementiert werden.
- **REQ-NFR-004 (CI/CD):** Der Build- und Testprozess muss über eine dokumentierte Pipeline-Logik (Simulation oder `requirements.txt` + Test-Skript) nachvollziehbar sein.
- **REQ-NFR-005 (Architecture):** Der Code muss objektorientiert (OOP) aufgebaut sein und die Trennung der Verantwortlichkeiten (Separation of Concerns) beachten.

---

## 5. System-Akteure (Use Case Analyse)
- **Akteur 1: Sid Sloth (Manager)**
    - Erfasst Buchungen.
    - Gibt Schrittdaten in den Tracker ein.
    - Prüft den Menüplan.
    - Setzt Weckzeiten.
- **Akteur 2: Sloth Guest (System-Objekt)**
    - Hat einen Zustand (State).
    - Hat eine Rechnung (Preis minus Faulheits-Rabatt).
