def test_login(client):
    # First create a user
    client.post(
        "/users/",
        json={
            "email": "loginuser@example.com",
            "password": "password123"
        }
    )

    # Then try to log in
    response = client.post(
        "/login",
        data={
            "username": "loginuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None
    
    
    
def test_invalid_login(client): 
    client.post(
        "/users/", 
        json = {
            "email":"loginuser@example.com", 
            "password": "password123" 
        }
    )
    
    response = client.post(
        "/login/",
        data = {
            "username": "loginuser@example.com", 
            "password": "wrongpassword" 
        }
    )
    
    assert response.status_code == 403
    assert response.json()['detail'] == "Invalid Credentials"