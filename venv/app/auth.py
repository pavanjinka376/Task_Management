from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

# ---------------- CONFIG ----------------
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------- PASSWORD ----------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    # bcrypt supports max 72 bytes
    password = password.encode("utf-8")[:72]
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    password = password.encode("utf-8")[:72]
    return pwd_context.verify(password, hashed_password)

# ---------------- JWT ----------------
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
