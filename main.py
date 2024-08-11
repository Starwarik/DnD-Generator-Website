from contextlib import asynccontextmanager

from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from jwt.exceptions import InvalidTokenError

import bcrypt

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing_extensions import Annotated

from sqlmodel import Field, SQLModel, create_engine, Session, select, or_
from sqlalchemy.sql.schema import Column
from sqlalchemy import String

from smtp import DummyNorification

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = "sqlite:///database.db"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", String, unique=True))
    password: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    balance: float = Field(default=0.0)


class UserRegisterForm(BaseModel):
    username: str
    password: str
    email: str


class RestPasswordForm(BaseModel):
    new_password: str
    token_reset: str


class Token(BaseModel):
    status: bool = True
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


mail_server = DummyNorification()

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global mail_server
    create_db_and_tables()
    mail_server.start()
    yield
    mail_server.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def send_reset_message(email: str, token: str):
    global mail_server
    mail_server.send_refactory_notification(email, token)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def get_user_by_id(id: str, session: Session) -> User | None:
    statement = select(User).where(User.id == id)
    results = session.exec(statement)
    result = results.first()
    return result


def get_user_by_username(username: str, session: Session) -> User | None:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    result = results.first()
    return result


def get_user_by_email(email: str, session: Session) -> User | None:
    statement = select(User).where(User.email == email)
    results = session.exec(statement)
    result = results.first()
    return result


def get_user_by_email_or_username(
    email_or_username: str, session: Session
) -> User | None:
    statement = select(User).where(
        or_(User.email == email_or_username, User.username == email_or_username)
    )
    results = session.exec(statement)
    result = results.first()
    return result


def authenticate_user(
    username_or_email: str, password: str, session: Session
) -> User | None:
    user = get_user_by_email_or_username(username_or_email, session)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"status": False},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_id(user_id, session)
    if user is None:
        raise credentials_exception
    return user


@app.post("/api/token")
@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/api/register")
def register(user: UserRegisterForm, session: Session = Depends(get_session)):
    user_username = get_user_by_username(user.username, session)
    user_email = get_user_by_email(user.email, session)
    current_user = user_username or user_email
    if not (current_user is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user = User(
            username=user.username,
            password=get_password_hash(user.password),
            email=user.email,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": True}
    except Exception:
        return {"status": False}


@app.get("/api/reset_password")
def reset_password(email: str, session: Session = Depends(get_session)):
    user = get_user_by_email(email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    reset_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    reset_token = create_access_token(
        data={"sub": user.id, "type": "reset"}, expires_delta=reset_token_expires
    )
    send_reset_message(user.email, reset_token)
    return {"status": True, "reset_token": reset_token}


@app.get("/api/user_info")
def get_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "status": True,
        "username": current_user.username,
        "email": current_user.email,
        "balance": current_user.balance,
    }


@app.post("/api/reset_password")
def reset_password(
    reset_form: RestPasswordForm, session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"status": False},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(reset_form.token_reset, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None or payload.get("type") != "reset":
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_id(user_id, session)
    if user is None:
        raise credentials_exception

    user.password = get_password_hash(reset_form.new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": True}


@app.post("/api/spend_balance")
def spend_balance(
    money: float,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> float:
    if money < 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    if money - current_user.balance > 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user.balance -= money
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user.balance


"""
Debug function

@app.get("/api/get_users")
def get_all_users(session: Session = Depends(get_session)):
    statement = select(User)
    results = session.exec(statement)
    result = results.all()
    return result
"""
