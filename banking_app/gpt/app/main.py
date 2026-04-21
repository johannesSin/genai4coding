from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .db import Base, engine
from .routers import auth, banking

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prototype Banking App")
app.add_middleware(SessionMiddleware, secret_key="change-me-in-production")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(banking.router)
