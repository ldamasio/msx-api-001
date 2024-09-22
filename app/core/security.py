from pwdlib import PasswordHash

# Cria uma instância do PasswordHash com o algoritmo recomendado (Argon2)
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash a password using Argon2."""
    return password_hash.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    """Verify a password against its hash."""
    return password_hash.verify(hashed_password, password)
