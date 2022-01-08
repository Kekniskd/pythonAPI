from passlib.context import CryptContext

pwd_contect = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Get hashed password
def hash(password: str):
    return pwd_contect.hash(password)


# Verify password
def verify(plain_password, hashed_password):
    return pwd_contect.verify(plain_password, hashed_password)