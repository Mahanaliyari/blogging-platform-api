from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr





# Request schema = "what the client sends in"  
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

    

# Inheriting from PostBase()
class PostCreate(PostBase): 
    pass


class PostUpdate(PostBase): 
    pass
    
    
# Response schema that does not return the password back to the user
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
            from_attributes = True   
            
            
# Response schema = "what the server sends back"  
class PostResponse(PostBase):
    id : int
    created_at : datetime 
    owner_id : int 
    
    # This will also return user's detail in the response section 
    owner: UserResponse
    
    # To convert it back from sqlalchemy to pydantic 
    class Config:
        from_attributes = True
        
        
class UserCreate(BaseModel): 
    email: EmailStr
    password: str
    
    
class LoginCreate(BaseModel): 
    email: EmailStr
    password: str
    

class token_data(BaseModel): 
    # This means "this field's value must either be a str, or it can be None."
    id : Optional[str] = None
    
  
# Validating the token created and given to the user  
class Token(BaseModel): 
    token : str
    token_type : str
    

class LikePost(BaseModel): 
    post_id : int
    #Literal[0, 1] tells Pydantic: this field must be precisely 0 or precisely 1.
    liked : Literal[0,1]
    
    
class GetLikes(BaseModel): 
    Post: PostResponse
    like: int