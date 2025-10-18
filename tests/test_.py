import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_upload_csv_invalid_file(client, tmp_path):
    # Create a dummy non-CSV file
    invalid_file_path = tmp_path / "test.txt"
    invalid_file_path.write_text("This is not a CSV file.")

    with open(invalid_file_path, "rb") as f:
        response = client.post("/upload/", files={"file": ("test.txt", f, "text/plain")})

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type. Please upload a CSV file."}
