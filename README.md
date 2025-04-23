
# 🤖 Agente IA — Backend Inteligente para Documentos

Este es un backend desarrollado con **FastAPI** que permite subir documentos PDF, extraer su contenido, fragmentarlo, generar embeddings semánticos con FAISS y responder preguntas sobre ellos mediante búsqueda vectorial.

---

## 🚀 Tecnologías utilizadas

- **Lenguaje**: Python 3.11+
- **Framework**: FastAPI
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticación**: JWT + OAuth2
- **Vector Search**: FAISS (con persistencia)
- **Procesamiento PDF**: PyMuPDF (fitz)
- **Control de roles**: Admin / User

---

## 🔐 Seguridad y roles

El backend implementa un sistema robusto de autenticación y autorización:

- Autenticación con **JWT** (`/users/login`)
- Roles definidos: `"admin"` y `"user"`
- Acceso restringido según rol mediante `Depends(get_current_user)` y `require_admin`
- Solo usuarios existentes en la base de datos pueden autenticarse

---

## ⚙️ Instalación y configuración

1. Clonar el repositorio:

\`\`\`bash
git clone https://github.com/tu_usuario/agente-ia-backend.git
cd agente-ia-backend
\`\`\`

2. Crear entorno virtual e instalar dependencias:

\`\`\`bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

3. Crear archivo `.env` en la raíz del proyecto:

\`\`\`
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/agent_db
SECRET_KEY=clave-secreta-para-jwt
\`\`\`

4. Crear las tablas en la base de datos:

\`\`\`bash
python create_tables.py
\`\`\`

5. Ejecutar la aplicación:

\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

---

## 🔧 Endpoints principales


