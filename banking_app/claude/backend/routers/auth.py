from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import verify_password, hash_password, create_access_token, get_current_user
from backend.models.user import User
from backend.models.account import Account, AccountType
from backend.schemas.schemas import UserCreate, UserResponse, Token, LoginRequest
import random
import string

router = APIRouter(prefix="/api/auth", tags=["auth"])


def generate_account_number() -> str:
    return "DE" + "".join(random.choices(string.digits, k=18))


@router.post("/register", response_model=dict, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="E-Mail bereits registriert")

    # Create user
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password)
    )
    db.add(user)
    db.flush()

    # Create default checking account with demo balance
    account = Account(
        account_number=generate_account_number(),
        account_type=AccountType.CHECKING,
        balance=2500.00,
        owner_id=user.id
    )
    db.add(account)
    db.commit()

    return {"message": "Registrierung erfolgreich", "user_id": user.id}


@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige E-Mail oder Passwort"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Konto deaktiviert")

    token = create_access_token(data={"sub": str(user.id)})
    return Token(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/token")
def token_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 compatible endpoint"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Ungültige Anmeldedaten")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
