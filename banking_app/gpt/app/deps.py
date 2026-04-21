from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .crud import get_user_by_username
from .db import get_db



def get_current_user(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})

    user = get_user_by_username(db, username)
    if not user:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})
    return user
