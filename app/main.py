from fastapi import FastAPI
from app.api.upload import router as upload_r

app = FastAPI(title="Transaction Summary API")
app.include_router(upload_r)
@app.get("/")
async def health():
    return {"status": "ok"}