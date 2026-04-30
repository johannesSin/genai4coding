from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.core.database import Base


class AccountType(str, enum.Enum):
    CHECKING = "Girokonto"
    SAVINGS = "Sparkonto"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    account_type = Column(Enum(AccountType), default=AccountType.CHECKING)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String, default="EUR")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="accounts")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.from_account_id", back_populates="from_account")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.to_account_id", back_populates="to_account")
