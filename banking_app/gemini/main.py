from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import database as db

app = FastAPI()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={}, )

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), d: Session = Depends(get_db)):
    hashed_pw = get_password_hash(password)
    new_user = db.User(username=username, hashed_password=hashed_pw)
    d.add(new_user)
    d.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), d: Session = Depends(get_db)):
    user = d.query(db.User).filter(db.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return HTMLResponse(content="Login fehlgeschlagen. <a href='/'>Zurück</a>", status_code=401)
    return RedirectResponse(url=f"/dashboard/{user.id}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/dashboard/{user_id}", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int, d: Session = Depends(get_db)):
    user = d.query(db.User).filter(db.User.id == user_id).first()
    if not user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse(request=request, name="dashboard.html",context={"user": user}, )

@app.post("/transfer/{user_id}")
async def transfer(user_id: int, recipient: str = Form(...), amount: float = Form(...), d: Session = Depends(get_db)):
    user = d.query(db.User).filter(db.User.id == user_id).first()
    if user.balance < amount:
        return HTMLResponse(content="Nicht genügend Guthaben! <a href='/dashboard/{}'>Zurück</a>".format(user_id))
    
    user.balance -= amount
    new_tx = db.Transaction(amount=-amount, recipient=recipient, user_id=user.id)
    d.add(new_tx)
    d.commit()
    return RedirectResponse(url=f"/dashboard/{user_id}", status_code=status.HTTP_303_SEE_OTHER)
