import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
import subprocess

root = Path(__file__).parent
gen_data_script = root.parent / "scripts" / "gen_dummy_data.py"
test_data_dir = root / "data"

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def large_csv_path():
    # Generate large dummy data if not already present
    output_file = test_data_dir / "dummy_transactions.csv"
    if not output_file.exists():
        subprocess.run(["python", str(gen_data_script)], check=True)
    return output_file

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

def test_upload_csv_missing_headers(client, tmp_path):
    # Create a dummy CSV file with missing headers
    invalid_csv_path = tmp_path / "invalid.csv"
    invalid_csv_path.write_text("transaction_id,wrong_header1,wrong_header2\nvalue1,value2")

    with open(invalid_csv_path, "rb") as f:
        response = client.post("/upload/", files={"file": ("invalid.csv", f, "text/csv")})

    assert response.status_code == 400
    assert "Missing required headers" in response.json()["detail"]

def test_upload_small_csv_success(client, tmp_path):
    # Create a dummy valid CSV file
    valid_csv_path = tmp_path / "valid.csv"
    valid_csv_path.write_text(
        "transaction_id,user_id,product_id,timestamp,transaction_amount\n"
        "1,100,200,'2023-01-01 10:00:00',50.0\n"
        "2,101,201,'2023-01-02 11:00:00',75.5\n"
    )

    with open(valid_csv_path, "rb") as f:
        response = client.post("/upload/", files={"file": ("valid.csv", f, "text/csv")})

    assert response.status_code == 200
    json_response = response.json()
    assert "rows_processed" in json_response
    assert "timetaken_ms" in json_response
    assert json_response["rows_processed"] == 2

def test_upload_large_csv_success(client):
    large_csv = test_data_dir / "dummy_transactions.csv"
    with open(large_csv, "rb") as f:
        response = client.post("/upload/", files={"file": ("dummy_transactions.csv", f, "text/csv")})

    assert response.status_code == 200
    json_response = response.json()
    assert "rows_processed" in json_response
    assert "timetaken_ms" in json_response
    assert json_response["rows_processed"] == 1_000_000

