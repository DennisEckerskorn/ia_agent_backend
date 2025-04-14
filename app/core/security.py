from cryptography.utils import deprecated
from passlib.context import CryptContext

# Contexto cifrado que usa bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashea una contraseña de texto plano usando bcrypt.
    Se usa al registrar un nuevo usuario o al actualizar una contraseña.
    Al devolver el hash se evita almacenar la contraseña original.
    :param password: Contraseña en texto plano que el usuario proporciona.
    :return: Contraseña en formato hash segura para alamacenar en la base de datos.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que una contraseña en texto plano coincide con su hash.
    Se usa durante el login para comparar las contraseñas.
    :param plain_password: Contraseña actual por el usuario
    :param hashed_password: Hash almacenado en la base de datos
    :return: Booleano que indica si coinciden.
    """
    return pwd_context.verify(plain_password, hashed_password)
