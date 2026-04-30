# SecureBank – Prototypische Internet-Banking-Webanwendung

Eine vollständige Banking-Webanwendung mit FastAPI (Backend), SQLite (Datenbank) und Vanilla JS (Frontend).

---

## Projektstruktur

```
banking-app/
├── main.py                    # FastAPI-App, Entry Point
├── requirements.txt           # Python-Abhängigkeiten
├── backend/
│   ├── core/
│   │   ├── config.py          # App-Einstellungen (JWT, DB)
│   │   ├── database.py        # SQLAlchemy-Setup, get_db
│   │   └── security.py        # Passwort-Hashing, JWT, Auth-Dependency
│   ├── models/
│   │   ├── user.py            # SQLAlchemy-Modell: User
│   │   ├── account.py         # SQLAlchemy-Modell: Account
│   │   └── transaction.py     # SQLAlchemy-Modell: Transaction
│   ├── schemas/
│   │   └── schemas.py         # Pydantic-Schemas (Request/Response)
│   └── routers/
│       ├── auth.py            # POST /register, /login, /token, GET /me
│       ├── accounts.py        # GET/POST /accounts
│       └── transactions.py    # GET /transactions, POST /transfer
└── frontend/
    ├── index.html             # Single-Page-App
    └── static/
        ├── css/style.css      # Luxury Dark Theme
        └── js/app.js          # Gesamte Frontend-Logik
```

---

## Schnellstart

### 1. Voraussetzungen

- Python 3.10 oder neuer
- pip

### 2. Abhängigkeiten installieren

```bash
cd banking-app
pip install -r requirements.txt
```

### 3. Anwendung starten

```bash
python -m uvicorn main:app --reload
```

Die Anwendung ist nun erreichbar unter: **http://localhost:8000**

API-Dokumentation (Swagger): **http://localhost:8000/api/docs**

---

## Funktionen

| Feature                  | Beschreibung                                           |
|--------------------------|--------------------------------------------------------|
| **Registrierung**        | Konto erstellen mit E-Mail, Name & Passwort            |
| **Login / Auth**         | JWT-basierte Authentifizierung (Bearer Token)          |
| **Kontenübersicht**      | Alle Konten mit Saldo auf einen Blick                  |
| **Transaktionshistorie** | Vollständige Ein-/Ausgangsliste mit Filterung          |
| **Überweisung**          | Sofortige interne Überweisungen zwischen Konten        |
| **Neues Konto**          | Girokonto oder Sparkonto eröffnen                      |
| **Auto-Login**           | JWT im localStorage – Sitzung bleibt nach Reload       |

---

## Sicherheitshinweise

> ⚠️ Dies ist ein **Prototyp** für Demonstrations- und Lernzwecke.

Für den Produktiveinsatz müssen folgende Punkte angepasst werden:

- `SECRET_KEY` in `.env` Datei auslagern und sicher generieren:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- HTTPS / TLS aktivieren
- CORS auf spezifische Domains einschränken
- Rate-Limiting für Auth-Endpunkte einbauen
- Produktionsdatenbank (PostgreSQL) verwenden
- Logging & Monitoring einrichten

---

## Demo-Daten

Bei der Registrierung erhält jeder neue Nutzer automatisch:
- 1 Girokonto mit **€ 2.500,00** Startguthaben

Zum Testen von Überweisungen: Zwei Konten registrieren, die IBAN des Zielkontos in der Konten-Ansicht kopieren.
