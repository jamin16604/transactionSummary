import csv
import random
from pathlib import Path
from faker import Faker #type: ignore

TRANSACTIONS = 1_000_000
HEADERS = ["transaction_id", "user_id", "product_id", "timestamp", "transaction_amount"]
# Initialize Faker
fake = Faker()
root = Path(__file__).parent
tests_dir = root.parent / "tests" / "data"
tests_dir.mkdir(parents=True, exist_ok=True)
output = tests_dir / "dummy_transactions.csv"
# Open the CSV file for writing
with output.open(mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=HEADERS)
    writer.writeheader()
    # Generate dummy data
    for _ in range(TRANSACTIONS):
        writer.writerow(
            {
                "transaction_id": fake.uuid4(),
                "user_id": fake.random_int(min=1, max=1000),
                "product_id": fake.random_int(min=1, max=500),
                "timestamp": fake.date_time_between(start_date="-1y", end_date="now"),
                "transaction_amount": round(random.uniform(5.0, 500.0), 2),
            }
        )
