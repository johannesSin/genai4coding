# Bachelorarbeit – KI Codegenerierung

## Ziel

Neuevaluierung der Codegenerierungsfähigkeiten moderner generativer KI-Systeme anhand von algorithmischen Programmieraufgaben sowie der Generierung einer vollständigen Softwareanwendung.

---

## Teil 1: Advent of Code Benchmark

Im ersten Teil der Arbeit werden generative KI-Systeme anhand von Aufgaben aus **Advent of Code 2025 (Tage 1–12)** evaluiert.

### Vorgehen

* Für jeden Tag werden **Part 1 und Part 2** getrennt gelöst
* Einheitlicher Prompt für alle Modelle
* Einheitliche Programmiersprache (Python)
* Automatische Ausführung und Bewertung

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

### Fokus

* Vollständigkeit der Anwendung
* Codequalität und Struktur
* Funktionsfähigkeit
* Sicherheitsaspekte

---

## Projektstruktur

```text
tasks/         # Advent of Code: Input, Expected Outputs, Prompts
solutions/     # Generierter Code pro Modell
results/       # Benchmark-Ergebnisse (CSV)
banking_app/   # Generierte Banking-Anwendung pro Modell
run_benchmark.py
```

---

## Methodik

* Einheitlicher Prompt pro Aufgabe
* Reproduzierbare Ausführung
* Automatische Benchmark-Pipeline
* Vergleich zwischen mehreren KI-Systemen

---

## Ausführung

```bash
python3 run_benchmark.py
```

---

## Ergebnisse

Werden automatisch gespeichert in:

```text
results/benchmark_results.csv
```
