from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from backend.models.account import AccountType
from backend.models.transaction import TransactionType, TransactionStatus


# ── User Schemas ──────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Passwort muss mindestens 8 Zeichen haben")
        return v

    @field_validator("full_name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name darf nicht leer sein")
        return v.strip()


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Auth Schemas ──────────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ── Account Schemas ───────────────────────────────────────────────
class AccountCreate(BaseModel):
    account_type: AccountType = AccountType.CHECKING


class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: AccountType
    balance: float
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Transaction Schemas ───────────────────────────────────────────
class TransferRequest(BaseModel):
    from_account_id: int
    to_account_number: str
    amount: float
    description: Optional[str] = ""

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("Betrag muss positiv sein")
        if v > 100_000:
            raise ValueError("Maximaler Überweisungsbetrag: 100.000 €")
        return round(v, 2)


class TransactionResponse(BaseModel):
    id: int
    reference: str
    from_account_id: Optional[int]
    to_account_id: Optional[int]
    amount: float
    currency: str
    description: Optional[str]
    transaction_type: TransactionType
    status: TransactionStatus
    created_at: datetime

    class Config:
        from_attributes = True
