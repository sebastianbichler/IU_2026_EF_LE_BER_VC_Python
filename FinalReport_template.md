### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

# Project Abschlussbericht: [Name der App / Projektname]

## 1. Einleitung und Vision

### 1.1 Projektvision und Ziele

Beschreiben Sie hier die Kernidee Ihres Projekts (z. B. das Fischrestaurant "Pingaue" oder den Postdienst "FoxPost").
Welches Problem löst die App für wen?

### 1.2 Wissenschaftliche Herausforderung / Python-Spezifischer Aspekt

Erläutern Sie den technischen Fokus (z. B. GIL, AsyncIO, Memory Management). Warum ist dieses Thema für
Python-Entwickler relevant? Welche Analogie wird innerhalb des Projekt (Grundaufgabe) verwendet? Baut eine Geschichte (
z.B. viele Füchse, die mit dem Empfangen und Versenden von Paketen überfordert sind, modelliert Postämter,
Transportwege, ...)

### 1.3 Arbeitshypothese

Stellen Sie eine klare Hypothese auf, die im wissenschaftlichen Teil (Jupyter Notebook) untersucht wird. (Beispiel: "Die
Nutzung von Multiprocessing führt bei CPU-lastigen Berechnungen trotz GIL zu einer Beschleunigung von X%"). Verwendet
für die Datenentities die Domain eurer Aufgabe.

---

## 2. Requirements Engineering

### 2.1 Kontextdiagramm

Stellen Sie das System in seiner Umgebung dar. Welche externen Akteure (Nutzer, APIs, Datenbanken) interagieren mit der
App?

### 2.2 Funktionale Anforderungen

Listen Sie die Features auf, die das System erfüllen muss. Vergeben Sie IDs (z. B. REQ-01), um später Tests darauf
beziehen zu können.

### 2.3 Nicht-funktionale Anforderungen (Qualitätsanforderungen)

Definieren Sie Anforderungen an Performance, Sicherheit oder Usability basierend auf der ISO 25010.

### 2.4 Use-Case Modellierung

Beschreiben Sie die typischen Interaktionen der Nutzer mit dem System.

---

## 3. Architektur und Tech-Stack

### 3.1 Auswahl der Plattform (Begründung)

Warum wurde Streamlit, ein Jupyter Notebook oder eine klassische GUI gewählt? Begründen Sie die Entscheidung gegen
Alternativen.

### 3.2 Modularer Kern und Open-Closed Principle

Wie ist der "Core" der Anwendung aufgebaut? Dokumentieren Sie, wie die Geschäftslogik unabhängig von der Oberfläche (
Frontend) bleibt.

### 3.3 Technologie-Stack

Listen Sie alle verwendeten Pakete und Tools auf (z. B. PyMC, PyTensor, Pandas) und erläutern Sie deren Rolle.

---

## 4. Design und Modellierung (Die "Story")

### 4.1 Domänenmodell und UML-Klassendiagramm

Hier muss die "Geschichte" sichtbar werden. Welche Objekte (z. B. Fische, Füchse, Postämter) gibt es? Wie hängen sie
zusammen?

### 4.2 Verhaltensdiagramme: Activity- & State-Diagram

Zeigen Sie komplexe Abläufe (Aktivität) und die Lebenszyklen wichtiger Objekte (Zustand).

### 4.3 Interaktionsdiagramm: Sequence-Diagram

Wer ruft welche Methode bei wem auf? Dokumentieren Sie hier die Kommunikation zwischen den Objekten.

### 4.4 Design Patterns und Prinzipien

Welche Muster (z. B. Factory, Strategy, MVC) wurden implementiert? Begründen Sie den Einsatz von SOLID, DRY und
KISS, ... Verwenden Sie UML-Diagramme, um die Umsetzung zu verdeutlichen.

---

## 5. Wissenschaftliche Problemstellung (Jupyter Notebook)

### 5.1 Methodik der Untersuchung

Beschreiben Sie den Aufbau Ihres Versuchs im Notebook.(Forschungsfrage beantworten, Datenmodell)

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

Beschreiben Sie die Automatisierung (GitHub Actions, Befehlsreihenfolge, Prüfung der `requirements.txt`, project.toml).

---

## 7. Software-Qualität nach ISO 25010

### 7.1 Beurteilung der Produktqualität

Skalieren und bewerten Sie Ihre Software in Kategorien wie Wartbarkeit, Zuverlässigkeit und Benutzbarkeit.

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

---

## Anhang

- **README.md (Inhalt):** Setup-Anleitung, Python-Umgebung, Paketliste.

- **Glossar:** Definition der fachlichen Begriffe der "Story".

---
