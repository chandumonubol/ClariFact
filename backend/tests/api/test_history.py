import pytest

@pytest.fixture
def auth_users(client):
    # User 1
    client.post("/api/auth/register", json={
        "name": "User One",
        "email": "user1@example.com",
        "password": "pwd"
    })
    token1 = client.post("/api/auth/login", json={"email": "user1@example.com", "password": "pwd"}).json()["access_token"]
    
    # User 2
    client.post("/api/auth/register", json={
        "name": "User Two",
        "email": "user2@example.com",
        "password": "pwd"
    })
    token2 = client.post("/api/auth/login", json={"email": "user2@example.com", "password": "pwd"}).json()["access_token"]
    
    return {"token1": token1, "token2": token2}

def test_history_and_detail(client, auth_users):
    token1 = auth_users["token1"]
    token2 = auth_users["token2"]
    
    # User 1 creates an analysis
    resp = client.post("/api/analyze", json={
        "content_type": "text",
        "text_content": "Fact by user 1"
    }, headers={"Authorization": f"Bearer {token1}"})
    assert resp.status_code == 200
    
    # User 1 gets history
    hist_resp = client.get("/api/history", headers={"Authorization": f"Bearer {token1}"})
    assert hist_resp.status_code == 200
    hist = hist_resp.json()
    assert len(hist) == 1
    analysis_id = hist[0]["analysis_id"]
    
    # User 1 gets detail
    det_resp = client.get(f"/api/history/{analysis_id}", headers={"Authorization": f"Bearer {token1}"})
    assert det_resp.status_code == 200
    assert det_resp.json()["credibility_label"] == "Supported"
    
    # User 2 tries to get User 1's history (should be empty for user 2)
    hist2_resp = client.get("/api/history", headers={"Authorization": f"Bearer {token2}"})
    assert hist2_resp.status_code == 200
    assert len(hist2_resp.json()) == 0
    
    # User 2 tries to access User 1's analysis detail
    det2_resp = client.get(f"/api/history/{analysis_id}", headers={"Authorization": f"Bearer {token2}"})
    assert det2_resp.status_code == 404
