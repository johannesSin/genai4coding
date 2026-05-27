# GenAI4Coding
Evaluierung moderner Large Language Models anhand algorithmischer Benchmarks und Webanwendungen.

Dieses Repository enthält sämtliche Benchmarks, Analyse-Skripte, generierten Lösungen und Auswertungen der Bachelorarbeit „GenAI4Coding“.

## Ziel

Neuevaluierung der Codegenerierungsfähigkeiten moderner generativer KI-Systeme anhand von algorithmischen Programmieraufgaben sowie der Generierung einer vollständigen Softwareanwendung.

---

## Teil 1: Advent of Code Benchmark

Im ersten Teil der Arbeit werden generative KI-Systeme anhand von Aufgaben aus **Advent of Code 2025 (Tage 1–12)** evaluiert. 

### Vorgehen

* Für jeden Tag werden **Part 1 und Part 2** getrennt gelöst
* Einheitlicher Prompt für alle Modelle
* Einheitliche Programmiersprache (Python)
* Automatische Ausführung und Bewertung mittels Benchmark-Skript

### Modelle

* GPT-5.3
* Claude Sonnet
* Gemini 3.1 Pro

### Bewertungskriterien

* Korrektheit der Lösung
* Auftretende Fehlertypen (z. B. Runtime Errors, falsche Ergebnisse, fehlende Abhängigkeiten)
* Stabilität und Konsistenz

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

Die generierten Anwendungen werden automatisiert getestet anhand von:

* Funktionale Vollständigkeit (Register, Login, Dashboard, Transfer)
* Korrektheit der implementierten Funktionen
* Sicherheitsaspekte (Authentifizierung, Eingabevalidierung, Zugriffsschutz)
* Stabilität der Anwendung (Startfähigkeit, Fehlerverhalten)

Zusätzlich erfolgt eine strukturelle Analyse:

* Modularität und Projektstruktur
* Vorhandensein relevanter Komponenten (z. B. Datenbank, Routen, Templates)

---

## Projektstruktur

```text
aoc/
├── tasks/          # Input, Expected Outputs, Prompts
├── solutions/      # Generierter Code pro Modell
├── results/        # Benchmark-Ergebnisse
└── run_benchmark.py

banking_app/
├── gpt/
├── claude/
├── gemini/
├── prompt/
├── tests/          # Automatisierte Funktionstests
└── results/        # Gesamt-Ergebnisse (CSV)

README.md
```

---

## Methodik

* Einheitliche Prompts für alle Modelle
* Reproduzierbare Testumgebung
* Automatisierte Benchmark-Pipeline
* Vergleich zwischen mehreren KI-Systemen
* Kombination aus funktionalen Tests und struktureller Analyse

---

## Ausführung

### Advent of Code Benchmark

```bash
cd aoc
python3 run_benchmark.py
```

### Banking App Benchmark

```bash
python3 banking_app/tests/benchmark_banking.py <model>
python3 banking_app/tests/check_structure.py <model>
```

Beispiel:

```bash
python3 banking_app/tests/benchmark_banking.py gpt
```

---

## Ergebnisse

Die Ergebnisse werden automatisch gespeichert in:

```text
banking_app/results/banking_structure_results.csv
banking_app/results/banking_benchmark_results.csv
```
### Ergebnisse automatisch analysieren

```bash
python3 banking_app/results/analyze_banking_results.py
```

## Hinweis

Dieses Repository wurde im Rahmen einer Bachelorarbeit an der Paris-Lodron-Universität Salzburg erstellt.

## License

This project is licensed under the MIT License.
