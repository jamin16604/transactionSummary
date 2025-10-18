from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models import UploadResponse

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/",response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    # Validate file type
    if not (file.filename and file.filename.lower().endswith('.csv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")
