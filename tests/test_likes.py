def test_like_post(client, auth_headers):
    # Create a post
    create_response = client.post(
        "/posts/",
        json={
            "title": "Post to like",
            "content": "Like test",
            "published": True
        },
        headers=auth_headers
    )

    post_id = create_response.json()["id"]

    # Like the post
    response = client.post(
        "/likes/",
        json={
            "post_id": post_id,
            "liked": 1
        },
        headers=auth_headers
    )

    assert response.status_code == 201