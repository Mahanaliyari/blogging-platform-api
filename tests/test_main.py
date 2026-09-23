

'''call the client fixture from conftest, 
runs the fixture and returns the result to test_root'''
def test_root(client):
    # sends a GET request to "/" and stores the response
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {'message':'Hello World'}