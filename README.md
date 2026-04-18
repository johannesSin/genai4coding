# Bachelorarbeit – KI Codegenerierung

## Ziel

Neuevaluierung der Codegenerierungsfähigkeiten moderner generativer KI-Systeme anhand von Advent-of-Code-Aufgaben.

## Modelle

* GPT-5.3
* Claude Sonnet
* Gemini 3.1 Pro

## Struktur

```
tasks/        # Input + Expected Outputs + Prompts
solutions/    # Generierter Code pro Modell
results/      # Benchmark-Ergebnisse (CSV)
run_benchmark.py
```

## Methodik

* Einheitlicher Prompt für alle Modelle
* Einheitliche Programmiersprache (Python)
* Automatische Ausführung und Bewertung
* Vergleich anhand von:

  * Korrektheit
  * Fehlertypen
  * Stabilität

## Ausführung

```
python3 run_benchmark.py
```

## Ergebnisse

Werden automatisch gespeichert in:

```
results/benchmark_results.csv
```
