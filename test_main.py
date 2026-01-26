from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "System walutowy dziala"}

def test_get_currencies_empty():
    response = client.get("/currencies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_fetch_currency_mock():
    mock_nbp_response = {
        "code": "USD",
        "rates": [
            {"mid": 4.50, "effectiveDate": "2025-01-01"},
            {"mid": 4.55, "effectiveDate": "2025-01-02"}
        ]
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_nbp_response

        payload = {
            "currency": "USD",
            "start_date": "2025-01-01",
            "end_date": "2025-01-02"
        }
        
        response = client.post("/currencies/fetch", json=payload)
        
        assert response.status_code == 200
        assert "Pobrano 2 nowych kursow" in response.json()["message"]

def test_get_currencies_after_fetch():
    response = client.get("/currencies/2025-01-01")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["rate"] == 4.50