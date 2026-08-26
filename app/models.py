from .database import Base 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Relationship

''' "base" is what tells SQLAlchemy "this isn't just a normal Python class,
treat this as a database table definition.'''

class Post(Base): 
    __tablename__ = "posts"
    
    id = Column(Integer,primary_key= True, nullable= False)
    title = Column(String,nullable= False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default= 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)
    
    '''This column is linked and has relationship with the User table 
    so that it fetches the data about the user and we can use the user's data 
    to return back to the frontend (in our response)'''
    owner = Relationship("User")
    

class User(Base): 
    __tablename__ = "users"
    
    id = Column(Integer,primary_key= True, nullable= False)
    email = Column(String,nullable= False, unique= True)
    password = Column(String,nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), server_default= text('now()'), nullable = False)
    phone_number = Column(String)
    
    
class Likes(Base): 
    __tablename__ = "likes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key= True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key= True)