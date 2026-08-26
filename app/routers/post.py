from fastapi import APIRouter,status,Response,HTTPException,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models
from .. import oauth2
from sqlalchemy import func



'''APIRouter() is essentially a mini FastAPI app —
it can hold its own set of routes, but it isn't actually "live" or 
connected to your real app until you explicitly plug it in.'''
router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)
 
 
# A post request is made when the user creates something 
# Or when the user sends something to the server 
# This function extracts what the user sent and it returns the final message
@router.post("/",status_code= status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate,db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """
    #                ,(post.title,post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    
    ''' instead of manually assigning corressponding values to each data field in models.post,
    we unpack the dictionary version of "post" (what user enters), and it does the same thing
    '''
    '''We need to assign the id of the current user who is sending post request,
    or in other words the user who wants to create the post to "owner_id". Otherwise 
    the owner_id field will be null and therefore throws an error'''
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    
    '''This does what "RETURNING *" do,
    it retrieves the created post (newly created record) and stores it back to new_post.
    It adds the new datafields that the user hasnt added while creating the post and it returns that back to "new_post" '''
    db.refresh(new_post)
    
    return new_post




@router.get("/" ,response_model= list[schemas.GetLikes])
def get_posts(db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),
              limit : int = 10, skip: int = 0, search: str = ""):
    #cursor.execute(""" SELECT * FROM posts""")
    #posts = cursor.fetchall()
    
    
    # Get or retrieve all the posts of the user who logged in 
    # This will also return the number of likes each post has gotten so far 
    total_likes = db.query(models.Post, func.count(models.Likes.user_id).label("like")).join(
        models.Likes, models.Post.id == models.Likes.post_id,
        isouter= True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
        

    return  total_likes
   
    
   
# Getting a single post from the database 
@router.get("/{id}", response_model = schemas.GetLikes)
# convertt the id into int
def get_post(id: int, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    # retrieving the post with the specific id requested by the user 
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    # retrieved_post = cursor.fetchone()
    
    # first() brings the first instance of a record that its id is equal to the id requested in the path
    # This will also bring the specific post and its number of likes 
    retrieved_post = db.query(models.Post, func.count(models.Likes.user_id).label("like")).join(
        models.Likes, models.Post.id == models.Likes.post_id, isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not retrieved_post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"The post with id {id} doesnt exist")
        
    if retrieved_post.Post.owner_id != current_user.id : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f"Not authorized to perform this action")
    
    
        
        
    return retrieved_post
    
    
   
# Deleting a post
@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s  RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    '''doesn't actually run anything against the database yet. 
    It builds what's called a Query object.
    it waits until you explicitly ask for results before it sends any SQL to Postgres.
    Also we dont add first() at the end of deleted_post because we wont be able to apply
    delete() method on it later on'''
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
        
    ''' first() is what actually executes the query and asks Postgres for a result — specifically,
    it fetches only the first matching row'''
    if deleted_post.first() is None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"The post with id {id} doesnt exist")
    
    if deleted_post.first().owner_id != current_user.id: # type: ignore
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                                           detail = "Not authorized to perform requested action",
                                           headers= {"WWW-Authenticate": "Bearer"})
            
    deleted_post.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    

# Updating an item's title only 
@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db : Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title,post.content,post.published,id))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    
    # "raise" will exit the function like "return"
    if updated_post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                        detail= f"The post with id {id} doesnt exist") 
    
    if updated_post.first().owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                                        detail = "Not authorized to perform requested action",
                                        headers= {"WWW-Authenticate": "Bearer"})
    
    # update() expects a dictionary 
    updated_post.update(post.model_dump(),synchronize_session= False) # type: ignore
    db.commit()
    return updated_post.first()