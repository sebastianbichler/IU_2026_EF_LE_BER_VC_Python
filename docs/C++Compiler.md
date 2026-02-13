### DLBDSIPWP01 - Einführung in die Programmierung mit Python (Projekt)

---

## C++ Compiler

Um einen C++-Compiler zu verwenden, wird Anaconda nicht benötigt. Anaconda ist primär eine
Distribution für Python und R, die vor allem im Data-Science-Bereich eingesetzt wird.

Man *kann* zwar über Anaconda C++-Compiler (wie `gcc` oder `clang`) in isolierten Umgebungen installieren, aber für die
klassische C++-Entwicklung ist das eher ein ungewöhnlicher Umweg.

Hier ist der Überblick, wie „nativ“ und ohne Ballast ein C++-Compiler verwendet werden kann:

---

### 1. Die Standard-Wege je nach Betriebssystem

Je nachdem, welches System genutzt wird, gibt es bewährte Standard-Lösungen:

* **Windows:**
* **Visual Studio (Community Edition):** Das ist das Rundum-sorglos-Paket von Microsoft. Beim Installer muss
  lediglich der Haken bei „Desktopentwicklung mit C++“ gesetzt werden. Damit erhältst du den **MSVC**-Compiler.
* **MSYS2 / MinGW-w64:** Wenn der klassische **GCC** (Linux-Style) auf Windows gennutzt werden soll. Das ist oft die
  Wahl, wenn man mit VS Code arbeitet.


* **macOS:**
* Hier ist es am einfachsten: Tippe im Terminal `xcode-select --install`. Das installiert die Command Line
  Tools inklusive des **Clang**-Compilers.


* **Linux:**
* Meistens ist er schon da. Wenn nicht: `sudo apt install build-essential` (unter Ubuntu/Debian) installiert alles, was
  gebraucht wird (GCC, g++, make).

---

### 2. Warum Anaconda für C++ oft eher hinderlich ist

Anaconda verwaltet eigene Bibliotheken und Pfade. Wenn C++ über Conda installiert wird, kann es passieren, dass:

1. **Pfad-Konflikte** entstehen, wenn gleichzeitig andere Compiler auf dem System vorhanden sind.
2. Unnötig viel **Speicherplatz** verbraucht wird (Anaconda ist recht groß).
3. Die Integration in IDEs wie CLion oder Visual Studio komplizierter wird, weil diese die Compiler in den
   Standardverzeichnissen suchen.

---

### 3. Was stattdessen gebraucht wird (Das Duo)

Um produktiv zu sein, werden meistens zwei Dinge benötigt:

1. **Den Compiler:** (Das Werkzeug, das den Code übersetzt, z. B. GCC, Clang oder MSVC).
2. **Eine IDE oder einen Editor:** * **Visual Studio:** Compiler und Editor in einem.

* **VS Code:** Nur ein Editor, der Compiler muss separat installieren und über die C++-Extension verknüpft werden.

---

Da hast du völlig recht: Dein Student hat zwar einen „wahren Kern“ in seiner Aussage, wirft aber Paketmanagement,
Kompiler-Anforderungen und Entwicklungsumgebungen (IDEs) in einen Topf.

Hier ist die Klarstellung, damit du das Projekt sauber aufsetzen kannst, ohne den „Anaconda-Ballast“ mitzuschleppen:

---

### 4. Braucht PyMC einen C++-Compiler?

Ja, PyMC benötigt im Hintergrund einen C++-Compiler.

* **Der Grund:** PyMC nutzt heute **PyTensor** (früher Aesara/Theano) als mathematisches Backend. Um die
  probabilistischen Modelle effizient zu berechnen, wird der Python-Code in optimierten C++-Code übersetzt und
  kompiliert.
* **Die Lösung:** Dafür muss nicht Anaconda installiert werden. Es reicht, wenn ein funktionsfähiger C++-Compiler auf
  dem System ist:
* **Windows:** Die *Build Tools für Visual Studio* (MSVC) sind der Standard. Alternativ kann auch `gcc` über MSYS2
  installiert werden.
* **Linux:** `gcc` oder `clang`.
* **macOS:** Die *Xcode Command Line Tools*.

MSYS2 heißt „Minimal SYStem 2“ und ist eine leichtgewichtige Umgebung, die es ermöglicht, viele Linux-Tools
(inklusive `gcc`) unter Windows zu nutzen, ohne gleich Anaconda installieren zu müssen.

### 2. Ist Anaconda zwingend erforderlich? (Nein!)

Anaconda ist lediglich eine **Distribution** und ein **Paketmanager** (`conda`). Es ist keine IDE wie PyCharm oder
Visual Studio.

Empfehlungen für Anaconde werden gegeben, weil PyMC über `conda` sehr einfach zu installieren ist, da `conda` den
C++-Compiler und die mathematischen Bibliotheken (wie BLAS/LAPACK) automatisch in die virtuelle Umgebung mitinstalliert.

**Die Alternativen für den Workflow:**
Wenn GitHub mit PyCharm oder Visual Studio gennutzt wird, gibt es zwei saubere Wege:

| Weg               | Beschreibung                                                                                    | Fazit                                                                                    |
|-------------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| **venv + pip**    | Klassischer Python-Weg. Du musst den C++-Compiler (MSVC) manuell unter Windows vorinstallieren. | Schlank, aber die Konfiguration der Pfade für PyTensor kann unter Windows knifflig sein. |
| **Conda / Mamba** | Du nutzt nur den Paketmanager (z.B. **Miniconda** oder das schnellere **Micromamba**).          | Installiert den Compiler isoliert nur für dieses Projekt mit. Sehr stabil für PyMC.      |

---

### 3. PyMC in PyCharm oder Visual Studio einbinden

Egal für welchen Paketmanager man sich entscheidet: **Sowohl PyCharm als auch Visual Studio können jede Python-Umgebung
nutzen.**

1. Erstelle die Umgebung (egal ob per `pip` oder `conda`).
2. Wähle in PyCharm unter *Settings -> Project Interpreter* einfach diese Umgebung aus.
3. PyMC „weiß“ dann über die Umgebungsvariablen, wo sein Compiler liegt.

### 4. Einordnung der „Probabilistischen Optimierung“

PyMC verwendet rechenintensive Algorithmen wie **NUTS (No-U-Turn Sampler)**. Diese profitieren massiv von der
Kompilierung. Ohne Compiler würde PyMC entweder gar nicht laufen oder quälend langsam sein.

---

### 5. Vorschlag für ein Setup:

Statt das riesige Anaconda zu installieren, nutzt **Miniconda** oder **Micromamba**. Damit erstellt ihr eine minimale
Umgebung nur für PyMC. Das lässt sich auch in einer `environment.yml` im GitHub-Repo dokumentieren, sodass
jeder im Team die gleiche Umgebung mit einem Befehl replizieren kann.
