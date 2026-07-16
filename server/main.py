from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI(title="AI Career Mentor API")

@app.get("/")
def read_root():
    return {"message": "AI Career Mentor API is running"}

@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected successfully"}
    except Exception as e:
        return {"database": "connection failed", "error": str(e)}