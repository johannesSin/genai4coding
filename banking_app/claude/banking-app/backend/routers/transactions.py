from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.models.user import User
from backend.models.account import Account
from backend.models.transaction import Transaction, TransactionType, TransactionStatus
from backend.schemas.schemas import TransferRequest, TransactionResponse
import uuid

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


def generate_reference() -> str:
    return "TXN-" + str(uuid.uuid4()).upper()[:12]


@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    account_id: int = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get all user account IDs
    user_accounts = db.query(Account.id).filter(Account.owner_id == current_user.id).all()
    account_ids = [a.id for a in user_accounts]

    if account_id:
        if account_id not in account_ids:
            raise HTTPException(status_code=403, detail="Kein Zugriff auf dieses Konto")
        account_ids = [account_id]

    transactions = db.query(Transaction).filter(
        (Transaction.from_account_id.in_(account_ids)) |
        (Transaction.to_account_id.in_(account_ids))
    ).order_by(Transaction.created_at.desc()).limit(limit).all()

    return transactions


@router.post("/transfer", response_model=TransactionResponse)
def transfer(
    data: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate source account belongs to user
    from_account = db.query(Account).filter(
        Account.id == data.from_account_id,
        Account.owner_id == current_user.id
    ).first()
    if not from_account:
        raise HTTPException(status_code=404, detail="Quellkonto nicht gefunden")

    # Validate target account
    to_account = db.query(Account).filter(Account.account_number == data.to_account_number).first()
    if not to_account:
        raise HTTPException(status_code=404, detail="Zielkonto nicht gefunden")

    if from_account.id == to_account.id:
        raise HTTPException(status_code=400, detail="Quelle und Ziel dürfen nicht identisch sein")

    if from_account.balance < data.amount:
        raise HTTPException(status_code=400, detail="Nicht ausreichendes Guthaben")

    # Execute transfer
    from_account.balance = round(from_account.balance - data.amount, 2)
    to_account.balance = round(to_account.balance + data.amount, 2)

    transaction = Transaction(
        reference=generate_reference(),
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        amount=data.amount,
        description=data.description or "Überweisung",
        transaction_type=TransactionType.TRANSFER,
        status=TransactionStatus.COMPLETED
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
