
from app import models 

def test_create_post(client): 
    
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
    
    
    # Create a post using the token
    post = client.post(
        "/posts/",
        json ={
            "title": "my first title",
            "content": "my first post",
            "published": True
        },
        
        headers={
            'Authorization': f"Bearer {token}"
        }
    ) 
    
    
    assert post.status_code == 201
    assert post.json()["title"] == "my first title"
    assert post.json()["content"] == "my first post"
    
    
    
def test_get_posts(client, auth_headers): 
    
    client.post(
            "/posts/",
            json ={
                "title": "new title",
                "content": "new post",
                "published": True
            },
            
            headers= auth_headers
    )
    
    
    # Retrieve posts
    response = client.get(
        "/posts/", 
        headers= auth_headers  
    )
    
    
    assert response.status_code == 200 
    assert len(response.json()) == 1 
    assert response.json()[0]['Post']['title'] == "new title"
    
    
    
    
def test_update_own_post(client, auth_headers):
    # Create a post
    create_response = client.post(
        "/posts/",
        json={
            "title": "Old title",
            "content": "Old content",
            "published": True
        },
        headers=auth_headers
    )

    post_id = create_response.json()["id"]

    # Update the post
    response = client.put(
        f"/posts/{post_id}",
        json={
            "title": "Updated title",
            "content": "Updated content",
            "published": True
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["content"] == "Updated content"
    
    
    
    
def test_delete_own_post(client, auth_headers, session):
    
    # Create a post first 
    create_response = client.post(
        "/posts/",
        json={
            "title": "Post to delete",
            "content": "This post will be deleted",
            "published": True
        },
        headers=auth_headers
    )

    # Get the post id 
    post_id = create_response.json()["id"]


    # Delete it 
    response = client.delete(
        f"/posts/{post_id}",
        headers=auth_headers
    )

 
    # make sure the post is deleted from database 
    get_response = client.get(
        f"/posts/{post_id}",
        headers=auth_headers
    )

    deleted_post = session.query(models.Post).filter(models.Post.id == post_id).first()
    
    assert response.status_code == 204
    assert deleted_post is None 
    assert get_response.status_code == 404
    
    

def test_update_another_user_post(client, auth_headers): 
    
    # user 1 creates a post
    # Note: "auth_headers" already creates the user and logins the user
    post = client.post(
        "/posts/",
        json = {
            "title": 'user 1 post',
            "content": 'user 1 content',
            'published': 'True'
        },
        
        headers= auth_headers
    )
    
    post_id = post.json()['id']
    
    
    # user 2 sign ins  
    user_2 = client.post(
        "/users/",
        json = {
            'email': "user2@gmail.com",
            'password': "pass12345"
        }
    )
    
    
    # user2 logins 
    user_2_login = client.post(
        "/login/",
        data = {
            'username': "user2@gmail.com",
            "password": "pass12345"
        }
    ) 
    
    user_2_token = user_2_login.json()["access_token"]
    
    
    # user2 wants to update user1 post 
    update_post = client.put(
        f"/posts/{post_id}",
        json = {
            'title': "hacked title",
            'content': 'hacked title',
            'published': True
        },
        # uses user2 token
        headers= {
            'Authorization': f'Bearer {user_2_token}'
        }
    )
    
    
    assert update_post.status_code == 403 
    