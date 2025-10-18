import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
import subprocess

root = Path(__file__).parent
gen_data_script = root.parent / "scripts" / "gen_dummy_data.py"
test_data_dir = root / "data"

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="session")
def large_csv_path():
    # Generate large dummy data if not already present
    output_file = test_data_dir / "dummy_transactions.csv"
    if not output_file.exists():
        subprocess.run(["python", str(gen_data_script)], check=True)
    return output_file
