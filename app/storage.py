import duckdb
import os
from pathlib import Path
import time
from datetime import datetime
from app.models import SummaryResponse
from fastapi import HTTPException

DATA_DIRECTORY = Path(os.getenv("DATA_DIRECTORY", "./data"))
DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIRECTORY / "transactions.duckdb"


def connect_db():
    """
    Connect to the DuckDB database, creating it if it doesn't exist."""
    return duckdb.connect(database=str(DB_PATH))


def load_csv(csv_path: Path):
    """
    Load a CSV file into the DuckDB database.
    Returns the number of rows processed and time taken in milliseconds.
    """
    try:
        start = time.perf_counter()
        conn = connect_db()
        conn.execute(
            f"""
        CREATE OR REPLACE TABLE transactions AS
        SELECT * FROM read_csv_auto('{csv_path}', HEADER=True)
        """
        )
        rows = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()
        if rows is None:
            raise RuntimeError("No rows were loaded into the database.")
        timmetaken_ms = int((time.perf_counter() - start) * 1000)
        return rows[0], timmetaken_ms
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV into database: {e}")


def load_summary(
    user_id: int, start_date: datetime, end_date: datetime
) -> SummaryResponse:
    """
    Get summary statistics for a given user_id and date range.
    Returns max, min, mean transaction amounts along with start and end dates.
    """
    try:
        conn = connect_db()
        result = conn.execute(
            f"""
        SELECT 
            MAX(transaction_amount) AS max_transaction_amount,
            MIN(transaction_amount) AS min_transaction_amount,
            AVG(transaction_amount) AS mean_transaction_amount,
            MIN(timestamp) AS start_date,
            MAX(timestamp) AS end_date
        FROM transactions
        WHERE user_id = {user_id}
        AND timestamp BETWEEN '{start_date}' AND '{end_date}'
        """
        ).fetchone()
        if result is None or any(value is None for value in result):
            raise HTTPException(
                status_code=404,
                detail="No data found for the given user_id and date range.",
            )

        return SummaryResponse(
            user_id=user_id,
            max_transaction_amount=result[0],
            min_transaction_amount=result[1],
            mean_transaction_amount=result[2],
            start_date=result[3],
            end_date=result[4],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve summary: {e}")
