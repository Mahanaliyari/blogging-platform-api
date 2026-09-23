from app import models, utils 


def test_create_user(client, session):
    response = client.post(
        "/users/",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    # Testing the response
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"
    
    user = session.query(models.User).filter(
            models.User.email == "testuser@example.com").first()
    
    # Testing whether new user has been added to database 
    # Also to test whether the password is hashed correctly
    assert user is not None
    assert user.email == "testuser@example.com"
    assert utils.verify("password123", user.password) == True
    
    
def test_duplicate_user(client, session):
    first_response = client.post(
        "/users/",
        json = {
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
    ) 
    
    second_response = client.post(
            "/users/",
            json = {
                "email": "newuser@example.com",
                "password": "newpassword123"
            }
        ) 
    
    assert first_response.status_code == 201 
    assert second_response.status_code == 400
    
    user = session.query(models.User).filter(
        models.User.email == "newuser@example.com").all()
    
    assert len(user) == 1 