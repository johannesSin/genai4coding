# Prototype Internet-Banking-Webanwendung

Diese Demo-Anwendung verwendet **FastAPI** als Backend, **SQLite** als Datenbank und **Jinja2** für ein leichtgewichtiges Web-Frontend.

## Funktionen

- Benutzerregistrierung
- Login / Logout mit Session-Cookie
- Kontenübersicht mit Gesamtsaldo
- Transaktionshistorie pro Konto
- Überweisungen zwischen vorhandenen Konten
- Modulare Projektstruktur

> Hinweis: Das ist ein **Prototyp für Lern- und Demo-Zwecke** und keine produktionsreife Banking-Software.

## Projektstruktur

```text
banking_app/
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   └── banking.py
│   ├── services/
│   │   └── transfer_service.py
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── transactions.html
│   │   └── transfer.html
│   ├── auth.py
│   ├── crud.py
│   ├── db.py
│   ├── deps.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── README.md
└── requirements.txt
```

## Startanleitung

### 1. Abhängigkeiten installieren

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Anwendung starten

```bash
uvicorn app.main:app --reload
```

### 3. Im Browser öffnen

```text
http://127.0.0.1:8000
```

## Demo-Ablauf

1. Benutzer registrieren
2. Automatisch auf das Dashboard weitergeleitet werden
3. Standardmäßig werden zwei Demo-Konten angelegt:
   - Girokonto
   - Sparkonto
4. Über `/transfer` kann Geld auf ein anderes vorhandenes Konto überwiesen werden
5. Über die Kontenübersicht lässt sich die Transaktionshistorie öffnen

## Wichtige Hinweise

Für einen echten Produktiveinsatz wären mindestens zusätzlich nötig:

- Sichere Secret-Verwaltung über Umgebungsvariablen
- CSRF-Schutz
- Strengere Validierung und Berechtigungslogik
- Audit-Logging
- Rate Limiting
- TLS/HTTPS
- Mehrstufige Authentifizierung
- Tests und Monitoring
