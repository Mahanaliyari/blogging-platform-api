from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemas,database,utils, models, oauth2

router =  APIRouter(
    tags= ["Auth"]
)

@router.post("/login", status_code= status.HTTP_201_CREATED, response_model = schemas.Token)
def login(user_credentials: schemas.LoginCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_credentials.email == models.User.email).first() # type: ignore
    
    if not user: 
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f" Invalid Credentials")
        
    if not utils.verify(user_credentials.password, user.password): 
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f"Invalid Credentials")
    
    # We decided to put user_id into payload
    token = oauth2.create_token({"user_id": user.id})
    
    return {"token": token, "token_type": "bearer"}  