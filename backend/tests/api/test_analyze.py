import pytest

@pytest.fixture
def auth_token(client):
    client.post("/api/auth/register", json={
        "name": "Analyze User",
        "email": "analyze@example.com",
        "password": "secure"
    })
    response = client.post("/api/auth/login", json={
        "email": "analyze@example.com",
        "password": "secure"
    })
    return response.json()["access_token"]

def test_analyze_text_success(client, auth_token):
    response = client.post("/api/analyze", json={
        "content_type": "text",
        "text_content": "This is a credible fact."
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.json()
    # Real AI: no evidence available at Checkpoint 1, so assessment is Uncertain
    assert data["credibility_label"] == "Uncertain"
    assert len(data["claims"]) > 0
    # No external evidence retrieved at Checkpoint 1
    assert len(data["evidence"]) == 0

def test_analyze_text_fake(client, auth_token):
    response = client.post("/api/analyze", json={
        "content_type": "text",
        "text_content": "This is a fake hoax."
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["credibility_label"] == "Potentially Misleading"

def test_analyze_unauth(client):
    response = client.post("/api/analyze", json={
        "content_type": "text",
        "text_content": "This is a credible fact."
    })
    assert response.status_code == 401

def test_analyze_empty_text(client, auth_token):
    response = client.post("/api/analyze", json={
        "content_type": "text",
        "text_content": "   "
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400

def test_analyze_wrong_type(client, auth_token):
    response = client.post("/api/analyze", json={
        "content_type": "image"
    }, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 400
