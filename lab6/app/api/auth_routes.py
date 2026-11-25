from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.shemas import Token, UserCreate, UserResponse
from app.repos.user_repo import UserRepository

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    repo = UserRepository(db)
    if repo.get_by_username(user_data.username):
        raise HTTPException(
            status_code=400, detail='Пользователь уже зарегистрирован'
        )
    return repo.create(user_data)


@router.post('/login', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
):
    repo = UserRepository(db)
    user = repo.get_by_username(form_data.username)
    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неправильное имя пользователя или пароль',
        )
    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=UserResponse)
def reads_user_me(current_user: CurrentUser):
    return current_user
