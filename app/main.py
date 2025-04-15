# app/main.py
from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.settings import settings

app = FastAPI()


@app.on_event("startup")
def startup_event():
    try:
        db = SessionLocal()
        # Ejecuta una consulta simple
        db.execute(text("SELECT 1"))
        print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print("Error conectando a la base de datos:")
        print(e)
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Agente IA backend operativo"}
