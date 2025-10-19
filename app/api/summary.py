from fastapi import APIRouter, Query, HTTPException, Path
from app.models import SummaryResponse
from datetime import datetime
from app.storage import load_summary

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/{user_id}", response_model=SummaryResponse)
async def get_summary(
    user_id: int = Path(..., ge=1, description="User_id"),
    start_date: datetime = Query(
        ..., description="Inclusive start date for transactions"
    ),
    end_date: datetime = Query(..., description="Inclusive end date for transactions"),
) -> SummaryResponse:
    """
    Endpoint to get summary statistics for a given user_id and date range.
    Validates input parameters before querying the database.
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=400, detail="start_date must be before or equal to end_date."
        )
    return load_summary(user_id, start_date, end_date)
