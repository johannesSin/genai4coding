# GenAI4Coding

Evaluierung moderner Large Language Models anhand algorithmischer Benchmarks und Webanwendungen.

Dieses Repository enthält sämtliche Benchmarks, Analyse-Skripte, generierten Lösungen sowie Auswertungen der Bachelorarbeit **„GenAI4Coding“**. Ziel der Arbeit ist die systematische Evaluierung moderner Large Language Models (LLMs) hinsichtlich ihrer Fähigkeiten zur automatisierten Codegenerierung anhand algorithmischer Programmieraufgaben sowie der Entwicklung einer vollständigen Webanwendung.

## Ziel

Neuevaluierung der Codegenerierungsfähigkeiten moderner generativer KI-Systeme anhand von algorithmischen Programmieraufgaben sowie der Generierung einer vollständigen Softwareanwendung.

---

## Teil 1: Advent of Code Benchmark

Im ersten Teil der Arbeit werden generative KI-Systeme anhand von Aufgaben aus **Advent of Code 2025 (Tage 1–12)** evaluiert.

### Vorgehen

* Für jeden Tag werden **Part 1 und Part 2** getrennt gelöst.
* Einheitlicher Prompt für alle Modelle.
* Einheitliche Programmiersprache (Python).
* Automatische Ausführung und Bewertung mittels Benchmark-Skript.
* Bei funktional falschen Ergebnissen erfolgt ein einmaliger zweiter Versuch mit unverändertem Prompt.

### Modelle

Die Evaluation wurde über die offiziellen Weboberflächen der jeweiligen Anbieter durchgeführt.

* OpenAI – GPT-5.3
* Anthropic – Claude Sonnet
* Google – Gemini 3.1 Pro

Für alle Modelle wurden identische Prompts und identische Eingabedaten verwendet. Da die Weboberflächen keine Informationen über Modell-Snapshots oder Build-Versionen bereitstellen, beziehen sich die Ergebnisse auf die zum Zeitpunkt der Evaluation verfügbaren Modellversionen.

### Bewertungskriterien

* Korrektheit der Lösung
* Auftretende Fehlertypen (z. B. Timeouts, Runtime Errors, falsche Ergebnisse)
* Stabilität und Konsistenz
* Erfolgsrate
* Vergleich zwischen Part 1 und Part 2

---

## Teil 2: Internet-Banking-Anwendung

Im zweiten Teil wird untersucht, inwieweit generative KI-Systeme in der Lage sind, eine vollständige Softwareanwendung zu entwickeln.

### Ziel

Entwicklung einer prototypischen Internet-Banking-Webanwendung mit:

* Benutzerregistrierung und Login
* Kontenübersicht
* Transaktionshistorie
* Überweisungen zwischen Konten

### Technologie

* Python
* FastAPI (Backend)
* SQLite (Datenbank)

### Evaluation

Die generierten Anwendungen werden mithilfe eines automatisierten Benchmark-Frameworks evaluiert. Da die Modelle unterschiedliche Softwarearchitekturen erzeugen, erfolgt die technische Kommunikation über modellspezifische Adapter. Die fachlichen Testfälle und Bewertungskriterien bleiben dabei für alle Modelle identisch.

Der funktionale Benchmark umfasst unter anderem folgende Testfälle:

* Erreichbarkeit der Anwendung
* Registrierung neuer Benutzer
* Login
* Zugriff auf geschützte Bereiche
* Überweisungsfunktion
* Login mit ungültigen Zugangsdaten
* Überweisung ohne Authentifizierung
* Ablehnung negativer Überweisungsbeträge
* Schutz gegen SQL-Injection

Zusätzlich erfolgt eine strukturelle Analyse der generierten Anwendungen hinsichtlich:

* Modularität und Projektstruktur
* Vorhandensein relevanter Komponenten (z. B. Datenbank, Routen, Templates)
* Qualität der Softwarestruktur
* Manueller Nachbearbeitungsaufwand

---

## Projektstruktur

```text
aoc/
├── tasks/          # Input-Dateien, erwartete Ergebnisse und Prompts
├── solutions/      # Generierter Code pro Modell
├── results/        # Benchmark-Ergebnisse und Analysen
└── run_benchmark.py

banking_app/
├── gpt/
├── claude/
├── gemini/
├── prompt/
├── tests/          # Automatisierter Banking-Benchmark und Strukturanalyse
└── results/        # CSV-Ergebnisse und Analyse-Skripte

README.md
```

---

## Methodik

* Einheitliche Prompts für alle Modelle
* Identische Eingabedaten für sämtliche Experimente
* Durchführung über die offiziellen Weboberflächen der Anbieter
* Reproduzierbare Testumgebung
* Automatisierte Benchmark-Pipeline
* Einheitlicher Testkatalog mit elf funktionalen und sicherheitsbezogenen Testfällen
* Modellspezifische Adapter für unterschiedliche technische Architekturen bei identischen fachlichen Bewertungskriterien
* Vergleich zwischen mehreren KI-Systemen
* Kombination aus funktionalen Tests, Sicherheitsanalyse und struktureller Bewertung
* Keine modellabhängigen Prompt-Anpassungen oder Folgeprompts

---

## Ausführung

### Advent of Code Benchmark

```bash
cd aoc
python3 run_benchmark.py
```

### Banking App Benchmark

Funktionaler Benchmark:

```bash
python3 banking_app/tests/benchmark_banking.py <model>
```

Strukturanalyse:

```bash
python3 banking_app/tests/check_structure.py <model>
```

Beispiel:

```bash
python3 banking_app/tests/benchmark_banking.py gpt
```

---

## Ergebnisse

Die Benchmark-Pipeline protokolliert unter anderem:

* HTTP-Statuscodes
* Weiterleitungen
* Testergebnisse
* Fehlermeldungen
* Sicherheitsprüfungen
* Ergebnisse der Strukturanalyse

Die Ergebnisse werden automatisch gespeichert in:

```text
banking_app/results/banking_benchmark_results.csv
banking_app/results/banking_structure_results.csv
```

### Ergebnisse automatisch analysieren

```bash
python3 banking_app/results/analyze_banking_results.py
```

Die Analyse erzeugt aggregierte Auswertungen der funktionalen Tests sowie der strukturellen Bewertung und dient als Grundlage für Tabellen, Diagramme und statistische Auswertungen der Bachelorarbeit.

---

## Hinweis

Dieses Repository wurde im Rahmen einer Bachelorarbeit an der **Paris-Lodron-Universität Salzburg** erstellt.

Die Experimente wurden unter reproduzierbaren Bedingungen durchgeführt. Alle Modelle erhielten identische Prompts und identische Eingabedaten. Die Evaluation erfolgte über die offiziellen Weboberflächen von OpenAI, Anthropic und Google. Da diese keine festen Modell-Snapshots oder konfigurierbaren Modellparameter (z. B. Temperatur oder Top-p) bereitstellen, beziehen sich die Ergebnisse auf die zum Zeitpunkt der Experimente verfügbaren Modellversionen.

---

## License

This project is licensed under the MIT License.