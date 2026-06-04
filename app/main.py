import os

import psycopg
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "MailMind API is running"}


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