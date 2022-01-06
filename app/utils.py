
from passlib.context import CryptContext


pwd_contect = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_contect.hash(password)