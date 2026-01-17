### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---
Das siebte Thema führt uns weg von der deterministischen Programmierung („Wenn X, dann Y“) hin zur Modellierung von
Unsicherheit. Während C# hervorragend für regelbasierte Geschäftlogik ist, hat sich Python als Weltsprache für die *
*Probabilistische Programmierung (PP)** etabliert. Hier programmieren wir keine festen Werte, sondern *
*Wahrscheinlichkeitsverteilungen**.

---

# Thema 7: Probabilistische Programmierung & Statistische Modellierung

### 1. Einleitung & Kontext

In der klassischen Softwareentwicklung ist ein Wert entweder `true` oder `false`, `5` oder `10`. In der Realität – und
besonders in unserem Projekt **Elephant Memory Cloud** – haben wir es oft mit unvollständigen Daten oder Rauschen zu
tun.

**Probabilistische Programmierung** erlaubt es uns:

1. Vorwissen (Priors) in ein Modell einfließen zu lassen.
2. Beobachtete Daten zu nutzen, um dieses Wissen zu aktualisieren (Bayesian Inference).
3. Nicht nur eine Vorhersage zu treffen, sondern auch die **Unsicherheit** dieser Vorhersage zu quantifizieren.

In Python nutzen wir hierfür Frameworks wie **PyMC**, **Pyro** oder **Bambi**. Diese Tools nutzen im Hintergrund
komplexe Algorithmen wie MCMC (Markov Chain Monte Carlo), um den Lösungsraum abzutasten.

---

### 2. Wissenschaftliche Fragestellung

> *"Quantifizierung von Vorhersage-Unsicherheiten in biologischen Migrationsmustern: Eine vergleichende Analyse von
Frequentist-Regressionsmodellen gegenüber Bayes'schen hierarchischen Modellen mittels MCMC-Sampling."*

**Kernfokus:** Wie viel zuverlässiger sind unsere Vorhersagen über den Aufenthaltsort eines Elefanten, wenn wir die
Varianz der Sensoren und das Vorwissen über die Herde statistisch korrekt modellieren?

---

### 3. Wissenschaftlicher Hintergrund

**Publikation:** *Probabilistic programming in Python using PyMC3* (Salvatier et al., 2016) oder *Bayesian Methods for
Hackers* (Cameron Davidson-Pilon).

Die Forschung zeigt, dass Bayes'sche Methoden besonders bei **kleinen Datensätzen** (Small Data) überlegen sind, da sie
durch "Priors" (Vorwissen) verhindern, dass das Modell überreagiert (Overfitting). Während Deep Learning (C# ML.NET oder
PyTorch) oft Millionen Datenpunkte braucht, kommt PP oft mit wenigen, aber qualitativ hochwertigen Beobachtungen aus.

---

### 4. Code-Demonstration (Notebook-Stil)

Stellen wir uns vor, wir wollen die Wahrscheinlichkeit schätzen, dass ein Elefant krank ist, basierend auf seiner
Bewegungsgeschwindigkeit.

#### Schritt 1: Installation & Setup

```python
# !pip install pymc arviz
import pymc as pm
import arviz as az
import numpy as np
import matplotlib.pyplot as plt

# Simulierte Daten: Geschwindigkeit von 20 Elefanten (in km/h)
# Wir wissen: Gesunde Elefanten laufen ca. 5 km/h, kranke langsamer.
data = np.array([4.8, 5.2, 3.1, 4.9, 5.0, 2.8, 5.1, 4.7, 3.2, 5.0])

```

#### Schritt 2: Das Bayes'sche Modell definieren

Wir definieren unsere Annahmen als Wahrscheinlichkeitsverteilungen.

```python
with pm.Model() as elephant_model:
    # Prior: Wir glauben, die Durchschnittsgeschwindigkeit liegt bei 4 km/h
    mu = pm.Normal("mu", mu=4.0, sigma=2.0)

    # Prior für die Standardabweichung (wie stark schwankt das Tempo?)
    sigma = pm.HalfNormal("sigma", sigma=1.0)

    # Likelihood: Wie wahrscheinlich sind die beobachteten Daten gegeben mu und sigma?
    obs = pm.Normal("obs", mu=mu, sigma=sigma, observed=data)

    # Inference: Den "Lösungsraum" mit MCMC abtasten
    trace = pm.sample(1000, return_inferencedata=True)

```

#### Schritt 3: Analyse der Ergebnisse

```python
# Ergebnisse visualisieren
az.plot_posterior(trace, var_names=["mu"])
plt.show()

# Unsicherheit anzeigen
summary = az.summary(trace, round_to=2)
print(summary)

```

*Ergebnis:* Wir erhalten keinen einzelnen Wert für die Geschwindigkeit, sondern eine Verteilung (z. B. 4.5 km/h mit
einem 95% Konfidenzintervall).

---

### 5. Zusammenfassung für die Folien

| Merkmal                 | Deterministisch (C# / Standard Python) | Probabilistisch (PyMC)                  |
|-------------------------|----------------------------------------|-----------------------------------------|
| **Output**              | Ein fester Wert (Punkt-Schätzung)      | Eine Verteilung (Wahrscheinlichkeiten)  |
| **Logik**               | Fest codierte Regeln                   | Statistische Inferenz                   |
| **Umgang mit Rauschen** | Oft problematisch (Ausreißer stören)   | Integriert (Unsicherheit wird sichtbar) |
| **Anwendung**           | Business Logic, Web-Backend            | Wissenschaft, KI, Risikoanalyse         |

---

### Anwendung im Projekt "Elephant Memory Cloud"

In unserem Archiv speichern wir GPS-Punkte. Wenn ein Sensor für 2 Stunden ausfällt:

* **Klassisch:** Wir ziehen eine gerade Linie (oft falsch).
* **Probabilistisch:** Wir berechnen eine "Wahrscheinlichkeitswolke". Wir wissen, wo der Elefant *wahrscheinlich* war,
  basierend auf seinem vorherigen Tempo und dem Gelände. Wir geben dem Nutzer nicht nur einen Punkt, sondern einen
  Radius der Gewissheit.

> **Merksatz für Studierende:** "In der Probabilistischen Programmierung gestehen wir ein, dass wir nicht alles wissen.
> Das Modell sagt uns nicht 'Der Elefant ist dort', sondern 'Ich bin mir zu 80% sicher, dass er in diesem 1km-Radius
> ist'."

---
