from contextlib import asynccontextmanager

from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing_extensions import Annotated

from sqlmodel import Field, SQLModel, create_engine, Session, select

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = "sqlite:///database.db"  


class User(SQLModel, table=True):  
    id: int | None = Field(default=None, primary_key=True)  
    username: str  
    password: str  
    email: str | None
    balance: float = Field(default=0.0)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None



engine = create_engine(DATABASE_URL, echo=True)  


def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)  


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
    

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        result = results.one()
        return result


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
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


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/register")
def register(username: str, password: str, email: str):
    user = User(
        username=username,
        password=get_password_hash(password),
        email=email
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()


@app.get("/balance")
def get_balance(
    current_user: Annotated[User, Depends(get_current_user)]
) -> float:
    return current_user.balance

@app.post("/spend_balance")
def spend_balance(
    current_user: Annotated[User, Depends(get_current_user)],
    money: float
) -> float:
    if money < 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You can't spend negative money",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if money - current_user.balance > 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="You don't have enough money to pay",
            headers={"WWW-Authenticate": "Bearer"},
        )
    with Session(engine) as session:
        current_user.balance -= money
        session.add(current_user)
        session.commit()  
        session.refresh(current_user)
    return current_user.balance