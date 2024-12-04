from fastapi import (
    HTTPException, Depends, APIRouter
)
from fastapi.responses import HTMLResponse, JSONResponse
from starlette import status
from models.schemas import User
from models.orm import UserORM
from db.database import get_db, SessionLocal
from services.user_services import (
    hash_password, verify_password, get_user_by_email,create_user
)
from fastapi.security import HTTPBearer
from utils.jwt_handler import validateToken, createToken
from datetime import datetime, timedelta
router = APIRouter(tags=['Users'])


@router.post(path='/user/register', tags=['Users'])
def register_user(user: User, db: SessionLocal = Depends(get_db)):
    existing_user = get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail='Email already registered'
        )
    hassed_password = hash_password(user.password)

    new_user = User(email=user.email, password=hassed_password)
    db_newUser = create_user(db=db, user=new_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={'message': 'User created', 'email': db_newUser.email})


@router.post(path='/user/login', tags=['Users'])
def login_user(email: str, password: str, db: SessionLocal = Depends(get_db)):
    user = get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail='Invalid email or password'
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=400,
            detail='Invalid email or password'
        )
    pay_load = {
        "email": user.email,
        "id": user.id,
        "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp())
    }
    token = createToken(pay_load)
    return JSONResponse(
        content={'token': token},
        status_code=status.HTTP_200_OK
    )

