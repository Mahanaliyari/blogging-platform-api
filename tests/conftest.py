from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.database import Base, get_db





TEST_DATABASE_URL = "postgresql://postgres:Zwixhastam*8886@localhost:5432/fastapi_test"

engine = create_engine(TEST_DATABASE_URL)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# This function provides something that other tests can request
# It creates database session for our tests 
@pytest.fixture
def session():
    
    '''before a test runs, wipe the test tables and recreate them
    to get a clean database. Note that this will create our database tables
    automatically (Post, User, Likes)'''
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        '''Give this database session to the test.
        When the test finishes, continue from here'''
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):

    ''' define the override database session
    so whenever an endpoint that is being tested has uses the normal
    database session, will now use the test database session''' 
    def override_get_db():
        try:
            yield session
        finally:
            pass

    '''Whenever a route asks for get_db, don't use the real one, 
    Use the test database session instead. It basically
    replaces dependencies.'''
    app.dependency_overrides[get_db] = override_get_db


    ''' Create a test client to send HTTP requests the
    path of the endpoint.
    Once the program reaches here and creates th TestClient,
    it will stay here until the test function uses this test client and 
    performs the assertions, after the test function has completed, 
    then the program goes to the next part which is at line 68'''
    yield TestClient(app)


    '''Remove the override after the test is finished.
    We don't want that replacement to remain permanently'''
    app.dependency_overrides.clear()
    
    
    
    
@pytest.fixture
def auth_headers(client): 
    # create a user first 
    client.post(
        "/users/",
        json = {
            "email": "mahan100@gmail.com",
            "password": "pass1234"
        }
    )
    
    # login to get the token
    login_response = client.post(
        "/login/",
        data = {
            "username": "mahan100@gmail.com",
            "password": "pass1234"
        }
    )
    
    # store JWT
    token = login_response.json()["access_token"]
    
    
    return {'Authorization': f"Bearer {token}"}
        
            