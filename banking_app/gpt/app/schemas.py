from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class TransferCreate(BaseModel):
    from_account_id: int
    to_account_number: str = Field(min_length=6, max_length=20)
    amount: Decimal = Field(gt=0)
    reference: str = Field(default="", max_length=255)
