from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database, models
from .config import setting



'''oauth2_scheme is callable (an object you can call like a function),
and FastAPI calls it automatically, 
extracts the token from the incoming request's Authorization header, 
and hands it to you as token.'''

'''tokenUrl= "login" just tells FastAPI's docs (/docs) 
which endpoint or path clients should hit to obtain a token in the first place,
so the interactive Swagger UI can show a proper "Authorize" login form.'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")


'''The backend creates a token (after verifying login credentials), 
sends it to the client, and it's valid for a limited time.
Anyone who presents that valid token in their requests
can access protected routes as the user it represents — 
the server doesn't re-check the password, just the token.'''

# SECRET_KEY
# Algorithm
# Expriation_Time


# data refers to payload in the token 
def create_token(data: dict):
    # Create copy of the data to apply changes
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes= setting.access_token_expire_minutes)
    to_encode.update({"exp" : expire_time.timestamp()})
    token = jwt.encode(to_encode,setting.secret_key, algorithm= setting.algorithm)
    
    return token 


# Verifies the token recieved from the user 
# Extracts and returns the payload data (in this case the user's id)
def verify_token(token: str, credentials_exception): 
    
    try: 
        payload = jwt.decode(token,setting.secret_key, algorithms= [setting.algorithm])
        
        # Extracting whatever payload data we had
        # In this case id 
        id = payload.get("user_id")
        
        if id is None: 
            raise credentials_exception
        
    except JWTError: 
        raise credentials_exception
    
    return id 


# This runs the veify_token() function 
# Returns the user details who sent the token 
# So we know who actually wants to access data and send requests
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    # Define the exception
    credentials_exception =  HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                           detail = "Could not validate credentials",
                                           headers= {"WWW-Authenticate": "Bearer"})
    id = verify_token(token, credentials_exception)
    
    # Retrieve the user's details using their id 
    user_data = db.query(models.User).filter(models.User.id == id).first()
    
    if user_data is None:
        raise credentials_exception
    
    return user_data
    
    
    