from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.core.config import settings
from backend.core.database import create_tables
from backend.routers import auth, accounts, transactions

app = FastAPI(title=settings.APP_NAME, version="1.0.0", docs_url="/api/docs")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)

# Static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.on_event("startup")
def startup():
    create_tables()
    print(f"✅ {settings.APP_NAME} gestartet – http://localhost:8000")


@app.get("/", include_in_schema=False)
@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend(full_path: str = ""):
    if full_path.startswith("api/"):
        return {"detail": "Not Found"}
    return FileResponse("frontend/index.html")
