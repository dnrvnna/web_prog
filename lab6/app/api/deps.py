from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.database import User
from app.repos.user_repo import UserRepository

oath2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(
    token: Annotated[str, Depends(oath2_scheme)],
    db: Session = Depends(get_db),  # noqa: B008
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить учетные данные',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get('sub')
    if username is None:
        raise credentials_exception

    repo = UserRepository(db)
    user = repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
