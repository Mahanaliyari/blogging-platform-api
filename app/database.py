from .config import setting 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

''' 
1. You manually create the Postgres database (e.g. "fastapi") — done earlier in your course
2. You write the connection URL pointing to that already-existing database
3. create_engine(url) — connects to that existing database
4. Base.metadata.create_all(bind=engine) — creates TABLES inside that database, if missing
'''

engine = create_engine(setting.sqlalchemy_database_url)
session_local = sessionmaker(autoflush= False, autocommit= False, bind= engine)

'''This is the base class every SQLAlchemy model inherits from (class URL(Base): ...). 
It's what lets SQLAlchemy track "these Python classes correspond to database tables" 
and later generate the actual CREATE TABLE statements from them via
"Base.metadata.create_all()".'''

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
        
        
        
#-------------------------
# Connecting to Database
#-------------------------
# attempt = 0 
# max_tries = 5

# while attempt < max_tries: 
#     try: 
#         conn = psycopg.connect(host= "localhost", dbname= "fastapi",user= "postgres",
#                             password= "Zwixhastam*8886")
#         cursor = conn.cursor(row_factory= dict_row)
#         print("Database connection was succesfull")
#         break
#     # Saves the error in "error" variable to be used and printed later on 
#     except Exception as error : 
#         attempt += 1 
#         print(f"Connection to database failed, Error: {error}")
#         # after running the exception block, waits for 2 seconds before rerunning the loop 
#         time.sleep(2)
# else: 
#     print("Could not connect to database")



# A decorator which tells fastapi to run this function 
# if there was a GET request
# It returns all the posts (the whole database) 