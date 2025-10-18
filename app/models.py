from pydantic import BaseModel
from datetime import datetime

class UploadResponse(BaseModel):
    rows_processed: int
    timetaken_ms: int

