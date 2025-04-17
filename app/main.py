from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import text
from app.db.session import SessionLocal
from app.routes.user_route import router as user_router

app = FastAPI()

app.include_router(user_router)
print("✅ user_router incluido correctamente")


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
