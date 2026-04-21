import secrets
from decimal import Decimal

from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models
from .auth import hash_password


DEFAULT_ACCOUNTS = [
    ("Girokonto", Decimal("1000.00")),
    ("Sparkonto", Decimal("2500.00")),
]


def generate_account_number(db: Session) -> str:
    while True:
        account_number = "DEMO" + secrets.token_hex(4).upper()
        exists = db.query(models.Account).filter_by(account_number=account_number).first()
        if not exists:
            return account_number



def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()



def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()



def create_user(db: Session, username: str, email: str, password: str) -> models.User:
    user = models.User(
        username=username,
        email=email,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.flush()

    for account_name, opening_balance in DEFAULT_ACCOUNTS:
        account = models.Account(
            user_id=user.id,
            name=account_name,
            account_number=generate_account_number(db),
            balance=opening_balance,
        )
        db.add(account)

    db.commit()
    db.refresh(user)
    return user



def get_user_accounts(db: Session, user_id: int):
    return (
        db.query(models.Account)
        .filter(models.Account.user_id == user_id)
        .order_by(models.Account.id.asc())
        .all()
    )



def get_account_by_id(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()



def get_account_by_number(db: Session, account_number: str):
    return db.query(models.Account).filter(models.Account.account_number == account_number).first()



def get_account_transactions(db: Session, account_id: int):
    return (
        db.query(models.Transaction)
        .filter(
            or_(
                models.Transaction.from_account_id == account_id,
                models.Transaction.to_account_id == account_id,
            )
        )
        .order_by(models.Transaction.created_at.desc())
        .all()
    )
