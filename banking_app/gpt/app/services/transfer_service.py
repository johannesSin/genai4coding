from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from .. import models

TWOPLACES = Decimal("0.01")


class TransferError(Exception):
    pass



def perform_transfer(
    db: Session,
    *,
    from_account: models.Account,
    to_account: models.Account,
    amount: Decimal,
    reference: str,
) -> models.Transaction:
    amount = amount.quantize(TWOPLACES, rounding=ROUND_HALF_UP)

    if amount <= 0:
        raise TransferError("Der Überweisungsbetrag muss größer als 0 sein.")
    if from_account.id == to_account.id:
        raise TransferError("Quelle und Zielkonto dürfen nicht identisch sein.")
    if from_account.balance < amount:
        raise TransferError("Nicht genügend Guthaben auf dem Quellkonto.")

    from_account.balance = (Decimal(from_account.balance) - amount).quantize(TWOPLACES)
    to_account.balance = (Decimal(to_account.balance) + amount).quantize(TWOPLACES)

    transaction = models.Transaction(
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        amount=amount,
        reference=reference.strip(),
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
