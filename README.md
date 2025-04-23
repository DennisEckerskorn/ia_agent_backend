
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

---

## 👤 Usuarios

### 🔐 POST /users/login
Inicia sesión y devuelve un token JWT.
- **Body**: Form (username, password)
- **Access**: Público

### 🆕 POST /users/register
Registra un nuevo usuario. Solo accesible por usuarios con rol "admin".
- **Body**: JSON { username, password, role }
- **Access**: Admin

### 👤 GET /users/me
Devuelve los datos del usuario autenticado actual.
- **Access**: User / Admin

### 📋 GET /users/listAll
Lista todos los usuarios registrados.
- **Access**: Admin

### 🗑 DELETE /users/delete/{user_id}
Elimina un usuario por su ID.
- **Access**: Admin

---

## 📄 Documentos

### 📤 POST /documents/upload
Sube un documento PDF, lo almacena en disco, lo procesa (fragmenta + vectoriza) y lo indexa en FAISS.
- **Body**: Form (name, file)
- **Access**: Admin

### ✍️ POST /documents/
Crea una entrada de documento manual (sin archivo real).
- **Body**: JSON { name }
- **Access**: Admin

### 📁 GET /documents/
Lista todos los documentos cargados.
- **Access**: User / Admin

### 🔍 GET /documents/{doc_id}
Devuelve la información de un documento por ID.
- **Access**: User / Admin

### 🗑 DELETE /documents/{doc_id}
Elimina un documento por su ID.
- **Access**: Admin

---

## 🧩 Fragmentos

### 🆕 POST /fragments/
Crea un fragmento manualmente.
- **Access**: Admin

### 📁 GET /fragments/
Lista todos los fragmentos existentes.
- **Access**: User / Admin

### 🔍 GET /fragments/{id}
Devuelve un fragmento por ID.
- **Access**: User / Admin

### 🔗 GET /fragments/by-document/{doc_id}
Lista todos los fragmentos asociados a un documento.
- **Access**: User / Admin

### 🗑 DELETE /fragments/{id}
Elimina un fragmento por ID.
- **Access**: Admin

---

## 🧠 Vector Index (FAISS)

### 🆕 POST /vector-index/
Crea una nueva entrada en el índice vectorial manualmente.
- **Body**: JSON { fragment_id, vector_id }
- **Access**: Admin

### 🔍 GET /vector-index/{id}
Devuelve un vector por su ID en base de datos.
- **Access**: User / Admin

### 🔎 GET /vector-index/faiss-id/{faiss_id}
Devuelve un vector por su ID interno en FAISS.
- **Access**: User / Admin

### 🔗 GET /vector-index/fragment/{fragment_id}
Lista los vectores asociados a un fragmento.
- **Access**: User / Admin

### 🗑 DELETE /vector-index/{id}
Elimina una entrada vectorial por ID.
- **Access**: Admin

---

## 🤖 Inteligencia Artificial

### ❓ POST /ask
Consulta semánticamente el contenido de los documentos usando FAISS.
- **Body**: JSON { query: string, top_k: int }
- **Returns**: Lista de fragmentos relevantes
- **Access**: User / Admin

