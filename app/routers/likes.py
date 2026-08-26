from fastapi import APIRouter,status,Response,HTTPException,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models
from .. import oauth2


router = APIRouter(prefix = "/likes",
                   tags= ["Likes"])


@router.post("/",status_code=status.HTTP_201_CREATED)
def like_posts(user_like : schemas.LikePost , db: Session = Depends(get_db), 
               current_user = Depends(oauth2.get_current_user)):
    
    liked_post = db.query(models.Post).filter(models.Post.id == user_like.post_id) # type: ignore
    
    # checking if the post even exists   
    if not liked_post.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"The post with id {user_like.post_id} not exist")
        
    # checking if the same user has already liked the post
    if db.query(models.Likes).filter(models.Likes.post_id == user_like.post_id,
                                     models.Likes.user_id == current_user.id).first() and user_like.liked == 1: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail= "A post can not be liked more than once")
        
    if user_like.liked == 1 : 
        new_like = models.Likes(post_id = user_like.post_id, user_id = current_user.id,)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like
    
    else: 
        removed_like = db.query(models.Likes).filter(models.Likes.post_id == user_like.post_id, models.Likes.user_id == current_user.id)
        if not removed_like.first(): 
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail= f" The post with id {user_like.post_id} does not exist")
            
        removed_like.delete(synchronize_session= False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        

        