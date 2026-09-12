def test_register_user(client):
    response = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"

def test_duplicate_registration(client):
    # First time
    client.post("/api/auth/register", json={
        "name": "Test User 2",
        "email": "dup@example.com",
        "password": "securepassword"
    })
    # Second time
    response = client.post("/api/auth/register", json={
        "name": "Test User 3",
        "email": "dup@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 400

def test_login(client):
    client.post("/api/auth/register", json={
        "name": "Login User",
        "email": "login@example.com",
        "password": "securepassword"
    })
    response = client.post("/api/auth/login", json={
        "email": "login@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client):
    response = client.post("/api/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401

def test_get_me(client):
    # Register and get token
    reg_response = client.post("/api/auth/register", json={
        "name": "Me User",
        "email": "me@example.com",
        "password": "securepassword"
    })
    token = reg_response.json()["access_token"]
    
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"

def test_get_me_unauth(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
