from fastapi import FastAPI
from app.api.upload import router as upload_r
from app.api.summary import router as summary_r
app = FastAPI(title="Transaction Summary API")
app.include_router(upload_r)
app.include_router(summary_r)
@app.get("/")
async def health():
    return {"status": "ok"}