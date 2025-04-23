from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import text
from app.db.session import SessionLocal
from app.routes.user_route import router as user_router
from app.routes.document_route import router as document_router
from app.routes.fragment_route import router as fragment_router
from app.routes.vectorindex_route import router as vectorindex_router
from app.routes.ask_route import router as ask_router

app = FastAPI()

app.include_router(user_router)
app.include_router(document_router)
app.include_router(fragment_router)
app.include_router(vectorindex_router)
app.include_router(ask_router)
print("user_router incluido correctamente")
print("document_router incluido correctamente")
print("fragment_router incluido correctamente")
print("vectorindex_router incluido correctamente")
print("ask_router incluido correctamente")


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
