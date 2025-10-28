from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="Cool CI/CD API", version="1.0.0")

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS kv (
            id SERIAL PRIMARY KEY,
            k VARCHAR(64) UNIQUE NOT NULL,
            v TEXT NOT NULL
        );
    """))
    conn.commit()

class KVItem(BaseModel):
    k: str
    v: str

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kv", response_model=List[KVItem])
def list_kv():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT k, v FROM kv ORDER BY k ASC"))
        return [{"k": r[0], "v": r[1]} for r in rows]

@app.put("/kv", response_model=KVItem)
def upsert_kv(item: KVItem):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO kv (k, v) VALUES (:k, :v)
            ON CONFLICT (k) DO UPDATE SET v = EXCLUDED.v
        """), {"k": item.k, "v": item.v})
        conn.commit()
    return item
