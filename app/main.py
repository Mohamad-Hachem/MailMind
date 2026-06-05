import os
import psycopg
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Account
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="MailMind API",
    lifespan=lifespan,
)



@app.get("/")
def root():
    return {"message": "MailMind API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    database_url = os.getenv("DATABASE_URL")

    try:
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()

        return {
            "database": "connected",
            "result": result[0],
        }

    except Exception as e:
        return {
            "database": "error",
            "detail": str(e),
        }


@app.post("/accounts")
def create_account(email_address: str, password_hash: str, db: Session = Depends(get_db),):
    account = Account(email_address=email_address, password_hash=password_hash)

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


@app.get("/accounts")
def list_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return accounts