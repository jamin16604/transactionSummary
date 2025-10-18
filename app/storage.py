import duckdb
import os
from pathlib import Path
import time
DATA_DIRECTORY = Path(os.getenv("DATA_DIRECTORY", "./data"))
DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIRECTORY/"transactions.duckdb"


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
        conn.execute(f"""
        CREATE OR REPLACE TABLE transactions AS
        SELECT * FROM read_csv_auto('{csv_path}', HEADER=True)
        """)
        rows = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()
        if rows is None:
            raise RuntimeError("No rows were loaded into the database.")
        timmetaken_ms = int((time.perf_counter() - start) * 1000)
        return rows[0], timmetaken_ms
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV into database: {e}")