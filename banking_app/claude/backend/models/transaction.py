from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.core.database import Base


class TransactionType(str, enum.Enum):
    TRANSFER = "Überweisung"
    DEPOSIT = "Einzahlung"
    WITHDRAWAL = "Auszahlung"


class TransactionStatus(str, enum.Enum):
    PENDING = "Ausstehend"
    COMPLETED = "Abgeschlossen"
    FAILED = "Fehlgeschlagen"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, index=True, nullable=False)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="EUR")
    description = Column(String, nullable=True)
    transaction_type = Column(Enum(TransactionType), default=TransactionType.TRANSFER)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.COMPLETED)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="sent_transactions")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="received_transactions")
