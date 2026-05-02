from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.models.user import User
from backend.models.account import Account
from backend.schemas.schemas import AccountCreate, AccountResponse
from backend.routers.auth import generate_account_number

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


@router.get("", response_model=List[AccountResponse])
def get_accounts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Account).filter(Account.owner_id == current_user.id).all()


@router.post("", response_model=AccountResponse, status_code=201)
def create_account(data: AccountCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = Account(
        account_number=generate_account_number(),
        account_type=data.account_type,
        balance=0.0,
        owner_id=current_user.id
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id, Account.owner_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Konto nicht gefunden")
    return account
