import bcrypt

def hash_password(password: str) -> str:
    pw = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)
    return hashed.decode()

def verify_password(password: str, hashed: str) -> bool:
    pw = password.encode()
    return bcrypt.checkpw(pw, hashed.encode())