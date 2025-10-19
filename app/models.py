from pydantic import BaseModel
from datetime import datetime


class UploadResponse(BaseModel):
    rows_processed: int
    timetaken_ms: int


class SummaryResponse(BaseModel):
    user_id: int
    max_transaction_amount: float
    min_transaction_amount: float
    mean_transaction_amount: float
    start_date: datetime
    end_date: datetime
