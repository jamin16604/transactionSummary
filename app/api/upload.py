from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models import UploadResponse
from app.validation import validate_headers
import csv
import tempfile
from pathlib import Path
from app.storage import load_csv


router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(..., description="CSV file containing transaction data")
) -> UploadResponse:
    """
    Endpoint to upload a CSV file containing transaction data.
    Validates the file type and headers before loading data into the database.
    """
    # Validate file type
    if not (file.filename and file.filename.lower().endswith(".csv")):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a CSV file."
        )
    # Read CSV content
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".csv", mode="wb"
    ) as temp_file:
        head = await file.read(4096)
        temp_file.write(head)
        try:
            # Decode only the head for header validation
            decoded_head = head.decode("utf-8").splitlines()[0]
            headers = set(next(csv.reader([decoded_head])))
            validate_headers(headers)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        while chunk := await file.read(1024 * 1024):
            temp_file.write(chunk)
        temp_file_path = Path(temp_file.name)
    try:
        rows_processed, timetaken_ms = load_csv(temp_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return UploadResponse(rows_processed=rows_processed, timetaken_ms=timetaken_ms)
