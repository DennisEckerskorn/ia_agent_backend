import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ValidationError

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    #Later: SECRET_KEY: str
    #Later: OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError as e:
    print("Error cargando las variables de entorno:")
    print(e)
    raise SystemExit("Deteniendo la aplicación por configuración incompleta")
