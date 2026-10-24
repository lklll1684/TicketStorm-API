from fastapi import FastAPI
from app.api.routes import router
app = FastAPI(title="TicketStorm API")
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "TicketStorm работает!"}