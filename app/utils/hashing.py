from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hashing:
    @staticmethod
    def hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def verify(password, hashed_password):
        return pwd_context.verify(password, hashed_password)