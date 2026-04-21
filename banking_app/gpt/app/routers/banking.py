from decimal import Decimal

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..crud import (
    get_account_by_id,
    get_account_by_number,
    get_account_transactions,
    get_user_accounts,
)
from ..db import get_db
from ..deps import get_current_user
from ..services.transfer_service import TransferError, perform_transfer

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = request.session.get("user")
    return RedirectResponse(url="/dashboard" if username else "/login", status_code=303)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    accounts = get_user_accounts(db, user.id)
    total_balance = sum(Decimal(account.balance) for account in accounts)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "title": "Kontenübersicht",
            "user": user,
            "accounts": accounts,
            "total_balance": total_balance,
        },
    )


@router.get("/accounts/{account_id}/transactions", response_class=HTMLResponse)
def transactions(account_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account = get_account_by_id(db, account_id)
    if not account or account.user_id != user.id:
        return RedirectResponse(url="/dashboard", status_code=303)

    txs = get_account_transactions(db, account.id)
    return templates.TemplateResponse(
        "transactions.html",
        {
            "request": request,
            "title": "Transaktionshistorie",
            "user": user,
            "account": account,
            "transactions": txs,
        },
    )


@router.get("/transfer", response_class=HTMLResponse)
def transfer_form(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "transfer.html",
        {
            "request": request,
            "title": "Überweisung",
            "user": user,
            "accounts": get_user_accounts(db, user.id),
        },
    )


@router.post("/transfer", response_class=HTMLResponse)
def transfer(
    request: Request,
    from_account_id: int = Form(...),
    to_account_number: str = Form(...),
    amount: str = Form(...),
    reference: str = Form(""),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    accounts = get_user_accounts(db, user.id)
    from_account = get_account_by_id(db, from_account_id)
    to_account = get_account_by_number(db, to_account_number.strip())

    error = None
    if not from_account or from_account.user_id != user.id:
        error = "Das ausgewählte Quellkonto ist ungültig."
    elif not to_account:
        error = "Das Zielkonto wurde nicht gefunden."
    else:
        try:
            amount_decimal = Decimal(amount)
            perform_transfer(
                db,
                from_account=from_account,
                to_account=to_account,
                amount=amount_decimal,
                reference=reference,
            )
        except Exception as exc:
            if isinstance(exc, (ArithmeticError, ValueError)):
                error = "Bitte gib einen gültigen Betrag ein."
            elif isinstance(exc, TransferError):
                error = str(exc)
            else:
                error = "Die Überweisung konnte nicht durchgeführt werden."

    if error:
        return templates.TemplateResponse(
            "transfer.html",
            {
                "request": request,
                "title": "Überweisung",
                "user": user,
                "accounts": accounts,
                "error": error,
                "form": {
                    "from_account_id": from_account_id,
                    "to_account_number": to_account_number,
                    "amount": amount,
                    "reference": reference,
                },
            },
            status_code=400,
        )

    return RedirectResponse(url=f"/accounts/{from_account_id}/transactions", status_code=303)
