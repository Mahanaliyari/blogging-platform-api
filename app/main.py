from fastapi import FastAPI
from .routers import post, user, auth, likes 
from fastapi.middleware.cors import CORSMiddleware

''' this line looks at all your model classes and
automatically creates the corresponding tables in Postgres,
but only the ones that don't already exist.''' 


app = FastAPI() 


origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



'''This line takes all the routes defined inside 
posts.router (everything decorated with @router.get/post/put/delete)
and merges them into your main app — 
as if you'd written them directly in main.py all along.
Same for users.router.'''
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)

@app.get("/")
def root():
    return{'Hello World'}
        
    
    

    
     
            
