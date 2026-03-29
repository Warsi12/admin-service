from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _pre_hash(password: str) -> str:
    """Pre-hash password with SHA-256 to overcome bcrypt 72-character limit."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(_pre_hash(plain_password), hashed_password)

def get_password_hash(password):
    return pwd_context.hash(_pre_hash(password))
