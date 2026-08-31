from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas,database,utils,models,oauth2
from sqlalchemy.orm import Session


router =  APIRouter(
    tags= ["Auth"]
)

@router.post("/login", status_code= status.HTTP_200_OK, response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_credentials.username == models.User.email).first() # type: ignore
    
    if not user: 
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f" Invalid Credentials")
        
    if not utils.verify(user_credentials.password, user.password): 
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f"Invalid Credentials")
    
    # Create token after validating credentials
    # We decided to put user_id into payload
    token = oauth2.create_token({"user_id": user.id})
    
    return {"access_token": token, 
            "token_type": "bearer"}  