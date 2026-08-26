from passlib.context import CryptContext


# Defining Hashing algorithm 
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)


# Function to compare and verify passwords 
# Returns True if both hashed passwords are the same, otherwise False
def verify(plain_pass, hashed_pass): 
    return pwd_context.verify(plain_pass,hashed_pass)