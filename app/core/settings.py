import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import ValidationError

# Carga automáticamente las variables de entorno desde el archivo .env en la raíz del proyecto
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str  # Variable obligatoria para conectar a la base de datos

    SECRET_KEY: str

    # Later: OPENAI_API_KEY: str = ""  # API key para OpenAI, inicializada como cadena vacía

    class Config:
        env_file = ".env"  # Indica a Pydantic dónde buscar las variables de entorno


try:
    settings = Settings()
except ValidationError as e:
    print("Error cargando las variables de entorno:")
    print(e)
    raise SystemExit("Deteniendo la aplicación por configuración incompleta")
