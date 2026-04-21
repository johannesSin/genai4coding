from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import verify_password
from ..crud import create_user, get_user_by_email, get_user_by_username
from ..db import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Registrierung"})


@router.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    error = None
    if get_user_by_username(db, username):
        error = "Der Benutzername ist bereits vergeben."
    elif get_user_by_email(db, email):
        error = "Die E-Mail-Adresse wird bereits verwendet."
    elif len(password) < 6:
        error = "Das Passwort muss mindestens 6 Zeichen lang sein."

    if error:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "title": "Registrierung",
                "error": error,
                "username": username,
                "email": email,
            },
            status_code=400,
        )

    user = create_user(db, username=username, email=email, password=password)
    request.session["user"] = user.username
    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login"})


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "title": "Login",
                "error": "Ungültige Zugangsdaten.",
                "username": username,
            },
            status_code=400,
        )

    request.session["user"] = user.username
    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
