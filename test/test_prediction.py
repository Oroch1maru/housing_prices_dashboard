import pytest
from app.core.security import settings


@pytest.fixture(scope="module")
def auth_token(client):
    response = client.post(
        "/api/token",
        json={"username": "demo_user", "password": "demo_password"}
    )
    return response.json()["access_token"]

def test_prediction_success(client, auth_token):
    payload = {
        "longitude": -122.64,
        "latitude": 38.01,
        "housing_median_age": 36.0,
        "total_rooms": 1336.0,
        "total_bedrooms": 258.0,
        "population": 678.0,
        "households": 249.0,
        "median_income": 5.5789,
        "ocean_proximity": "NEAR OCEAN"
    }

    response = client.post(
        "/api/predict",
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )

    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], float)

def test_prediction_unauthorized(client):
    payload = {
        "longitude": -117.96,
        "latitude": 33.89,
        "housing_median_age": 24.0,
        "total_rooms": 1332.0,
        "total_bedrooms": 252.0,
        "population": 625.0,
        "households": 230.0,
        "median_income": 4.4375,
        "ocean_proximity": "<1H OCEAN"
    }

    response = client.post("/api/predict", json=payload)
    assert response.status_code == 403

def test_rate_limit_exceeded(client, auth_token):
    payload = {
        "longitude": -117.96,
        "latitude": 33.89,
        "housing_median_age": 24.0,
        "total_rooms": 1332.0,
        "total_bedrooms": 252.0,
        "population": 625.0,
        "households": 230.0,
        "median_income": 4.4375,
        "ocean_proximity": "<1H OCEAN"
    }

    for _ in range(settings.RATE_LIMIT_PER_MINUTE-1):
        response = client.post(
            "/api/predict",
            headers={"Authorization": f"Bearer {auth_token}"},
            json=payload
        )
        assert response.status_code == 200

    response = client.post(
        "/api/predict",
        headers={"Authorization": f"Bearer {auth_token}"},
        json=payload
    )

    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text

