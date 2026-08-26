from fastapi import status,HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import schemas,models,utils




'''Instead of writing "/users" in the path of every route
we define prefix in APIRouter and write "/users"
since this stays constant in our path.
Therefore we dont need to write "/users"
in every route's path'''

router = APIRouter(
    prefix = "/users",
    tags= ["Users"]
)
#--------------------               
# User registration
#--------------------
@router.post("/",status_code= status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate,db : Session = Depends(get_db)): 

        # Hashing user's password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password     
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    
    
@router.get("/{id}", response_model = schemas.UserResponse)
def get_user_info(id: int, db: Session = Depends(get_db)): 
    retrieved_user = db.query(models.User).filter(models.User.id == id).first()
    if not retrieved_user: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f" The user with id {id} does not exist")
    
    return retrieved_user