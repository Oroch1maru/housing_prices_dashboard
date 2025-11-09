def test_login_success(client):
    response = client.post(
        "/api/token",
        json={"username": "demo_user", "password": "demo_password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client):
    response = client.post(
        "/api/token",
        json={"username": "wrong", "password": "wrong_password"}
    )
    assert response.status_code == 401
