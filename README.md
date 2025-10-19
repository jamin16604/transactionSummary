# transactionSummary

## Requirements
- Python 3.11+
- pip/venv

## Install
- python -m venv ./venv
- pip install -r requirements.txt

## Run the API
- uvicorn app.main:app --reload

## Overview 
Ingests a CSV of transations into DuckDB database and provides quick summary statistics for specified user within a time frame.

### Data model (CSV)
Required headers:
- transaction_id
- user_id
- product_id
- timestamp
- transaction_amount

### Endpoints

#### POST /upload
Uploads a CSV file, server then creates or replaces transactions table

#### GET /summary/{user_id}
Computes min, max, and mean for user within a time frame

##### Query Parameters:
- start_date
- end_date

### Testing
Unit & Integration : pytest-q

