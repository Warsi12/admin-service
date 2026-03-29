import bcrypt
import hashlib

def _pre_hash(password: str) -> bytes:
    """Pre-hash password with SHA-256 to overcome bcrypt 72-character limit."""
    # Bcrypt expects bytes for the password input. 
    # SHA-256 digest is always 32 bytes, which is well under the 72 bytes limit.
    return hashlib.sha256(password.encode("utf-8")).digest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password by pre-hashing and using bcrypt.checkpw."""
    try:
        return bcrypt.checkpw(_pre_hash(plain_password), hashed_password.encode("utf-8"))
    except Exception:
        # Fallback for any unexpected errors (e.g. malformed hash)
        return False

def get_password_hash(password: str) -> str:
    """Get password hash by pre-hashing and using bcrypt.hashpw."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(_pre_hash(password), salt).decode("utf-8")
